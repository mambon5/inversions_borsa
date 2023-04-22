"""
how the open price is calculated? > https://finlib.in/open-price-calculated/

"""

import yfinance as yfin
import pandas_datareader as pdr
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

# how to get data from yahoo.
# check this tutorial > https://www.geeksforgeeks.org/get-financial-data-from-yahoo-finance-with-python/


def historic_yfin(ticker, period="7d", interval="1m", start=None, end=None):
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

    # 
    stock= yfin.Ticker(ticker)
    if start == None :
        stock_historical = stock.history(period=period, interval=interval)
    else:
        stock_historical = stock.history(start=start, end=end, interval=interval)

    print(stock_historical)
    plot_onecol(stock_historical, ticker, "Open", period, interval)
    plot_onecol(stock_historical, ticker, "Close", period, interval)
    #plot_onecol(stock_historical, ticker, "High", period, interval)
    #plot_onecol(stock_historical, ticker, "Low", period, interval)
    return stock_historical


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
    

def main(period="7d", interval="1m"):

    ticks = ["ADA-USD",  "RIOT", "005930.KS", "PHIA.AS", "TSLA", "HMC", "LGL", "JUVE.MI", "MANU", "NVDA"]
    print("my stocks:")
    for tick in ticks:
        stock = yfin.Ticker(tick)
        print("stock: {}, last price: {}".format(stock.info["longName"], stock.fast_info.last_price ))
        historic_yfin(tick, period=period, interval=interval, start=None, end=None)



    ticks = ["1810.HK", "GOOG", "BTC-USD"]
    print("\ninterested in stocks:")
    for tick in ticks:
        stock = yfin.Ticker(tick)
        print("stock: {}, last price: {}".format(stock.info["longName"], stock.fast_info.last_price ))
        historic_yfin(tick, period=period, interval=interval, start=None, end=None)

