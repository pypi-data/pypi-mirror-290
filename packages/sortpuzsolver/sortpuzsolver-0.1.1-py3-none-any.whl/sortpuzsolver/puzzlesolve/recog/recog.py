import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

import sortpuzsolver.colorseg.colorsegmentor as segs
import sortpuzsolver.puzzlesolve.puzzlesortsolver as pss


def sh( im ):
    cv.imshow('window', im)
    cv.waitKey(0)


def pltshow( im ):
    plt.subplot(122), plt.imshow(im, cmap='gray')
    plt.title('Show'), plt.xticks([]), plt.yticks([])
    plt.show()


def abdiff( l1, l2 ):
    return abs(l1 - l2)


# Inspired by Leland Hepworth's numpy array slicing at
# https://stackoverflow.com/questions/24398708/slicing-a-numpy-array-along-a-dynamically-specified-axis#64436208
def array_slice(a, axis, start, end, step=1):
    """Slices multidimensional arrays

    Parameters
    ----------
    a : ndarray
        The array
    axis : int
        Axis to perform the slicing operation
    start : int
        Starting position, inclusive
    end : int
        Ending position, exclusive
    step : int
        Step size or stride length

    Returns
    -------
    ndarray
        Slice of the array returned as a view
    """
    return a[(slice(None),) * (axis % a.ndim) + (slice(start, end, step),)]


class ReadError(Exception):
    pass


