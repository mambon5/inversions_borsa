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

bool compareStrings(const std::string& str1, const std::string& str2) {
  return str1 < str2;
}

void sortarray(vector<string>& arrayDeStrings) {
    // Ejemplo de un array de strings
    // std::vector<std::string> arrayDeStrings = {"baababa","zzz", "abc", "aaaaa", "xyz", "def"};

    // Ordenar el array utilizando la función compareStrings como criterio de ordenamiento
    std::sort(arrayDeStrings.begin(), arrayDeStrings.end(), compareStrings);

    // Imprimir el array ordenado
    // std::cout << "Array ordenado:" << std::endl;
    // for (const auto& str : arrayDeStrings) {
    //     std::cout << str << " ";
    // }

}

string DownloadWebBody(const string& url) {
    CURL *curl = curl_easy_init();
    string webContent;
    if(curl) {
        CURLcode res;
        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &webContent);
        res = curl_easy_perform(curl);
        curl_easy_cleanup(curl);     
        if (res != CURLE_OK) {
            cerr << "Failed to download web content: " << curl_easy_strerror(res) << endl;
            webContent.clear();
        }   
    }
    
    return webContent;
}

// Define the write callback function
size_t WriteCallback(void* ptr, size_t size, size_t nmemb, std::string* userdata) {
    size_t totalSize = size * nmemb;
    userdata->append(static_cast<char*>(ptr), totalSize);
    return totalSize;
}


// Function to download content from a URL using libcurl
string DownloadWebContent(const string& url) {
    CURL* curl;
    CURLcode res;
    string webContent;

    curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &webContent);
        // cout << "all curl_easy_setopt() done efore easy_perform()" << endl;
        res = curl_easy_perform(curl);
        // cout << "curl_easy_perform() done" << endl;
        if (res != CURLE_OK) {
            cerr << "Failed to download web content: " << curl_easy_strerror(res) << endl;
            webContent.clear();
        }

        curl_easy_cleanup(curl);
    }
    cout << "DownloadWebContent() succeded" << endl;
    return webContent;
}

string getTableStocks(const string& body) {
    size_t pos = 0;
    string table;
    pos = body.find("lookup-table", pos); // start of the table of interest
    size_t endPos = body.find("<span>Next", pos); // end of the table of interest
    if(int(pos) < body.length() && int(endPos) < body.length()){
            table = body.substr(pos, endPos - pos);
    } else{
        cout << "ERROR in getTableStocks(): no stock data found for this url" << endl;
        table = "";
    }
    return table;
}

string DirectWebContent(string& searchGroup, string B, string  C) {
    string baseUrl = "https://finance.yahoo.com/lookup/all?s=";
    string url = baseUrl + searchGroup + "&t=A&b="+B+"&c="+C;
    string webContent = DownloadWebContent(url);
    return webContent;
}

// String filtering for the tickers:
bool StringInVector(const string& ticker, const vector<string>& tickers) {
    // return true if ticker in string vector
    return find(begin(tickers), end(tickers), ticker) != end(tickers);
}

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

void OutputVector( const vector<string>& tickers) {
    for(string str : tickers) {
        cout << str << " - ";
    }
    cout << endl;
}

void OutputVectorInt( const vector<int>& tickers) {
    for(int str : tickers) {
        cout << str << " - ";
    }
    cout << endl;
}

void WriteToFileSimple( const string& output, const string& outputFile) {
    ofstream outFile;
    outFile.open(outputFile, ios_base::out); // append instead of overwrite
    if (!outFile.is_open()) {
        cerr << "Failed to open the output file: " << outputFile << endl;
        return;
    }
    cout << "writing output to ouput file: " << outputFile << endl;
    outFile << output << endl;
    outFile.close();
}

void WriteToFile(const vector<string>& tickers, const string& outputFile) {
    ofstream outFile;
    outFile.open(outputFile, ios_base::app); // append instead of overwrite
    if (!outFile.is_open()) {
        cerr << "Failed to open the output file: " << outputFile << endl;
        return;
    }
    cout << "writing output to ouput file: " << outputFile << endl;
    cout << "there are " << size(tickers) << " tickers:" << endl;
    // int len = sizeof(tickers)/sizeof(tickers[0]);
    // tickers = sort(tickers.begin(), tickers.end());
    // Write tickers to the output file
    for (const string& ticker : tickers) {
        cout << ticker << ", ";
        outFile << ticker << ",";
    }
    outFile.close();
    
}

vector <string> getLastSearchGroup() {
    string line;
    string block;
    string filename = "last_save_ticks.txt";
    string characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    int size = sizeof(characters);
    int first;
    int second;

    ifstream file(filename);
    if (file.is_open()) {
        getline(file, line);
        getline(file, block);
        file.close();
        first = characters.find(line[0]);
        second = characters.find(line[1]);
    } else {
        cout << endl << "ERROR! Could not open file " + filename;
        line = "";
        first = 0;
        second = 0;
    }
    cout << endl << "Opened file for last tickers used, got this: " + line << endl;
    
    string characters1 = characters.substr(first, size - first);
    string characters2 = characters.substr(second, size - second);
    if (block=="") block="0";
    vector <string> vect;
    vect.push_back(line);
    vect.push_back(characters1);
    vect.push_back(characters2);
    vect.push_back(block);
    
    return vect;
}

int getLastFileNumber() {
   DIR *dr;
   struct dirent *en;
   int files = 0;
   int lastn=1;
   dr = opendir("."); //open all directory
   if (dr) {
      while ((en = readdir(dr)) != NULL) {
        //  cout<<" \n"<<en->d_name; //print all directory name
        string filename = en->d_name;
        int n = filename.length();


        if( filename.find(".csv") < n && filename.find("_") <  n) {
            filename = filename.substr(0, n-4);
            string number = filename.substr(filename.find("_")+1, filename.length()-1);
            if(stoi(number) > lastn) lastn = stoi(number);
            files = files + 1;
        }
      }
      closedir(dr); //close all directory
      
   }
   return lastn;
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
