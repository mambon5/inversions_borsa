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
    
    while(getline(file,line)) {

        stringstream          lineStream(line);
        string                cell;

        while(getline(lineStream,cell, ','))
        {
            result.push_back(cell);
        }
        // This checks for a trailing comma with no data after it.
        if (!lineStream && cell.empty())
        {
            // If there was a trailing comma then add nothing
        }
    }
    return result;
}

int main() {
    string file = "tickers_5.csv";
    vector<string> ticks;
    ticks = getNextLineAndSplit(file);
    OutputVector(ticks);


}