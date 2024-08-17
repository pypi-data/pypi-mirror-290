#ifndef PUZZLESOLVELIB_H_INCLUDED
#define PUZZLESOLVELIB_H_INCLUDED

// from collections import deque
#include <unordered_set>
#include <algorithm> // TODO: Delete if not used
#include <vector>
#include <deque>
#include <functional>
#include <string>
#include <bitset>
#include <utility>
#include <stdexcept>


// Turns a flattened 1D array of the puzzle into a 2D format
std::vector<std::vector<int>> arr_to_vec(std::vector<int>& arr, size_t size_x, size_t size_y)
{
    // Check size constraints
    if ( size_x * size_y > arr.size() ) {
        throw std::invalid_argument( "Error: provided container size does not match the provided size given by size_x and size_y" );
    }
    //
    std::vector<int> temp (size_y, 0); //
    std::vector< std::vector<int> > l (size_x, temp); // Make vector of same dimension filled with 0
    size_t cc = 0;
    // TODO: This function assumes that size_x and size_y are valid and accurately represent the array dimensions
    for ( size_t i=0; i < size_x; i++ ) {
        for ( size_t j=0; j < size_y; j++ ) {
            l[i][j] = arr[cc];
            cc++;
        }
    }
    return l;
}

// Sorts the blocks in condensed formated puzzles.
bool format_sort( std::pair< int, std::bitset<8> > l1, std::pair< int, std::bitset<8> > l2 ) {
    if ( std::get<0>(l1) < std::get<0>(l2) ) {
        return true;
    }
    else if ( std::get<0>(l1) == std::get<0>(l2) ) {
        std::bitset<8> botmask (0x1F); // bottle mask // 00011111
        int botn1 = int( ( botmask & std::get<1>(l1) ).to_ulong() ); // The bottle of l1
        int botn2 = int( ( botmask & std::get<1>(l2) ).to_ulong() ); // The bottle of l2
        if ( botn1 < botn2 ) {
            return true;
        }
        else if ( botn1 == botn2 ) {
            std::bitset<8> posmask (0xE0); // position inside the bottle mask // 11100000
            // If l1 is above l2 in the bottle
            if ( ( (posmask & std::get<1>(l1) ) >> 5).to_ulong() < ( (posmask & std::get<1>(l2) ) >> 5).to_ulong() ) {
                return true;
            }
            else {
                return false;
            }
        }
        else {
            return false;
        }
    }
    else {
        return false;
    }
}

//!  A class used to solve WaterSort Puzzles
/*!
    Each instance of this class solves puzzles of the format provided when instantiated.
    To solve puzzles of a different formats a new solver needs to be instantiated.
*/
class Solver {
    public:

        //! A constructor.
        /*!
            Sets the expected puzzle format to solve
            \param setb number of blocks per bottle.
            \param setc total number of colors.
            \param setbn total number of bottles.
        */
        Solver( int setb, int setc, int setbn );

        //! Function to solve a provided puzzle state.
        /*!
            Takes in a flattened puzzle format and solves the puzzle.
            \param puzzle flattened array with values of -1 representing empty space and values greater than 0 representing blocks.
            \return set of moves to solve the puzzle as a sequence of moves separated by commas.
        */
        const char * Solve ( std::vector<int>& puzzle );


    protected:
        //! Function to condense puzzle states into a memory efficient format.
        /*!
            \param 2D puzzle state.
            \return condensed array with each bitset item representing a single colored block.
        */
        std::vector<std::bitset<8>> format_in( std::vector<std::vector<int>>& lis );

        //! Function to expand condensed puzzle states into workable 2D format.
        /*!
            \param condensed puzzle state.
            \return 2D vector of type int representing the puzzle state.
        */
        std::vector< std::vector<int> > format_out( std::vector< std::bitset<8> >& lis );

