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


int main() {
    cout << "type the name of the file you want to process the tickers: " << endl;
    string file;
    cin >> file;
    vector<string> ticks;
    ticks = CsvFilterDuplicates(file);
    // OutputVector(ticks);
    WriteToFile(ticks, "processed_ticks.csv");


}