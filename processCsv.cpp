using namespace std;
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <cstdlib>
#include <algorithm>
#include <ctime>
#include <chrono>
#include <thread>
#include <string.h>

#include <dirent.h>
#include <sys/types.h>


#include <curl/curl.h>
#include "textProcess.h"

vector<string> getNextLineAndSplit(const string& filename)
{
    vector<string>   result;
    string                line;
    ifstream file(filename);
    int repeated = 0;
    
    while(getline(file,line)) {

        stringstream          lineStream(line);
        string                cell;

        while(getline(lineStream,cell, ','))
        {
            if(!StringInVector(cell, result)) {
                result.push_back(cell);
            }
            else {
                repeated++;
            }
        }
        // This checks for a trailing comma with no data after it.
        if (!lineStream && cell.empty())
        {
            // If there was a trailing comma then add nothing
        }
    }
    cout << to_string(repeated) << " repetitions deleted." << endl;
    return result;
}

int main() {
    cout << "type the name of the file you want to process the tickers: " << endl;
    string file;
    cin >> file;
    vector<string> ticks;
    ticks = getNextLineAndSplit(file);
    // OutputVector(ticks);
    WriteToFile(ticks, "processed_ticks.csv");


}