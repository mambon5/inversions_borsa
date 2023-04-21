import yfinance as yfin

# how to get data from yahoo.
# check this tutorial > https://www.geeksforgeeks.org/get-financial-data-from-yahoo-finance-with-python/

def main():

    ticks = ["ADA-USD",  "RIOT", "005930.KS", "PHIA.AS", "TSLA", "HMC", "LGL", "JUVE.MI", "MANU", "NVDA"]
    print("my stocks:")
    for tick in ticks:
        stock = yfin.Ticker(tick)
        print("stock: {}, last price: {}".format(stock.info["longName"], stock.fast_info.last_price ))


    ticks = ["1810.HK", "GOOG", "BTC-USD"]
    print("\ninterested in stocks:")
    for tick in ticks:
        stock = yfin.Ticker(tick)
        print("stock: {}, last price: {}".format(stock.info["longName"], stock.fast_info.last_price ))
