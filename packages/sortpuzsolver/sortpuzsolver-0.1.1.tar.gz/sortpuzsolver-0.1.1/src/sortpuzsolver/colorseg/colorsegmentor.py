import logging
import math

import cv2 as cv
import numpy
import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
from skimage import segmentation, color
from skimage.measure import regionprops
from skimage.util import img_as_ubyte


def sh( im ):
    cv.imshow('window', im)
    cv.waitKey(0)


def pltshow( im, cs='gray'):
    #plt.subplot(122), plt.imshow(im, cs)
    #plt.title('Show'), plt.xticks([]), plt.yticks([])
    plt.imshow(im)
    plt.show()


def abdiff( l1, l2 ):
    return abs(l1 - l2)


def square_mean( l1, l2 ):
    """Finds mean squared deviation of two colors.

    Parameters
    ----------
    l1, l2 : array-like
        The colors which should be an iterable list of values

    Raises
    ------
    EquivalenceError
        The provided lists were not of the same length

    Returns
    -------
    float
        The mean squared deviation
    """
    try:
        if len(l1) != len(l2):
            raise EquivalenceError("Input lists are of different length", len(l1), len(l2))
        diff = 0.0
        s = 0.0
        # TODO: change it so the 180 and 0 loop instead of having large difference
        #   might have to detect HSV first
        for il in range(len(l1)):
            diff = float(l1[il]) - float(l2[il])
            s = s + pow(diff, 2)
        return math.sqrt(s)
    except EquivalenceError as err:
        logging.error(err)
        raise


# TODO: make the [0, 1] option or even be able to set the norm range
def normalize_img(arr):
    """Normalizes images into range of [0, 1] or [-1,1]

    Parameters
    ----------
    arr : ndarray
        Image using values

    Returns
    -------
    ndarray
        The image with values normalized
    """

    arr = arr.astype(float)
    # rconst = 1.0 / 127.5 # uint8 255 midpoint is 127.5 for this
    # rconst = 1.0 / ( abs(np.max(arr)) + abs(np.min(arr)) / 2 )
    rconst = 1.0 / (abs(np.max(arr)) + abs(np.min(arr)) )
    it = np.nditer([arr], flags=['external_loop', 'buffered'], op_flags=['readwrite'])
    with it:
        for x in it:
            # x[...] = ( abs(x) * rconst ) - 1.0
            x[...] = ( abs(x) * rconst)
        return it.operands[0]


# Fast method to find first instance of a value in an array
# Based on https://stackoverflow.com/questions/7632963/numpy-find-first-index-of-value-fast#61117770
def find_first(x):
    idx = x.view(bool).argmax() // x.itemsize
    p_index = np.unravel_index(idx, x.shape)
    return p_index if x[p_index] else -1


class ReadError(Exception):
    pass


class EquivalenceError(Exception):
    pass


