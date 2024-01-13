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
// compile by the command: g++ yh_download_data.cpp -o prova -lcurl
// hint: Yahoo data won't show stocks if the list is greater than 9000. Trick: inspect this 
// list by pieces.
// this guy got a list of all US stock symbols, apparently: https://github.com/rreichel3/US-Stock-Symbols/tree/main
// it is worth checking it out


// to do in the code:
// 1. process by block
// 2.
// 3. 


// int sortarray(const vector<string>& paraules) {
//     // Create a character array "paraules" of size 10 and character value 15.
    
//     // Create another array “arr” of data type string, and the value of '10' is set as a character value.
//     int n = size(paraules);
//     for (int x = 0; x < n; x++) {
//         int m = size(paraules[x]);
//         for (int y = 1; y < m; y++) {
//             const char* par11 = paraules[y].c_str();
//             const char* par22 = paraules[y-1].c_str();
//             int len1 = size(par11);
//             int len2 = size(par22);
//             char par1[len1];
//             char par2[len2];
//             int maxi = max(size(par1), size(par2));
//             char arr[maxi];
//             if (strcmp(par2, par1) > 0) {
//                 strcpy(arr, par2);
//                 strcpy(par2, par1);
//                 strcpy(par1, arr);
//             }

//         }
//     }
//     cout << "\nAlphabetical order of parauless :\n";
//     for (int x = 0; x < 10; x++)
//         cout << paraules[x] << endl;
//     cout << endl;
//     return 0;

// }

vector<string> repeatedTickers = { ""}; // l'iniciem buit, i guardarem els tickers repetits
vector<string> prevTickers = { ""}; // l'iniciem buit, i guardarem els ultims tickers
string lastTicker = "";


void RepeatedTickers(const vector<string>& ticks1, const vector<string>& ticks2) {
    for(string ticker : ticks1) {
        if(StringInVector(ticker, ticks2)) {
            repeatedTickers.push_back(ticker);
        }
    }
}


bool FilterTicker(const string& ticker, const vector<string>& tickers) {
    // next line: tickers doesn't contain an "=" symbol, nor is already in the tickers string, or inthe previous block of tickers (avoiding repeated)
    if (ticker.find('=') != string::npos || StringInVector(ticker, tickers) || 
     StringInVector(ticker, repeatedTickers)) {
        return false; // found
    }        
    return true; // filter passed
}

// function to find the number in the body.html file, saying the number of tickers per block
int getTickersPerBlock(const string& content) {
    size_t pos = 0;
    pos = content.find("All (", pos); 
    size_t endPos = content.find(')', pos); // find the ending ")" after starting at pos of "All ("
    pos = pos + 5; //trimming off the "All (" character positions in the string.
    string counts = content.substr(pos, endPos - pos);
    cout << endl << "Found exactly " + counts + " tickers in the search group to be processed" << endl;
    // count_beg = body.find('All (')
    // rest = body[count_beg+5: count_beg+20]
    // count_end = rest.find(')')
    // count_all = rest[0: count_end]
    return stoi(counts);
}


// Function to extract tickers from web content
vector<string> ExtractTickers(const string& content) {
    vector<string> tickers;
    size_t pos = 0;

    while ((pos = content.find("data-symbol=\"", pos)) != string::npos) {
        pos += 13;  // Move past "data-symbol=\""
        size_t endPos = content.find('\"', pos);
        if (endPos != string::npos) {
            string ticker = content.substr(pos, endPos - pos);
            // Additional filtering logic can be applied here if needed
            if (FilterTicker(ticker, tickers)) {
                tickers.push_back(ticker);
            }            
            pos = endPos + 1;
        }
    }
    return tickers;
}


int CountTickers(const string& body, const string& ticks_group) {
    int count_beg = body.find("All (");
    string rest = body.substr(count_beg+5, count_beg+20);
    int count_end = rest.find(')');
    string count_all = body.substr(count_beg+5, count_end);
    int int_all = stoi(count_all);
    return int_all;
}

void WriteLastCharSet(const string& charset, int block) {    
    string outputFile = "last_save_ticks.txt";
    ofstream outFile;
    outFile.open(outputFile, ios_base::out); // append instead of overwrite
    if (!outFile.is_open()) {
        cerr << "Failed to open the output file: " << outputFile << endl;
        return;
    }
    cout << "writing last used charset "<< charset <<" to file: " << outputFile << endl;
    outFile << charset << endl;   
    outFile << block;
    outFile.close();
}

int ProcessOne(const string url, const string outputFile) {
    cout << "looking for html content from url: " << url << endl;
    string webContent = DownloadWebContent(url);
    cout << "body.html trimmed to just contain table info" << endl;

    string table = getTableStocks(webContent);
    WriteToFileSimple(table, "body2.html");
    vector<string> tickers = ExtractTickers(table);
    if(sizeof(tickers) < 1) {
        cout << "no more ticks" << endl;
        return -1;
    }
    sortarray(tickers);
    
    RepeatedTickers(tickers, prevTickers); // we update the repeated tickers
    cout << "repeated ticker:" << endl;
    OutputVector(repeatedTickers);
    
    prevTickers = tickers;      // we update the last block tickers
    WriteToFile(tickers, outputFile);
    return 0;
}

void ProcessBlock(const string baseUrl, const string searchGroup, const string outputFile, const int& size, const int& fblock=0) {
    for (int block = fblock; block < min(size, 10000); block=block+100) { 
        // we look in blocks of 10 thousand tickers, by chunks of 100
        WriteLastCharSet(searchGroup, block);
        string url = baseUrl + searchGroup + "&t=A&b="+ to_string(block) +"&c=100";
        float percen = block; percen = percen/size*100;
        int tage = percen;
        cout << endl << endl << "Processing: " + searchGroup +  " ("+ to_string(tage) + "%) " + to_string(block)+ "/"+to_string(size)<< endl;
        int result = ProcessOne(url, outputFile);
        if(result == -1) break; //this means there are no more tickers to process in this chunk
    }    
}

int main() {
    string baseUrl = "https://finance.yahoo.com/lookup/all?s=";
    // Generate a sequence of characters (e.g., A, B, ..., Z, 0, 1, ..., 9)
    string characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    cout << "program starts" << endl;
    // Loop through characters to generate URLs
    int n = getLastFileNumber();
    vector<string> vector = getLastSearchGroup();
    string searchgp = vector[0];
    string characters1 = vector[1];
    string characters2 = vector[2];
    int block = stoi(vector[3]);
    cout << "last file used for tickers: " << n << endl;
    string outputFile = "tickers_"+to_string(n+1)+".csv";
    
    for (char char1 : characters1) {
        for (char char2 : characters2) {
            string searchGroup = {char1, char2};
            cout << endl << endl << "processing char group: " << char1 << char2 << ":"<< endl << endl;
            // now get the number of tickers per this searchGroup:
            string webContent = DirectWebContent(searchGroup,  to_string(0), to_string(25));
            int all_count = getTickersPerBlock(webContent);
            ProcessBlock(baseUrl, searchGroup, outputFile, all_count, block);
            block=0;

            // Introduce a delay between requests (e.g., 1 second)
            this_thread::sleep_for(chrono::seconds(1));
        }
    }
   
    cout << "Tickers downloaded and saved to " << outputFile << endl;

    return 0;
}
