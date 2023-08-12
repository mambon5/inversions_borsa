"""
how the open price is calculated? > https://finlib.in/open-price-calculated/

"""

import yfinance as yfin
import pandas_datareader as pdr
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# how to get data from yahoo.
# check this tutorial > https://www.geeksforgeeks.org/get-financial-data-from-yahoo-finance-with-python/


def ecdf(data) :
    """
    define empyrical CDF function, where you can input a number
    
    :param data: must be an array of numbers   
    """
    x = lambda a : len([1 for i in data if i <= a])/len(data)
    return x

def download_historic_yfin(ticker, period="1mo", interval="1d", start=None, end=None):
    """
    Getting historical stock data using the yfinance library.
        - Remember we now use this aapl ticker object for almost everything- calling various methods on it.
        - To get the historical data we want to use the history() method, which is the most 'complicated' method in the yfinance library.
        - Check this guide on how to use it > https://algotrading101.com/learn/yfinance-guide/ 

        :param start: must be of format: "2020-06-02"
        :param end: must be of format: "2020-06-02"
        :param period: must be of format '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'
        :param interval: valid intervals include: '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'

    """
    stock= yfin.Ticker(ticker)
    if start == None :
        stock_historical = stock.history(period=period, interval=interval)
    else:
        stock_historical = stock.history(start=start, end=end, interval=interval)

    #print(stock_historical)
    #plot_onecol(stock_historical, ticker, "Open", period, interval)
    #plot_onecol(stock_historical, ticker, "Close", period, interval)
    #plot_onecol(stock_historical, ticker, "High", period, interval)
    #plot_onecol(stock_historical, ticker, "Low", period, interval)
    return stock_historical

def browse_values(historic, type=None):
    """
    Get the whole data set into a list of values, if a specific type is selected.
    For instance, the "close" values, or the "open" values of that stock value.
    """
    if type != None:
        y = pd.to_numeric(historic[type]) 
        return y
    print("alert: no value type selected (either 'Close' or 'Open')")
    return 0

def historic_pandas():
    """
    historical yahoo finance data.
    """
    ticker = "AAPL"
    start = dt.datetime(2019, 1, 1)
    end = dt.datetime(2020, 12, 31)
    
    data = pdr.get_data_yahoo(ticker, start, end)
    
    print(data)

def plot_values(value, time=None,  title="", pandas_values=False):
    if pandas_values:
            plt.plot(value)
    else:
        if len(time) == len(value):        
            # plotting the points 
            plt.plot(time,value)        
        else:
            print("error, time and values have different dimensions!")
    # naming the x axis
    plt.xlabel('t - time')
    # naming the y axis
    plt.ylabel('y - values')
    
    # giving a title to my graph
    plt.title('Stock {}'.format(title))

    # Rotates X-Axis Ticks by 45-degrees
    plt.xticks(rotation = 75) 
    # save plot
    plt.savefig('plots/plot_{}.png'.format(title))

    # function to show the plot
    # plt.show()
    plt.close()


def plot_onecol(historic, tickname="", type="Open", period="", interval=""):
    y = pd.to_numeric(historic[type])    
    plot_values(y, title="{} {} values per: {} int: {}".format(tickname, type, period, interval), pandas_values=True)
    

def simple_slope(historic, type="Open") :
    y = pd.to_numeric(historic[type])    
    slope = y[-1]  - y[0]
    return slope

def linreg_slope(historic, type="Open") :
    y = pd.to_numeric(historic[type])   
    x = range(0,len(y))
    res = stats.linregress(x,y)
    # x= map(lambda a: a.strftime("%d/%m/%y"), x)
    return [y, res]

def plot_linregress(x, y, res):
    plt.plot(x, y, 'o', label='original data')
    plt.plot(x, res.intercept + res.slope*x, 'r', label='fitted line')
    plt.legend()
    plt.show()

def do_linreg():
    historic = historic_yfin("RIOT", period="5d", interval="1d")
    linreg = linreg_slope(historic, type="Open")
    y = linreg[0]
    res = linreg[1]
    print("linear regression slope: {}".format(res.slope))
    print("lin reg percentual slope: {}%".format( round(100*res.slope/y[0],2 )))
    plot_linregress(range(0,len(y)), y, res)

def main(period="1mo", interval="1d"):

    ticks = ["ADA-USD",  "RIOT", "005930.KS", "PHIA.AS", "TSLA", "HMC", "LGL", "JUVE.MI", "MANU", "NVDA",
             "1810.HK", "GOOG", "BTC-USD"]
    ticks = ["RIOT"]
    print("my stocks:")
    for tick in ticks:
        stock = yfin.Ticker(tick)
        print("stock: {}, last price: {}".format(stock.info["longName"], stock.fast_info.last_price ))
        stock_historical = download_historic_yfin(tick, period=period, interval=interval, 
                                                  start=None, end=None)
        print("Historical")
        print(stock_historical)
        type = "Close"
        stock_y = browse_values(stock_historical, type=type)
        print("Printing {} values from {}".format(type, tick))
        print(stock_y)
        #plot_onecol(stock_historical, tick, "Open", period, interval)
        #plot_onecol(stock_historical, tick, "Close", period, interval)
        
        print("1 - ECDF, printing how high up is this value: ")
        fun = ecdf(stock_y)
        print(fun(stock_y[-1]))

        return stock_y