class ColorSegmentor:
    """A class used to recognize WaterSort Puzzles in images

    Attributes
    ----------
    image_source : str
        The path to the image to be segmented using color information
    resized_width, resized_height : int, optional
        Width and height of the final resized image. If not set, the image will not be resized
    original_image : array-like
        The image at the path of image_source
    sq : float
        Upper limit on mean squared deviation between distinct colors
    central_tendency : array-like
        Mean, median, and mode for the size of segments
    total_colors : int
        Total number of unique colors found
    segments : array-like
        Array of all labeled segments
    rr : array-like
        Array of region data from labeled segments
    background_label : int
        The label of the background
    background_point : tuple of ints
        The first point in the image corresponding to the background
    """

    def __init__( self, image_source, resized_width=None, resized_height=None ):
        """
        Parameters
        ----------
        image_source : str
            The path to the image to be segmented using color information
        resized_width, resized_height : int, optional
            Width and height of the final resized image. If not set, the image will not be resized
        """
        self.image_source = image_source
        self.resized_width = resized_width
        self.resized_height = resized_height
        self.original_image = []
        # TODO: sq value could be automatically adjusted or be an input parameter
        self.sq = 15.0
        #
        self.central_tendency = []
        self.total_colors = 0
        self.segments = []
        self.rr = []
        self.background_label = -1
        self.background_point = (0, 0)
        self.input_image()

    def input_image( self ):
        """Input an image to be segmented
        If resized attributes were set, then the image be resized.

        Raises
        ------
        ReadError
            The provided source could not be read

        Returns
        -------
        ndarray
            The resized image
        """

        try:
            # Path to file is given
            if isinstance(self.image_source, str):
                ogimg = cv.imread(self.image_source)
                if ogimg is None:
                    raise ReadError("file could not be read, check with os.path.exists()", self.image_source)
            else:
                # Image file is given directly
                ogimg = np.array(self.image_source)
            # Image is not color
            if len(ogimg.shape) <= 2:
                raise ReadError("file is not a color image, check file type and channels", self.image_source)
            # Resize image
            rh, rw = ogimg.shape[:2]
            if self.resized_height is not None:
                rh = self.resized_height
            if self.resized_width is not None:
                rw = self.resized_width
            ogimg = cv.cvtColor(ogimg, cv.COLOR_BGR2RGB)
            ogimg = cv.resize(ogimg, (rw, rh), interpolation=cv.INTER_CUBIC)
            bilati = 15
            ogimg = cv.bilateralFilter(ogimg, bilati, bilati * 2, bilati / 2)
            self.original_image = ogimg
            return ogimg
        except ReadError as err:
            logging.error(err)
            raise

    # TODO: Add a function which makes the image high contrast for easier color based segmentation

    @staticmethod
    def canny_border( img_shift ):
        """Finds edges and borders using Canny Edge detection

        Parameters
        ----------
        img_shift : ndarray
            Image to be used

        Returns
        -------
        ndarray
            The source image, with the detected edges and borders now overlayed
        """

        ogimg = img_shift.copy()
        # Gaussian blur
        bilati = 15
        img_shift = cv.bilateralFilter(img_shift, bilati, bilati * 2, bilati / 2)
        canny = cv.Canny(img_shift, 2, 40, True)  # Canny borders
        kernel = np.ones((3, 3), np.uint8)
        canny = cv.morphologyEx(canny, cv.MORPH_DILATE, kernel)  # make them borders thick
        # Now Gaussian blur to remove noise mostly for the background
        img_shift = cv.GaussianBlur(img_shift, (21, 21), 0)
        canny2 = cv.Canny(img_shift, 2, 35, True)  # These borders are blurrier and noisier
        canny2 = cv.morphologyEx(canny2, cv.MORPH_DILATE, kernel)
        # Merge two sharp and noisy canny images
        canny[canny2 > 10] = 200
        canny = cv.GaussianBlur(canny, (15, 15), 0)
        canny = cv.morphologyEx(canny, cv.MORPH_DILATE, kernel)
        canny = cv.bilateralFilter(canny, bilati, bilati * 2, bilati / 2)
        # Use both local and global thresholding to find the canny edges
        ret, cannygt = cv.threshold(canny, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        cannyat = cv.adaptiveThreshold(canny, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 7, 0)
        cannygt[cannyat > 5] = 255  # The two thresholding methods are merged
        canny = np.invert(cannygt)
        canny = cv.GaussianBlur(canny, (5, 5), 0)
        canny = cv.morphologyEx(canny, cv.MORPH_DILATE, kernel)
        canny = cv.bilateralFilter(canny, bilati, bilati * 2, bilati / 2)
        thresh = 200
        canny[canny < thresh] = 0
        canny[canny > thresh] = 255
        # apply edges as border in the original image
        img_shift = ogimg
        img_shift = cv.bitwise_and(img_shift, img_shift, mask=canny)
        img_shift = cv.bilateralFilter(img_shift, bilati, bilati * 2, bilati / 2)
        return img_shift, canny

    @staticmethod
    def _weight_mean_color( graph, src, dst, n ):
        """Callback to handle merging nodes by recomputing mean color.

        The method expects that the mean color of `dst` is already computed.

        Parameters
        ----------
        graph : RAG
            The graph under consideration.
        src, dst : int
            The vertices in `graph` to be merged.
        n : int
            A neighbor of `src` or `dst` or both.

        Returns
        -------
        data : dict
            A dictionary with the `"weight"` attribute set as the absolute
            difference of the mean color between node `dst` and `n`.
        """

        diff = graph.nodes[dst]['mean color'] - graph.nodes[n]['mean color']
        diff = np.linalg.norm(diff)
        return {'weight': diff}

    @staticmethod
    def merge_mean_color( graph, src, dst ):
        """Callback called before merging two nodes of a mean color distance graph.

        This method computes the mean color of `dst`.

        Parameters
        ----------
        graph : RAG
            The graph under consideration.
        src, dst : int
            The vertices in `graph` to be merged.
        """
        graph.nodes[dst]['total color'] += graph.nodes[src]['total color']
        graph.nodes[dst]['pixel count'] += graph.nodes[src]['pixel count']
        graph.nodes[dst]['mean color'] = (
                graph.nodes[dst]['total color'] / graph.nodes[dst]['pixel count']
        )

    def connected_component_segment(self):
        """Uses connected components to segment the image

        Returns
        -------
        out : ndarray
            Color image in RGB with borders between regions
        labels : ndarray
            Labeled image
        """
        img, canny = self.canny_border(self.original_image)
        # Roughly segment image using connected components with the canny border
        numLabels, labels, ccstats, centroids = cv.connectedComponentsWithStats( canny, 4, cv.CV_32S)
        self.rr = regionprops(labels, cache=True)
        self.rr.sort(key=lambda l: -l.area)
        self.background_label = self.rr[0].label
        bgp = find_first(self.rr[0].image)
        self.background_point = (self.rr[0].bbox[0] + bgp[0], self.rr[0].bbox[1] + bgp[1])
        out = color.label2rgb(labels, img, kind='avg')
        out = segmentation.mark_boundaries(out, labels, (0, 0, 0), mode='thick')  # Make them borders thick
        # LAB colorspace is better for color differentiation
        out = img_as_ubyte(out)
        out = color.rgb2lab(out)
        out = (out + [0, 128, 128]) / [100, 255, 255]
        l_out = out[:, :, 0]  # lightness value to detect the black borders
        b_mask = np.zeros_like(l_out)
        b_mask[l_out <= 0.01] = 1
        background_color = out[self.background_point]
        out[b_mask == 1] = background_color
        labels[b_mask == 1] = self.background_label
        # pltshow(labels)
        # pltshow(out)
        return out, labels

    # TODO: This outputs the color White sometimes, change that
    @staticmethod
    def same_color_labeler( c1, c2, sq_mean_thresh, label=None ):
        """Determines whether two colors are the same.
        Will output the shared color, None if no color is shared, or a label if a label is provided.

        Parameters
        ----------
        c1, c2 : array-like
            The two colors which are compared. These colors should have the same shape and use the same
            color format.
        sq_mean_thresh : float
            The threshold for the square mean comparison. Lower this threshold for more strict color equivalence.
            Raise this threshold for relaxed color equivalence.
        label : int, optional
            The labels to be used instead of color values. Used if an image was produced from labeled regions.
            Otherwise, no labels are assigned and the output uses color values.

        Raises
        ------
        EquivalenceError
            The provided colors were not of the same type

        Returns
        -------
        array-like
            The shared color or the value for white if the colors do not match
        int, optional
            The label corresponding to the shared color or -1 if the colors do not match
        """
        try:
            # TODO: make this actually check color type in the future
            if len(c1) != len(c2):
                raise EquivalenceError("Input colors are of different type", c1.shape, c2.shape)
            # TODO: iterator dtype might need to be changed if color types use int, not sure if numpy can handle that
            if label is None:
                # No labels, use the colors as output
                if square_mean(c1, c2) < sq_mean_thresh:
                    # They are similar colors
                    z = [None] * len(c1)
                    for i in range(len(c1)):
                        z[i] = (c1[i] + c2[i]) / 2  # Return the average of the two colors
                    return z
                else:
                    # TODO: use type of color instead of value type
                    if type(c1[0]) == int:
                        return [255, 255, 255]
                    else:
                        return 1.0
            else:
                # Labels were provided
                if square_mean(c1, c2) < sq_mean_thresh:
                    # They are similar colors
                    return int(label)
                else:
                    return int(-1)

        except EquivalenceError as err:
            logging.error(err)
            raise

    def same_color_mask( self, i1, i2, sq_mean_thresh, color_labels=None ):
        """Creates a mask from two input images where positive values corresponding to where images share color

        Parameters
        ----------
        i1, i2 : ndarray
            The two images which have their color's compared. These images should have the same shape and use the same
            color format.
        sq_mean_thresh : float
            The threshold for the square mean comparison. Lower this threshold for more strict color equivalence.
            Raise this threshold for relaxed color equivalence.
        color_labels : ndarray, optional
            The labels to be used instead of color values. Used if an image was produced from labeled regions.
            Otherwise, no labels are assigned and the output uses color values.

        Raises
        ------
        EquivalenceError
            The provided images were not of the same size and shape

        Returns
        -------
        ndarray of dtype int
            The output mask. Non-zero regions represent the areas where the two images shared colors, with each shared
            color having a unique value.
        """
        try:
            if i1.shape != i2.shape:
                raise EquivalenceError("Input images have different shapes", i1.shape, i2.shape)
            # TODO: maybe add another check to ensure images use the same color system ( HSV, RGB, LAB, etc )
            # Color labels will fill output
            if color_labels is not None:
                # Check that the labels match the images
                if i1.shape[:-1] != color_labels.shape:
                    raise EquivalenceError("The color_labels and image input have different shapes", i1.shape[:-1],
                                           color_labels.shape)
                #
                out_mask = np.zeros_like(color_labels)
                for x in range(i1.shape[0]):
                    for y in range(i1.shape[1]):
                        out_mask[x, y] = self.same_color_labeler(i1[x, y], i2[x, y], sq_mean_thresh, color_labels[x, y])
            else:
                # The colors themselves will fill output
                out_mask = np.zeros_like(i1)
                for x in range(i1.shape[0]):
                    for y in range(i1.shape[1]):
                        out_mask[x, y] = self.same_color_labeler(i1[x, y], i2[x, y], sq_mean_thresh)
            #
            return out_mask

        except EquivalenceError as err:
            logging.error(err)
            raise

    # TODO: make these parameters function inputs
    def region_color_quantization( self, out, c_labels=[], extent_threshold=0.6, solidity_threshold=0.5,
                                   min_region_size=5.0 ):
        """Creates a mask from two input images where positive values corresponding to where the images share color

        Parameters
        ----------
        out : ndarray
            Output from segmentation process
        c_labels : ndarray, optional
            The resulting labels from the same segmentation process as out
        extent_threshold : float, optional
            Regions with extent below threshold are disregarded
            Extent is the Ratio of pixels in the region to pixels in the total bounding box
            Computed as area / (rows * cols)
        solidity_threshold : float, optional
            Regions with solidity below threshold are disregarded
            Solidity is ratio of pixels in the region to pixels of the convex hull image
        min_region_size : float, optional
            The minimum size threshold for a region

        Returns
        -------
        ndarray
            If labels are provided, outputs labels, colored image that has undergone color quantization, regions, and
            background point
            If no labels are provided, outputs a colored image that has undergone color quantization
        """
        # Image processing
        img = cv.GaussianBlur(self.original_image, (21, 21), 0)
        img = img_as_ubyte(img)
        img = color.rgb2lab(img)  # LAB colorspace is better for color differentiation
        img = (img + [0, 128, 128]) / [100, 255, 255]
        #
        out = cv.GaussianBlur(out, (21, 21), 0)  # out should already be LAB colorspace
        if len(c_labels) != 0:
            gg = self.same_color_mask(out, img, 0.35, c_labels)
            self.rr = list(filter(lambda l: l.extent > extent_threshold and l.solidity > solidity_threshold
                                  and l.axis_minor_length > min_region_size and l.axis_major_length > min_region_size,
                                  self.rr))
            axis_major = []
            axis_minor = []
            #region_areas = []
            for x in self.rr:
                axis_minor.append(x.axis_minor_length)
                axis_major.append(x.axis_major_length)
                #region_areas.append(x.area)
                # string_d = "Label: %d, Area: %f, Axis_major_length: %f, Axis_minor_length: %f, Extent: %f, Solidity: %f, Centroids: [%f, %f] " % \
                #           (x.label, x.area, x.axis_major_length, x.axis_minor_length, x.extent, x.solidity, x.centroid[1],
                #            x.centroid[0])
            # The median
            minor_median = np.median(axis_minor)
            major_median = np.median(axis_major)
            # area_median = np.median(region_areas)
            # The median absolute deviation derived from the second order moment ( variance )
            minor_mad = stats.median_abs_deviation(axis_minor)
            major_mad = stats.median_abs_deviation(axis_major)
            # area_mad = stats.median_abs_deviation(region_areas)
            # List of regions which are not the desired color blocks
            noise_regions = []
            ds_data = []
            # Removes regions based on standard deviation from the mean
            # TODO: replace axis length with image shape values
            for x in self.rr:
                ds = (minor_median - x.axis_minor_length) / minor_mad
                if ds < 2.5 and x.axis_major_length > major_median * 1.25:
                    # Possible large block
                    # TODO: deal with large blocks
                    ds += 0.01
                else:
                    ds += math.pow((major_median - x.axis_major_length) / major_mad, 2) * 0.25
                    # ds += math.pow( ( area_median - rr[x].area ) / area_mad, 2)
                ds_data.append((ds, x.label))
            #
            ds_median = np.median(ds_data, axis=0)[0]
            ds_mad = stats.median_abs_deviation(ds_data, axis=0)[0]
            for x in ds_data:
                if x[0] > ds_median + ds_mad * 2:
                    noise_regions.append(x[1])
            # 39 blocks should be right
            region_mask = numpy.isin(gg, noise_regions)
            gg[region_mask] = -1
            gg[gg == -1] = self.background_label
            block_regions = regionprops(gg, cache=True)
            #
            test = cv.cvtColor(self.original_image, cv.COLOR_RGB2HSV_FULL)  # HSV is used for better color sorting
            back_color = test[self.background_point]
            test[gg == self.background_label] = back_color
            out = color.label2rgb(gg, test, kind='avg')
            return gg, out, block_regions, self.background_point
        else:
            gg = self.same_color_mask(out, img, 0.275)
            #pltshow(gg)
            gg = cv.GaussianBlur(gg, (21, 21), 0)
            #pltshow(gg)
            gg = img_as_ubyte(gg)
            #pltshow(gg)
            gg = color.rgb2lab(gg)
            lab_scaled = (gg + [0, 128, 128]) / [100, 255, 255]
            #pltshow(lab_scaled)
            return lab_scaled

    def segment_by_color( self ):
        """Segments the color image using color

        Returns
        -------
        ndarray
            If labels are provided, outputs labels, colored image that has undergone color quantization, and regions
        """
        out, la = self.connected_component_segment()
        return self.region_color_quantization(out, la)


#t = timeit('general_correlation(img, color.deltaE_ciede2000, footprinted)',
#       'from __main__ import general_correlation, img, footprinted; from skimage import color', number=3)
# print(t)

# Testing example
#cs = ColorSegmentor("tests/sortpuz.jpg", 500, 500)
#labels, seg_img, regs, bg = cs.segment_by_color()
#print(len(regs))
#print( regs[2].slice )
#pltshow(labels)
#pltshow(regs[2].image)
#idx = find_first(regs[2].image)
#print(idx)
#pltshow( seg_img[regs[2].slice] )
#print( seg_img[regs[2].slice][idx] )
#pltshow(seg_img)


