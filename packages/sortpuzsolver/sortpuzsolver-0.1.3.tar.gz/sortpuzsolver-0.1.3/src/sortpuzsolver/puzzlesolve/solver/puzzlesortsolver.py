import logging
import os
import subprocess
import sys
from shutil import which


class ExecError(Exception):
    pass


class Solver:
    """A class used to solve WaterSort Puzzles

    Attributes
    ----------
    setb : int
        The number of blocks per bottle
    setc : int
        The number of colors
    setbn : int
        The number of total bottles
    """

    def __init__( self, setb, setc, setbn ):
        """
        Parameters
        ----------
        setb : int
            The number of blocks per bottle
        setc : int
            The number of colors
        setbn : int
            The number of total bottles
        """

        self.b = setb  # b is the number of blocks in each bottle
        self.c = setc  # c is the number of colors
        self.bn = setbn  # number of bottles

    def ssAlgo( self, lis ):
        """Algorithm which solves the puzzle

        Returns a sequence of moves which solve the puzzle.
        If the puzzle can not be solved, then returns an empty array.

        Parameters
        ----------
        lis : array_like
            The condensed puzzle as a 2D array

        Returns
        -------
        array_like
            The sequence of moves to solve the puzzle
        """
        moves = []
        # TODO: turn the 2D puzzle into 1D array
        # Turn the 2D array into a 1D form
        array_length = len(lis) * len(lis[0])
        puzl = ""
        for r in range(len(lis)):
            for c in range(len(lis[0])):
                puzl += str(lis[r][c]) + ','
        # Run the C++ exec
        dir_path = os.path.dirname(os.path.realpath(__file__))
        comm = ["PuzzleSort", str(self.b), str(self.c), str(self.bn), puzl]
        exx = which(comm[0], path=dir_path)
        try:
            if exx:
                # Not None which means a path was found for the executable
                comm[0] = exx
            else:
                raise ExecError("Executable could not be found, check that it exists", comm[0])
            moves = subprocess.Popen(comm, shell=False, stdout=subprocess.PIPE).stdout.read()
            moves = moves.decode( sys.stdout.encoding ) # STDOut is usually a byte string, so this just decodes it
        except Exception as e:
            logging.error(e)
            raise
        #
        ms = [ x.strip() for x in moves.split(",")]
        return ms

# Test Example:
# tpuz = [[0, 1, 2, 3], [1, 1, 2, 3], [0, 0, 3, 2], [0, 1, 2, 3], [-1, -1, -1, -1], [-1, -1, -1, -1] ]
# tes = Solver(4, 4, 6)
# m = tes.ssAlgo(tpuz)
# print( m )