class PuzzleRecognizer:
    """A class used to recognize WaterSort Puzzles in images

    Attributes
    ----------
    max_kernel_length : int
        The max size of the width and height of the kernel used in convolution processes
    bpb : int
        The number of blocks per bottle
    empt_bots : int
        The number of empty bottles
    sq : float
        The upper limit on mean squared deviation between distinct colors
    fluid_median : int
        The median height of blocks in the image
    total_colors : int
        The total number of unique colors in the puzzle
    bottles : array_like
        List of the bottles with their individual blocks
    """

    def __init__( self, max_kernel_length, bpb, empt_bots=2 ):
        """
        Parameters
        ----------
        max_kernel_length : int
            The max size of the width and height of the kernel used in convolution processes
        bpb : int
            The number of blocks per bottle
        empt_bots : int, optional
            The number of empty bottles. Default value of 2
        """
        self.MAX_KERNEL_LENGTH = int(max_kernel_length)
        self.blocks_per_bottle = int(bpb) # blocks per bottle # 4
        self.empty_bottles = int(empt_bots)
        # TODO: sq value could be automatically adjusted
        self.sq = 30.0
        #
        self.fluid_median = 0
        self.total_colors = 0
        self.bottles = []
        self.draw_pos = []

    @staticmethod
    def hues_in_range( h1, h2, r):
        """Find hues that are within a given range r

        Parameters
        ----------
        h1, h2 : [Hue, Saturation, Value]
            HSV Colors, uses OpenCV hues with range [0,255]
        r : int
            Range, the size of the range between hues

        Returns
        -------
        bool
            Whether the hue of the two colors are within range
        """

        # Hues function like a wheel with range 0-255
        smaller = 0
        larger = 0
        hrange = 255
        if h1 <= h2:
            smaller = h1
            larger = h2
        else:
            smaller = h2
            larger = h1

        hh = hrange + smaller - larger
        gg = larger - smaller
        cc = float( min(hh, gg) )
        return cc < r

    # TODO: Segments have interesting attributes such as central moments which might prove more beneficial than just
    #   width or height
    @staticmethod
    def calc_central_tendencies( seg_sizes ):
        """Find the mean, median, and mode of the size of segments

        Parameters
        ----------
        seg_sizes : array-like
            List of the segment sizes in format: [ [width, height], ... ]

        Returns
        -------
        array-like
            A list containing the mean, median, and mode for the width, height, and area of segments
        """

        cl = len(seg_sizes)
        seg_sizes.sort( key=lambda l: l[0] )
        if cl % 2 == 0:
            medw = float( ( seg_sizes[int( cl / 2)] + seg_sizes[int( (cl + 1) / 2)] ) / 2 )
        else:
            medw = float(seg_sizes[int( cl / 2)])
        seg_sizes.sort(key=lambda l: l[1])
        if cl % 2 == 0:
            medh = float( ( seg_sizes[int( cl / 2)] + seg_sizes[int( (cl + 1) / 2)] ) / 2 )
        else:
            medh = float(seg_sizes[int( cl / 2)])

        meanw, meanh, meana = 0
        modew = []
        mw = [0, 1]
        modeh = []
        mh = [0, 1]
        modea = []
        ma = [0, 1]
        mode_bucket_size = 5 # The range of values that are sorted together when determining mode
        mode_area_range = 10 # The range of area values that are sorted together when determining mode
        for seg in seg_sizes:
            meanw = meanw + seg[0]
            meanh = meanh + seg[1]
            #
            a = seg[0] * seg[1]
            meana = meana + a
            #
            if len( modew ) == 0:
                modew.append( [seg[0], 1] )
                modeh.append( [seg[1], 1] )
                modea.append( [a, 1] )
                mw[0] = seg[0]
                mh[0] = seg[1]
                ma[0] = a
            else:
                # Width
                ff = False
                for x in modew:
                    if x[0] - mode_bucket_size <= seg[0] <= x[0] + mode_bucket_size:
                        x[1] += 1
                        if x[1] > mw[1]:
                            mw[1] = x[1]
                            mw[0] = x[0]
                        ff = True
                if not ff:
                    modew.append( [seg[0], 1] )
                # Height
                ff = False
                for x in modeh:
                    if x[0] - mode_bucket_size <= seg[1] <= x[0] + mode_bucket_size:
                        x[1] += 1
                        if x[1] > mh[1]:
                            mh[1] = x[1]
                            mh[0] = x[0]
                        ff = True
                if not ff:
                    modeh.append([seg[1], 1])
                # Area
                ff = False
                for x in modea:
                    if x[0] - mode_area_range <= a <= x[0] + mode_area_range:
                        x[1] += 1
                        if x[1] > ma[1]:
                            ma[1] = x[1]
                            ma[0] = x[0]
                        ff = True
                if not ff:
                    modea.append([seg[0], 1])
        #
        modea.sort(key=lambda l: l[0])
        if len(modea) % 2 == 0:
            meda = float( ( modea[int( len(modea) / 2)] + modea[int( (len(modea) + 1) / 2)] ) / 2 )
        else:
            meda = float( modea[int( len(modea) / 2)])
        #
        ct = [ [ meanw/cl, medw, mw[0] ], [ meanh/cl, medh, mh[0] ], [ meana/cl, meda, ma[0] ] ]
        return ct

    def find_blocks( self, labels, seg_img, regs, background_point ):
        """Finds the blocks of the labels

        Parameters
        ----------
        labels : ndarray
            Labeled image
        seg_img : ndarray
            Segmented image in HSV
        regs : array-like
            List of regions corresponding to the labels
        background_point : tuple of int
            Point corresponding to the background
        
        Returns
        -------
        array_like
            The list of all color segments, list of unique colors found within the list of color segments, 
            and list of segments of unusual shape
        """

        # fluid list
        fluids_temp = []
        back_color = seg_img[background_point]
        background_label = labels[background_point]
        #
        for i in range(len(regs)):
            # preview[labels == i] = ccolors[i % len(ccolors)]
            temp_img = seg_img[regs[i].slice]
            cl = segs.find_first(regs[i].image)
            fluids_temp.append([i, temp_img[cl],
                                np.array(regs[i].centroid).astype(int), temp_img.shape[0]] )

        # Sort by height which is the rows in shape
        fluids_temp.sort(key=lambda l: l[len(l) - 1])
        # TODO: median and a simple range are cool, but there are probably better statistical means to find the fluids
        #  / gems or whatever that need to be sorted
        self.fluid_median = fluids_temp[ len(fluids_temp) // 2 ][3] # // for integer
        fmbuff = 10
        fluids_count = 0
        unique_colors = []
        fluid_colors = []
        bigguns = []
        l1 = []
        l2 = []
        ucnum = 0
        found = False
        # Find the unique colors
        # pltshow(seg_img)
        for f in fluids_temp:
            if f[3] > self.fluid_median - fmbuff:
                l1 = f[1]
                # Color is similar to the background
                # print( l1 )
                # print( back_color )
                if self.hues_in_range(l1[0], back_color[0], 10) and segs.square_mean(l1[1:], back_color[1:]) < self.sq:
                    # print( regs[f[0]].label )
                    continue
                fluids_count += 1
                found = False
                for un in range(len(unique_colors)):
                    # if the difference between the colors is small enough group the colors together
                    if self.hues_in_range(l1[0], unique_colors[un][0], 10) and \
                            segs.square_mean(l1[1:], unique_colors[un][1:]) < self.sq:
                        ucnum = un
                        fluid_colors.append( [fluids_count, ucnum, regs[f[0]].bbox[0], f[2][1], f[3]] )
                        found = True
                        break

                if not found:
                    unique_colors.append( l1 )
                    ucnum = len(unique_colors) - 1
                    fluid_colors.append([fluids_count, ucnum, regs[f[0]].bbox[0], f[2][1], f[3]])
                # print(regs[f[0]].label, ucnum)
                # TODO: after identifying the labels that are too long, maybe split them up or change them somehow
                # TODO: actually the algorithm does not care about block size
                if f[3] > self.fluid_median + fmbuff:
                    # print("Big one")
                    bigguns.append([fluids_count, fluids_count, fluids_count, ucnum, f[3]])
                    # print(f)

        #
        fluid_colors.sort( key=lambda l: l[2] )
        # pltshow(labels)
        return fluid_colors, unique_colors, bigguns

    def block_format( self, fluid_colors, unique_colors, bigguns ):
        """Formats the blocks from the image into a form the solver recognizes

        Parameters
        ----------
        fluid_colors : array_like
            List of color segments
        unique_colors : array_like
            List of unique colors found within the list of color segments
        bigguns : array_like
            List of color segments deemed unusual

        Returns
        -------
        array_like
            2D array in the puzzle format, [ [1,1,1,1], [2,2,2,2], ..., [n,n,n,n] ]
        """
        
        dd = 6.0 # This number determines the max distance difference ( dd ) for x coords to be grouped together
        xbucket = []
        # Turn the float x coords into integers
        # Also give blocks that are close in x position the same x value
        #   to make it easier to put them in bottles.
        for un in fluid_colors:
            found = False
            unx = un[3]
            for xb in xbucket:
                if abdiff( unx, float(xb)) < dd:
                    un[3] = xb
                    found = True

            if not found:
                xbucket.append( int(unx) )
                un[3] = int(unx)
        # Sort by x and y coordinates
        fluid_colors.sort( key=lambda l: (l[3], l[2]) )
        hbuff = self.fluid_median + 7 # height buffer based on median height
        last_x = fluid_colors[0][3]
        last_y = fluid_colors[0][2]
        last_h = fluid_colors[0][4]
        bottles = [ [fluid_colors[0][1]] ]
        #
        for bigs in bigguns:
            if bigs[0] == fluid_colors[0][0]:
                bigs[1] = 0
                bigs[2] = 0
        #
        uc = [0] * (len(unique_colors))
        uc[fluid_colors[0][1]] += 1
        boti = 0
        # TODO: error checking also this ONLY works if only colors are labeled and no other extraneous stuff
        # Go through found colors and put them into bottles based on x and y coordinates
        for i in range(1, len(fluid_colors) ):
            cx = fluid_colors[i][3]
            cy = fluid_colors[i][2]
            ch = fluid_colors[i][4]
            if last_x == cx:
                if last_y + last_h + hbuff >= cy:
                    bottles[boti].append(fluid_colors[i][1])
                    uc[fluid_colors[i][1]] += 1
                    last_y = cy
                    last_h = ch
                    for bigs in bigguns:
                        if bigs[0] == fluid_colors[i][0]:
                            bigs[1] = boti
                            bigs[2] = len(bottles[boti]) - 1 # TODO
                else:
                    # Position of last block in previous bottle
                    self.draw_pos.append([last_x - int(self.fluid_median / 2), last_y + self.fluid_median])
                    # New Bottle
                    bottles.append([fluid_colors[i][1]])
                    uc[fluid_colors[i][1]] += 1
                    last_y = cy
                    last_h = ch
                    boti += 1
                    for bigs in bigguns:
                        if bigs[0] == fluid_colors[i][0]:
                            bigs[1] = boti
                            bigs[2] = len(bottles[boti]) - 1 # TODO
            else:
                self.draw_pos.append([last_x - int(self.fluid_median / 2), last_y + self.fluid_median])
                # New bottle
                bottles.append([fluid_colors[i][1]])
                uc[fluid_colors[i][1]] += 1
                last_x = cx
                last_y = cy
                last_h = ch
                boti += 1
                for bigs in bigguns:
                    if bigs[0] == fluid_colors[i][0]:
                        bigs[1] = boti
                        bigs[2] = len(bottles[boti]) - 1 # TODO
        #
        self.draw_pos.append([last_x - int(self.fluid_median / 2), last_y + self.fluid_median])

        # Handles formating and ensures the number of blocks is right
        ccn = [self.blocks_per_bottle] * len(xbucket)
        bigguns.sort( key=lambda l: -(l[3])) # sorts so the biggest get priority
        formatted_right = False
        while not formatted_right:
            formatted_right = True
            for b in bigguns:
                ccn[b[3]] = self.blocks_per_bottle - uc[b[3]]
                if ccn[b[3]] > 0:
                    if len(bottles[b[1]]) < self.blocks_per_bottle:
                        bottles[b[1]].insert(b[2], b[3])
                        uc[b[3]] += 1
                    else: # TODO: have this else do something else
                        bottles[b[1]].insert(b[2], b[3])
                        uc[b[3]] += 1
                        print("ERROR: biggun detected, but bottle full.")
                    formatted_right = False


        # Checks to add empty bottles which might not be visible, but can be calculated to exist
        cdiff = len(unique_colors) - len(bottles)
        for cd in range(abs(cdiff), self.empty_bottles, 1):
            bottles.append(list())

        for b in bottles:
            blen = self.blocks_per_bottle - len(b)
            for bb in range(blen):
                b.insert(0, -1)

        #
        self.total_colors = len(unique_colors)
        #
        self.bottles = bottles
        return bottles

    def bottle_check( self ):
        """Checks the bottles state to ensure it is safe to pass to the solver

        Returns
        -------
        bool
            Whether the bottles state is formatted correctly and is possible to solve
        """
        check_l = [0] * self.total_colors
        for b in self.bottles:
            for chl in b:
                if chl != -1:
                    check_l[chl] += 1

        for ss in range(len(check_l)):
            if check_l[ss] != self.blocks_per_bottle:
                print("Incorrect amount of blocks for color: ", ss)

        # print("Blocks per Bottle: " + str(self.blocks_per_bottle) + " Colors: " + str(self.total_colors) +
        # " Bottles: " + str(len(self.bottles)))
        # Checks that the blocks and bottles makes sense
        # TODO: reference the waterpuzzle paper to check the below actually finds valid puzzles
        if self.total_colors != ( len(self.bottles) - self.empty_bottles ):
            print("ERROR: number of unique colors does not match given number of blocks and bottles.")
            return False
        else:
            return True

    def draw_bottle_nums( self, img ):
        """Draws the bottle numbers used in the move list over the corresponding bottle.

        Parameters
        ----------
        imgsrc : ndarray
            The image used to solve the puzzle

        Returns
        -------
        ndarray
            The image with the drawn numbers on top
        """
        draw_img = img.copy()
        self.draw_pos.sort( key=lambda l: (l[0], l[1]) )
        font = cv.FONT_HERSHEY_SIMPLEX
        for p in range( len(self.draw_pos) ):
            cv.putText(draw_img, str(p), (self.draw_pos[p][0], self.draw_pos[p][1]), font, 1, (255, 255, 255), 2, cv.LINE_AA)
        return draw_img

    def quick_out( self, imgsrc ):
        """Handles all the intermediate functions calls for ease of use

        Creates a ColorSegmentor object, instantiates it, and finds segmentations.
        Then calls find_blocks, block_format, and bottle_check
        
        Parameters
        ----------
        imgsrc : str
            Path to image

        Returns
        -------
        array_like
            The list of moves which solve the inputted puzzle
        ndarray
            The original image with the bottle numbers overlaid on top of the corresponding bottles
        """
        cs = segs.ColorSegmentor(imgsrc, 500, 500)
        labels, seg_img, regs, bg = cs.segment_by_color()
        #pltshow(labels)
        #pltshow(seg_img)
        fluid_colors, unique_colors, bigguns = self.find_blocks( labels, seg_img, regs, bg )
        self.block_format( fluid_colors, unique_colors, bigguns )
        self.bottle_check()
        csolver = pss.Solver(self.blocks_per_bottle, self.total_colors, len(self.bottles))
        pm = csolver.ssAlgo(self.bottles)
        dimg = self.draw_bottle_nums( cs.input_image() )
        dimg = cv.imencode('.jpg', dimg)[1].tobytes()
        return pm, dimg


# TODO: Testing Example
#  tester = PuzzleRecognizer( 31, 4, 2)
#  moves, mimg = tester.quick_out("../../../../tests/SortExample.png")
#  print(moves)

