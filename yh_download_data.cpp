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

#include <curl/curl.h>
// compile by the command: g++ -o sms ./src/sms.o -lcurl

// to do in the code:
// 1. process by block
// 2.
// 3. 


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
        cout << "all curl_easy_setopt() done efore easy_perform()" << endl;
        res = curl_easy_perform(curl);
        cout << "curl_easy_perform() done" << endl;
        if (res != CURLE_OK) {
            cerr << "Failed to download web content: " << curl_easy_strerror(res) << endl;
            webContent.clear();
        }

        curl_easy_cleanup(curl);
    }

    return webContent;
}

// String filtering for the tickers:
bool FilterTicker(const string& ticker, const vector<string>& tickers) {
    if (ticker.find('=') != string::npos || find(begin(tickers), end(tickers), ticker) != end(tickers)) {
        return false; // found
    }        
    return true; // filter passed
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

void WriteToFile(const vector<string>& tickers, const string& outputFile) {
    
    ofstream outFile;

    outFile.open(outputFile, ios_base::app); // append instead of overwrite
    if (!outFile.is_open()) {
        cerr << "Failed to open the output file: " << outputFile << endl;
        return;
    }
    cout << "there are " << size(tickers) << " tickers:" << endl;
    // Write tickers to the output file
    for (const string& ticker : tickers) {
        cout << ticker << ", ";
        outFile << ticker << ",";
    }
    outFile.close();
    
}

int CountTickers(const string& body, const string& ticks_group) {
    int count_beg = body.find("All (");
    string rest = body.substr(count_beg+5, count_beg+20);
    int count_end = rest.find(')');
    string count_all = body.substr(count_beg+5, count_end);
    int int_all = stoi(count_all);
    return int_all;
}

void ProcessBlock(const string baseUrl, const string searchGroup) {
    string url = baseUrl + searchGroup + "&t=A&b=0&c=100";

    cout << "looking for html content from url: " << url << endl;
    string webContent = DownloadWebContent(url);
    vector<string> tickers = ExtractTickers(webContent);
    WriteToFile(tickers, outputFile);
}

int main() {
    string baseUrl = "https://finance.yahoo.com/lookup/all?s=";
    string outputFile = "tickers.csv";

    // Generate a sequence of characters (e.g., A, B, ..., Z, 0, 1, ..., 9)
    string characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    cout << "program starts" << endl;
    // Loop through characters to generate URLs
    for (char char1 : characters) {
        for (char char2 : characters) {
            string searchGroup = {char1, char2};
            ProcessBlock(baseUrl, searchGroup)
            

            // Introduce a delay between requests (e.g., 1 second)
            this_thread::sleep_for(chrono::seconds(1));
        }
    }

   
    cout << "Tickers downloaded and saved to " << outputFile << endl;

    return 0;
}
