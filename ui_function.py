import datetime as dt
import pandas_datareader as web

def get_btc():
    start = dt.datetime(2021,1,1)
    end = dt.datetime.now()
    crypto = 'BTC'
    currency = 'USD'
    price = web.DataReader(f"{crypto}-{currency}", 'yahoo', start, end)
    return price

def get_eth():
    start = dt.datetime(2021,1,1)
    end = dt.datetime.now()
    crypto = 'ETH'
    currency = 'USD'
    price = web.DataReader(f"{crypto}-{currency}", 'yahoo', start, end)
    return price

def get_doge():
    start = dt.datetime(2021,1,1)
    end = dt.datetime.now()
    crypto = 'DOGE'
    currency = 'USD'
    price = web.DataReader(f"{crypto}-{currency}", 'yahoo', start, end)
    return price