        //! Function to hash puzzle states.
        /*!
            Gives each puzzle state a unique value.
            \param condensed puzzle state.
            \return unique string that can be used in hashing.
        */
        std::string ps_hash( std::vector< std::bitset<8> >& lis );

        //! Function to count the number of contiguous blocks of colors in the puzzle state.
        /*!
            \param condensed puzzle state.
            \return number of blocks.
        */
        int blocks( std::vector< std::bitset<8> >& lis );

    private:
        // Variables
        int num_blocks = 0; //!< Number of non-empty blocks in the puzzle. Contiguous blocks of a single color are counted as one block.
        int num_colors = 0; //!< Number of total colors in the puzzle
        int num_bottles = 0; //!< Number of total bottles in the puzzle
        std::unordered_set<std::string> hashset; //!< Set containing all puzzles states already explored by the algorithm.

        //! Function to generate the possible moves that can be made in a puzzle state.
        /*!
            \param condensed puzzle state.
            \return A list of all valid moves from the provided puzzle state.
        */
        std::vector< std::pair<std::vector< std::vector<int> >, std::string > > genMoves( std::vector< std::bitset<8> >& lists );

        // TODO: Make this more efficient
        //! Function to find the moves that solve a given puzzle.
        /*!
            Uses a modified form of A* search to find the optimal move.
            If the puzzle is complex enough or large enough, a suboptimal solution can be returned as a compute saving expense.
            \param condensed puzzle state.
            \return sequence of moves to solve the puzzle with each move separated by a comma.
        */
        std::string ssAlgo( std::vector<std::vector<int>>& lis );
};

Solver::Solver( int setb, int setc, int setbn ) {
    this->num_blocks = setb; // b is the number of blocks in each bottle
    this->num_colors = setc; // c is the number of colors
    this->num_bottles = setbn; // number of bottles
}

const char * Solver::Solve ( std::vector<int>& puzzle ) {
    if ( puzzle.size() != this->num_bottles * this->num_blocks ) {
        return "Error: puzzle is not in line with provided number of bottles and blocks";
    }
    std::vector<std::vector<int>> lis;
    std::string mm = "Error: null or none returned by ssAlgo()";

    try {
        lis = arr_to_vec( puzzle, this->num_bottles, this->num_blocks );
        mm = this->ssAlgo(lis);
    }
    catch ( const std::exception& e ) {
        mm = "Error: " + std::string( e.what() );
    }
    return mm.c_str();
}

// TODO: Use a single bitset with the first 5 bits representing one of 32 possible colors.
//  Then for each possible color generate a possible mask
//  Instead of a list of bitsets it could just be one large bitset
std::vector<std::bitset<8>> Solver::format_in( std::vector<std::vector<int>>& lis ){
    std::vector< std::pair< int, std::bitset<8> > > hol;
    std::bitset<8> temper;
    int rc = 0;
    int cc = 0;
    for ( auto &r : lis ) {
        for ( auto &c : r ) {
            // skip empty spaces which are -1
            if (c == -1) {
                cc += 1;
                continue;
            }
            // bottle position has 32 options or 5 digits
            // position within the bottle has 8 or 3 digits, so these two fit within uint8
            temper = ( rc | cc << 5 );
            hol.push_back( std::pair<int, std::bitset<8>> (c,temper) ); // map sorts by color code
            cc += 1;
        }
        rc += 1;
        cc = 0;
    }

    std::vector< std::bitset<8> > ll (hol.size());
    std::sort(hol.begin(), hol.end(), format_sort);
    for ( int i=0; i<hol.size(); i++ ) {
        ll[i] = std::get<1>(hol[i]);
    }
    return ll;
}

