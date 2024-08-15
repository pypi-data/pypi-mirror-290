#include <iostream>
#include <string>
#include "puzzlesolvelib.h"

int main( int argc, char** argv)
{
    // argc = 5;
    // argv[1] = "4";
    // argv[2] = "4";
    // argv[3] = "6";
    // argv[4] = "0,1,2,3,1,1,2,3,0,0,3,2,0,1,2,3,-1,-1,-1,-1,-1,-1,-1,-1,";
    //
    // argv[1] = "4";
    // argv[2] = "11";
    // argv[3] = "13";
    // argv[4] = "8,8,0,5,9,9,3,7,5,10,10,6,-1,5,4,1,10,8,2,9,1,7,7,0,6,9,3,8,2,6,3,2,6,3,1,4,-1,-1,4,4,7,0,10,2,-1,5,0,1,-1,-1,-1,-1,";
    // Above is for testing
    if ( argc < 3 ) {
        std::cout<<"Error: Insufficient Arguments"<<std::endl;
        return -1;
    }
    int blocks = std::stoi( std::string( argv[1] ) );
    int colors = std::stoi( std::string( argv[2] ) );
    int bottles = std::stoi( std::string( argv[3] ) );
    std::string p ( argv[4] ); // Turn char * to string
    std::vector<int> puzz;
    std::string temp = "";
    for ( auto & c : p ) {
        if ( c != ',' ) {
            temp += c;
        } else {
            puzz.push_back( std::stoi(temp) );
            temp = "";
        }
    }

    Solver ss(blocks,colors,bottles);
    std::string cmm = ss.Solve(puzz);
    if ( cmm.find("Error") != std::string::npos ) {
        // An error occurred
        std::cout<<cmm<<std::endl;
        return -1;
    }
    //
    const char * moves = cmm.c_str();
    int tm = 0;
    for ( auto &cha : cmm ) {
        if ( cha == '>' ) {
            tm++;
        }
    }
    std::cout << "Successfully solved in "<< std::to_string( tm ) << moves << std::endl;
    return tm;
}
