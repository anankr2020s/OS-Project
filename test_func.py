import datetime as dt
import pandas_datareader as web

def get_btc_usd():
    start = dt.datetime(2021,1,1)
    end = dt.datetime.now()
    crypto = 'BTC'
    currency = 'USD'
    price = web.DataReader(f"{crypto}-{currency}", 'yahoo', start, end)
    return price
print(get_btc_usd())

def get_btc_thb():
    btc_thb = []
    start = dt.datetime(2021,1,1)
    end = dt.datetime.now()
    crypto = 'BTC'
    currency = 'USD'
    price = web.DataReader(f"{crypto}-{currency}", 'yahoo', start, end)
    for i in price.index:
        btc_thb.append(price.loc[i]['Close']*32.5)
    return btc_thb