std::vector< std::vector<int> > Solver::format_out( std::vector< std::bitset<8> >& lis ){
    std::vector<int> tneg (this->num_blocks, -1); // Blocks per bottle are filled with -1
    std::vector< std::vector<int> > flis (this->num_bottles, tneg); // make the number of bottles and fill each with blocks of -1
    int gg = this->num_blocks;
    int p = 0;
    int botn = 0;
    int ff = -1;
    std::bitset<8> posmask (0xE0); // position inside the bottle mask // 11100000
    std::bitset<8> botmask (0x1F); // bottle mask // 00011111
    for ( auto &l : lis ) {
        // since the condensed form is sorted by color this allows the extraction of color info
        if ( gg == this->num_blocks) {
            ff += 1;
            gg = 0;
        }
        //
        p = int( ((posmask & l) >> 5).to_ulong() );
        botn = int( (botmask & l).to_ulong() );
        flis[botn][p] = ff;
        gg += 1;
    }

    return flis;
}

std::string Solver::ps_hash( std::vector< std::bitset<8> >& lis ){
    std::string s = "";
    for( auto const& x : lis ){
        s += std::to_string( x.to_ulong() );
    }
    return s;
}

int Solver::blocks( std::vector< std::bitset<8> >& lis ){
    int nb = 0;
    int gg = this->num_blocks;
    int p = 0;
    int botn = 0;
    int prev_p = -1;
    int prev_botn = -1;
    int ff = 0;
    std::bitset<8> posmask (0xE0); // position inside the bottle mask // 11100000
    std::bitset<8> botmask (0x1F); // bottle mask // 00011111
    for ( auto &l : lis ) {
        // since the condensed form is sorted by color this allows the extraction of color info
        if ( gg == this->num_blocks ) {
            ff += 1;
            gg = 0;
        }
        //
        p = int( ((posmask & l) >> 5).to_ulong() );
        botn = int( (botmask & l).to_ulong() );
        if ( botn == prev_botn ) {
            if ( prev_p + 1 != p ) {
                nb++;
            }
        }
        else {
            nb++;
        }
        // print("TEST: " + str(l) + ", " + std::to_string(botn) + ", " + std::to_string(p) + ", " + std::to_string(ff))
        prev_p = p;
        prev_botn = botn;
        gg += 1;
    }

    return nb;
}

std::vector< std::pair<std::vector< std::vector<int> >, std::string > > Solver::genMoves( std::vector< std::bitset<8> >& lists ) {
    std::vector< std::vector<int> > lis = this->format_out(lists);
    std::vector< std::pair<std::vector< std::vector<int> >, std::string > > pmoves;
    std::vector< std::vector<int> > m;
    int gtop = 0; // giving bottle top layer color
    int rtop = 0; // receiving bottle top layer color
    int gs = 0; // giving bottle top layer position
    int rs = 0; // receiving bottle top layer position
    int temptop = 0;
    // temtops = [];
    bool deadend = true;
    std::string move_history;
    //
    // Look at the top ( ie the first to not equal -1 ) block and its color and store it in tops ( by block this also includes the squares below so if the block has 2-3 then include that )
    // then go through the list of tops and find which empty spaces ( ie the -1 spots in the original lis ) where it could fit ( the block below is the same color )
    // Store the generated states in pmoves
    for ( int i=0; i<lis.size(); i++ ) {
        gs = 0;
        gtop = -1;
        while ( gtop == -1 && gs < this->num_blocks ) {
            if ( lis[i][gs] != -1 ) {
                gtop = lis[i][gs];
                break;
            }
            gs += 1;
        }
        //
        if (gtop == -1) {
            continue;
        }
        //
        temptop = gs;
        for ( int j=0; j<lis.size(); j++ ) {
            // giver and receiver bottles are the same so skip
            if (j == i) {
                continue;
            }
            // The bottle is full and no blocks can be moved into it
            if (lis[j][0] != -1) {
                continue;
            }
            //
            rs = 1;
            rtop = -1;
            gs = temptop;
            while (rtop == -1 && rs < this->num_blocks) {
                if (lis[j][rs] != -1) {
                    rtop = lis[j][rs];
                    break;
                }
                rs += 1;
            }
            // Tops have same color or bottle is empty
            if (rtop == gtop || rtop == -1) {
                m = lis; // Copy puzzle state
                move_history = std::to_string(i) + "->" + std::to_string(j);
                for ( int k=rs-1; k >= 0; k-- ) {
                    m[i][gs] = -1;
                    m[j][k] = gtop;
                    gs = gs + 1;
                    if ( gs < this->num_blocks ) {
                        if (m[i][gs] != gtop) {
                            break;
                        }
                    }
                    else {
                        break;
                    }
                }
                // TODO: Finish this heuristic which gets rid of dead end moves
                //deadend = True
                //for rrr in m:
                //    for ccc in range(len(rrr)):
                //        if rrr[ccc] != -1:
                //            temtops.append([rrr[ccc], ccc])
                //            break
                //        if ccc == len(rrr) - 1:
                //            if rrr[ccc] == -1:
                //                deadend = False
                //                break
                //    if not deadend:
                //        break
                //if deadend:
                //    temtops.sort( key=lambda l: l[0] )
                //    for ctt in range(1, len(temtops)):
                //        if temtops[ctt-1][0] == temtops[ctt][0]:
                //            if temtops[ctt-1][1] != temtops[ctt][1]:
                //                deadend = False
                //                break
                ////
                //if not deadend:
                //    pmoves.append( [m, move_history.copy()] )
                pmoves.push_back( std::make_pair( m, move_history ) );
            }
        }
    }
    //
    return pmoves;
}

