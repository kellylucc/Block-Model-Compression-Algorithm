#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <map>
#include <cctype>
#include <unordered_map>

using namespace std;

string stringMaker(int x, int y, int z, int xSize, int ySize, int zSize, unordered_map<char, string> tagTableMap, char symbol) {
    string compressed = "";
    string xc = to_string(x);
    string yc = to_string(y);
    string zc = to_string(z);

    string xS = to_string(xSize);
    string yS = to_string(ySize);
    string zS = to_string(zSize);

    compressed = compressed + xc + "," + yc + "," + zc + "," + xS + "," + yS + "," + zS + "," + tagTableMap[symbol] + "\n";
    return compressed;

}

string LZW2D(string xyzData[2], int xCount, int yCount, int zCount, int y, int z, unordered_map<char, string> tagTableMap) {

    string compressed = "";

    for(int x = 0; x < xyzData[0].length()-1; x+=2) {
        
        // 2x2 Block
        //  C0  C1
        //  C2  C3
        char C0 = xyzData[0][x];
        char C1 = xyzData[0][x+1];
        char C2 = xyzData[1][x];
        char C3 = xyzData[1][x+1];

        // Case: 2x2 block
        if(C0 == C1 && C0 == C2 && C0 == C3) {
            compressed += stringMaker(x, y, z, 2, 2, 1, tagTableMap, C0);
        }

        // Case: 2x1 Block top half
        else if(C0 == C1) {
            compressed += stringMaker(x, y, z, 2, 1, 1, tagTableMap, C0);

            // Case: 2x1 Block bottom half
            if(C2 == C3)
                compressed += stringMaker(x, y+1, z, 2, 1, 1, tagTableMap, C2);
            // Case: bottom half not equal
            else {
                compressed += stringMaker(x, y+1, z, 1, 1, 1, tagTableMap, C2);
                compressed += stringMaker(x+1, y+1, z, 1, 1, 1, tagTableMap, C3);
            }
        }
        // Case: 2x1 Block bottom half
        else if(C2 == C3) {
            compressed += stringMaker(x, y+1, z, 2, 1, 1, tagTableMap, C2);
            // Case: 2x1 Block top half
            if(C0 == C1)
                compressed += stringMaker(x, y, z, 2, 1, 1, tagTableMap, C0);
            // Case: top half not equal
            else {
                compressed += stringMaker(x, y, z, 1, 1, 1, tagTableMap, C0);
                compressed += stringMaker(x+1, y, z, 1, 1, 1, tagTableMap, C1);
            }
        }
        // Case: 1x2 Block left half
        else if(C0 == C2) {
            compressed += stringMaker(x, y, z, 1, 2, 1, tagTableMap, C0);

            // Case: 2x1 Block right half
            if(C1 == C3)
                compressed += stringMaker(x+1, y, z, 1, 2, 1, tagTableMap, C1);
            // Case: right half not equal
            else {
                compressed += stringMaker(x+1, y, z, 1, 1, 1, tagTableMap, C1);
                compressed += stringMaker(x+1, y+1, z, 1, 1, 1, tagTableMap, C3);
            }
        }
        // Case: 1x2 Block right half
        else if(C1 == C3) {
            compressed += stringMaker(x+1, y, z, 1, 2, 1, tagTableMap, C1);

            // Case: 2x1 Block left half
            if(C0 == C2)
                compressed += stringMaker(x, y, z, 1, 2, 1, tagTableMap, C0);
            // Case: left half not equal
            else {
                compressed += stringMaker(x, y, z, 1, 1, 1, tagTableMap, C0);
                compressed += stringMaker(x, y+1, z, 1, 1, 1, tagTableMap, C2);
            }
        }
        // Case: no matches
        else {
            compressed += stringMaker(x, y, z, 1, 1, 1, tagTableMap, C0);
            compressed += stringMaker(x+1, y, z, 1, 1, 1, tagTableMap, C1);
            compressed += stringMaker(x, y+1, z, 1, 1, 1, tagTableMap, C2);
            compressed += stringMaker(x+1, y+1, z, 1, 1, 1, tagTableMap, C3);
        }

    }
    return compressed;
}

bool onlySpaces(string &line) {
    
    for (int i = 0; i<line.length(); i++) {
        if (!isspace(line[i])) {
            return false;
        }
    }
    return true;
}

int main() { 
    // Process input 
    int bx, by, bz;
    int px, py, pz;
    char comma;
    cin >> bx >> comma >> by >> comma >> bz >> comma >> px >> comma >> py >> comma >> pz >> ws;
    cout<<bx<<" "<<by<<" "<<bz<<" "<<px<<" "<<py<<" "<<pz<<endl;
    string line;
    char symbol;
    string label;
    unordered_map<char, string> tag_table;

    while (true) {
        getline(cin, line);
        if (line.empty() || onlySpaces(line)) {
            break;
        }
        stringstream line_stream (line);
        line_stream >> symbol >> comma >> label;
        tag_table[symbol] = label;
        // cout<<"symbol: "<<symbol<<" label: "<<label<<endl;
    }

    string doubleLine[2];
    vector<string> outputList;
    
    bool keepReading = true;
    int empty = 0;
    int y = 0;
    int z = 0;
    int i = 0;
    while(keepReading) {
        
        getline(cin, line);

        // If a line with only spaces is encountered, it is the start of a new layer (z + 1)        
        if(onlySpaces(line)){
            
            empty++;
            z++;  
            y = 0;
            i = 0;
        } 
        else {
            empty = 0;
            // since we are processing two lines at a time, if i is even then we set the first element of doubleLine to the current line
            if(i % 2 == 0) {
                doubleLine[0] = line;
            } else {
                // if i is odd, then we set the second element in the doubleLine array to the current line, and call the algorithm
                doubleLine[1] = line;
                cout << LZW2D(doubleLine, bx, by, bz, y, z, tag_table);
                y += 2;
                
            }

            i++;
        }
        
        // if two empty lines in a row are encountered, we have finished processing the input
        if(empty == 2) keepReading = false;

    }
    return 0;
}

