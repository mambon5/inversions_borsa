"""
Brute force program that downloads all tickers from yahoo. Takes a few hours to run.
> https://github.com/mlapenna7/yh_symbol_universe/blob/main/yh_get_all_sym.py


Checking why python program eats up so much memory:

1. Rried to fix issue deleting all logging > didn't work
2. Tried to inspect usingthe @profile function who eats the memory > couldnt find anything
3. Tried to list at each loop iteration all the global/local variables and their size > they all stay the same
4. Maybe its because of the print to the terminal I do? I closed the terminal to see if RAM decreased, it didn't. That is also not the issue
5.
6.

"""
import gc
import requests
import json
#from array import array
#from datetime import datetime
import logging
from os.path import exists

#from html.parser import HTMLParser
import time
import string_utils as stru
import memory_utils as memu
import numpy as np

### tracing memory consumption to find why program breaks:
# from memory_profiler import profile


logging.basicConfig(level=logging.DEBUG, filename='yh_get_all_sym.log',
    filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

# getting ammount of tickers found following the filter criteria: ...All (65) asdasdfasdf<dev>
def get_counts(body, srch):
    count_beg = body.find('All (')
    #print(count_beg)
    rest = body[count_beg+5: count_beg+20]
    #print( rest)
    count_end = rest.find(')')
    #print(count_end)
    count_all = rest[0: count_end]
    # print(logging.info('Counts: ' + srch + ' ' + str(count_all)))
    # f = open("body.html", "w")
    # f.write(body)
    # f.close()
    # logging.info('Counts: ' + srch + ' ' + str(count_all))

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
    # text = response.text
    # f = open("body.html", "w")
    # f.write(text)
    # f.close()
    # del f
    del s
    # del response
    gc.collect()
    return response

# instantiating the decorator
# @profile
# code for which memory has to
# be monitored
###
def call_url(url):
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
            body = r.text
            # if r.text.find('Something went wrong') > -1:
            #    logging.warning("Found:" + 'Something went wrong')
            # else:
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
    del r
    gc.collect()
    return body

def extreu_tickers(text, posicions):
    tickers = []
    for ind in posicions:
        third_cometes = stru.troba_nessim_repe(text[ind:-1],'"',3)  # necessitem agafar text fins les terceres cometes
        tick = stru.extreu_paraula(text[ind:(ind+third_cometes)])
        if tick.find('=') == -1 and tick.find("^") == -1 and tick not in tickers: # no agafem ni indexos ni errors ni repetim tickers, evidentment
            tickers.append(tick)
    return tickers

def process_one(body):
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
    

def process_block(body, srch):
    global turns # moves before function exits
    for block in range(0, 9999, 100):
        # if turns < 1:# delete this for production, just using to watch memory usage
        #     break
        # else:
        #     turns -=1
        url = "https://finance.yahoo.com/lookup/all?s=" + srch + "&t=A&b=" + str(block) + "&c=100"
        print('Processing: ', srch, block)
        # logging.info('Processing: ' + srch + str(block))
        body = call_url(url)
        result = process_one(body)
        # print("global vars:")
        # print(memu.get_vars_size(list(globals().items()))) # print size of all variables in python script
        # print("local vars 1:")
        # print(memu.get_vars_size(list(locals().items()))) # print size of all variables in python script
        if result == -1:
            break
        del body
        collected = gc.collect() # trying to free RAM memory
        print("Garbage collector: collected %d objects." % (collected))

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
    global turns # moves before function exits
    turns=2
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
    del f
    print("last used ticks: {}".format(ticks_group))
    search_set = set_char_range(ticks_group) # els dos rangs de characters que falten per visitar els ticks

    for term_1 in search_set[0]:
        for term_2 in search_set[1]:
            # if turns < 1: # delete this for production, just using it to watch memory usage
            #     return
            ticks_group = term_1 + term_2
            f=open("last_save_ticks.txt","w",encoding='UTF-8')
            f.write(ticks_group+search_set[2][0])        # now we write down the tick group we were last doing again, just to remeber ^^
            f.close()
            del f
            url = "https://www.removepaywall.com/"
            url = "https://finance.yahoo.com/lookup/all?s=" + ticks_group + "&t=A&b=0&c=25"
            print("calling URL: ", url)

            # hdr["path"]=url

            body = call_url(url)
            all_num = get_counts(body, ticks_group)
            print("counts: ")
            print(all_num)
            try:
                all_num = int(all_num)
            except:
                return

            print(ticks_group, 'Total:', all_num)

            if all_num < 9000:
                process_block(body, ticks_group)
                # print("local vars 2:")
                # print(memu.get_vars_size(list(locals().items()))) # print size of all variables in python script
                del body
            else:
                for term_3 in search_set[2]:
                    ticks_group = term_1 + term_2 + term_3
                    f=open("last_save_ticks.txt","w",encoding='UTF-8')
                    f.write(ticks_group)        # now we write down the tick group we were last doing again, just to remeber ^^
                    f.close()
                    del f
                    url = "https://finance.yahoo.com/lookup/all?s=" + ticks_group + "&t=A&b=0&c=25"
                    # hdr["path"] = url

                    body = call_url(url)
                    all_num= get_counts(body, ticks_group)
                    all_num = int(all_num)
                    print(ticks_group, 'Total:', all_num)

                    if all_num < 9000:
                        process_block(body, ticks_group)
                        del body
                    else:
                        for term_4 in seq_caracters:
                            ticks_group = term_1 + term_2 + term_3 + term_4
                            process_block(body, ticks_group)
                            del body
                    
                                                        
            
            search_set[2] = seq_caracters # reset the characters for the third letter when loop 2 finishes an iteration

            
        search_set[1] = seq_caracters # reset the characters for the second letter when first loop finishes an iteration


    f=open("yhallsym.txt","w",encoding='UTF-8')
    # thefile.write. thefile.write('\n'.join(thelist)) or thefile.write(str(item) + "\n")
    f.write(str(yh_all_sym))
    f.close()

if __name__ == '__main__':
    main()