//TODO: Make this more efficient, especially by decreasing memory usage and using Multi-threading
std::string Solver::ssAlgo( std::vector<std::vector<int>>& lis ){
    std::string moves;
    //
    int nblocks = 0;
    //
    std::deque< std::pair< std::vector<std::bitset<8>>, std::string> > hque;
    hque.push_back( std::make_pair( this->format_in(lis), std::string("")) );
    this->hashset.insert( this->ps_hash( std::get<0>(hque.front() ) ) );
    int counter = 0;
    std::pair< std::vector<std::bitset<8>>, std::string> lholder;
    std::string temper;
    std::string tempertemp;
    std::vector<std::bitset<8>> formatedholder;
    std::vector< std::pair<std::vector< std::vector<int> >, std::string > > p;
    int search_limit = 50000;
    while ( !hque.empty() ) {
        counter++;
        lholder = hque.front();
        temper = std::get<1>(lholder);
        moves = std::get<1>(lholder);
        nblocks = this->blocks(std::get<0>( lholder ) );
        // if all colors are one block a solution has been found
        if ( nblocks == this->num_colors ) {
            return moves;
        }
        //
        hque.pop_front();
        p = this->genMoves( std::get<0>( lholder ) );
        for ( auto &m : p ) {
            tempertemp = std::get<1>(m);
            tempertemp = temper + ", " + tempertemp;
            formatedholder = this->format_in(std::get<0>(m));
            // Compute the hash to avoid adding states that are already in the queue
            // Only go if the insertion of the hash was successful
            if ( std::get<1>( this->hashset.insert( this->ps_hash(formatedholder) ) ) ) {
                if (this->blocks(formatedholder) < nblocks) {
                    hque.push_front( std::make_pair(formatedholder, tempertemp ) );
                }
                else {
                    // If the search space is too large
                    // only looks at currently known positions which may be suboptimal or fail to find a solution
                    if ( hque.size() < search_limit ) {
                        hque.push_back( std::make_pair(formatedholder, tempertemp ) );
                    }
                }
            }
        }
        //
        if ( counter >= search_limit * 4 ) {
            std::cout<<"Error: Search limit reached."<<std::endl;
            break;
        }
    }
    // Return the moves taken in order
    return "Error: No solution found.";
}

#endif // PUZZLESOLVELIB_H_INCLUDED
