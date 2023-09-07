"""
Brute force program that downloads all tickers from yahoo. Takes a few hours to run.
> https://github.com/mlapenna7/yh_symbol_universe/blob/main/yh_get_all_sym.py
"""

import requests
import json
#from array import array
#from datetime import datetime
import logging
from os.path import exists

#from html.parser import HTMLParser
#import time
import string_utils as stru
import numpy as np


logging.basicConfig(level=logging.DEBUG, filename='yh_get_all_sym.log',
    filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

hdr = {
    "authority": "finance.yahoo.com",
    "method": "GET",
    "scheme": "https",
    "accept": "text/html",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "dnt": "1",
    "pragma": "no-cache",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}

def get_counts(body, srch):
    count_beg = body.find('All (')
    #print(count_beg)
    rest = body[count_beg+5: count_beg+20]
    #print( rest)
    count_end = rest.find(')')
    #print(count_end)
    count_all = rest[0: count_end]
    print(logging.info('Counts: ' + srch + ' ' + str(count_all)))
    print("body length: {}".format(len(body)))
    f = open("body.html", "w")
    f.write(body)
    f.close()
    logging.info('Counts: ' + srch + ' ' + str(count_all))

    return count_all

def get_dynamic_webcontent(url):
    """
    If the webpage content is generated using javascrit, then a simple request.get() won't work
    The following code is needed.

    """
    from requests_html import HTMLSession
    s = HTMLSession()
    response = s.get(url)
    response.html.render()

    f = open("body.html", "w")
    f.write(response.text)
    f.close()

    return response

def call_url(url,hdr):
    confirmed = False


    # import urllib.request

    # fp = urllib.request.urlopen("https://finance.yahoo.com/lookup/all?s=AA&t=A&b=0&c=25")
    # mybytes = fp.read()

    # mystr = mybytes.decode("utf8")
    # fp.close()

    # print(mystr)

    while not confirmed:
        try:
            r = get_dynamic_webcontent(url)
            r.raise_for_status()

            #if r.text.find('Something went wrong') > -1:
            #    logging.warning("Found:" + 'Something went wrong')
            #else:
            confirmed = True
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            logging.warning("Http Error:" + str(errh))
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            logging.warning("Error Connecting" + str(errc.status_code))
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", str(errt.status_code))
            logging.warning("Timeout Error:" + errt)
        except requests.exceptions.RequestException as err:
            print("Something Other Request Error", err)
            logging.warning("Something Other Request Error" + str(err.status_code))

        if not confirmed:
            print("Waiting 1 sec to see if problem resolved then retry")
            time.sleep(1)

    #print()
    # special debug
    #f=open("yh_data/yhallsym.txt","w",encoding='UTF-8')
    #f.write( r.text )
    #f.close()
    return r.text

def extreu_tickers(text, posicions):
    tickers = []
    for ind in posicions:
        third_cometes = stru.troba_nessim_repe(text[ind:-1],'"',3)  # necessitem agafar text fins les terceres cometes
        tick = stru.extreu_paraula(text[ind:(ind+third_cometes)])
        if tick.find('=') == -1 and tick.find("^") == -1 and tick not in tickers: # no agafem ni indexos ni errors ni repetim tickers, evidentment
            tickers.append(tick)
    return tickers

def process_one(body, srch, yh_all_sym):
    # {"lookupData":{"start":0,"count":100,"total":100,"documents":
    patro_simbol=' data-symbol="'
    rep_indexs= stru.troba_vals(body,patro_simbol) # positions of all tickers
    ticks = extreu_tickers(body,rep_indexs)
    if len(ticks) == 0:
        print("no more ticks")
        return -1
    print("tickers:")
    print(",".join(ticks))
    f = open(ticks_out_file, "a")
    f.write(",".join(ticks))
    f.close()
    return 0
    

def process_block(body, srch, yh_all_sym, hdr):
    for block in range(0, 9999, 100):
        url = "https://finance.yahoo.com/lookup/all?s=" + srch + "&t=A&b=" + str(block) + "&c=100"
        print('Processing: ', srch, block)
        logging.info('Processing: ' + srch + str(block))
        body = call_url(url,hdr)
        result = process_one(body, srch, yh_all_sym)
        if result == -1:
            break

def set_char_range(start_by="AG", seq = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
    """
    Aquesta funció te com a input dos caràcters que son o una lletra o un dígit, i tornen les lletres i numeros que falten per aribar
    al final de la seqüència. La següència és ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
    """
    ranges = []
    n = len(seq)
    for val in range(0,3) :
        ind = seq.find(start_by[val])
        rang = seq[ind:n]
        rang = list(rang)

        ranges.append(rang)

    return(ranges)

def main():

    # check that file of tickers doesn't exist, otherwise create a new one:
    global ticks_out_file
    seq_caracters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    ind = 1
    ticks_out_file="ticks_{}.csv".format(ind)
    while exists(ticks_out_file): # just iterate until you find a new filename such as ticks_25.csv
        ind+=1
        ticks_out_file="ticks_{}.csv".format(ind)
    
    # ultims tickers que s'han buscat:
    f=open("last_save_ticks.txt","r",encoding='UTF-8')
    Lines = f.readlines()
    ticks_group = Lines[0][0:3] # first two char of first line of the file contain the last used ticks group
    f.close()
    print("last used ticks: {}".format(ticks_group))
    search_set = set_char_range(ticks_group) # els dos rangs de characters que falten per visitar els ticks

    yh_all_sym = {}


    for term_1 in search_set[0]:
        for term_2 in search_set[1]:
            ticks_group = term_1 + term_2
            f=open("last_save_ticks.txt","w",encoding='UTF-8')
            f.write(ticks_group+search_set[2][0])        # now we write down the tick group we were last doing again, just to remeber ^^
            f.close()

            url = "https://www.removepaywall.com/"
            url = "https://finance.yahoo.com/lookup/all?s=" + ticks_group + "&t=A&b=0&c=25"
            print("calling URL: ", url)

            global hdr
            hdr["path"]=url

            body = call_url(url,hdr)
            all_num = get_counts(body, ticks_group)
            print("counts: ")
            print(all_num)
            try:
                all_num = int(all_num)
            except:
                return

            print(ticks_group, 'Total:', all_num)

            if all_num < 9000:
                process_block(body, ticks_group, yh_all_sym,hdr)
            else:
                for term_3 in search_set[2]:
                    ticks_group = term_1 + term_2 + term_3
                    f=open("last_save_ticks.txt","w",encoding='UTF-8')
                    f.write(ticks_group)        # now we write down the tick group we were last doing again, just to remeber ^^
                    f.close()
                    url = "https://finance.yahoo.com/lookup/all?s=" + ticks_group + "&t=A&b=0&c=25"
                    hdr["path"] = url

                    body = call_url(url, hdr)
                    all_num= get_counts(body, ticks_group)
                    all_num = int(all_num)
                    print(ticks_group, 'Total:', all_num)

                    if all_num < 9000:
                        process_block(body, ticks_group, yh_all_sym,hdr)
                    else:
                        for term_4 in search_set:
                            ticks_group = term_1 + term_2 + term_3 + term_4
                            process_block(body, ticks_group, yh_all_sym, hdr)
            
            search_set[2] = seq_caracters # reset the characters for the third letter when loop 2 finishes an iteration
        search_set[1] = seq_caracters # reset the characters for the second letter when first loop finishes an iteration


    f=open("yhallsym.txt","w",encoding='UTF-8')
    # thefile.write. thefile.write('\n'.join(thelist)) or thefile.write(str(item) + "\n")
    f.write(str(yh_all_sym))
    f.close()

if __name__ == '__main__':
    main()
