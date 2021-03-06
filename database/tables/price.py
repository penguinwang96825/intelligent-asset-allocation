from database.database import db

import pickle
import requests
from bs4 import BeautifulSoup
import datetime as dt
from tqdm import tqdm
import pandas as pd
import pandas_datareader.data as web
import yfinance as yf

class StockPrice(db.Model):
    __tablename__ = 'price'

    id_ = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    high = db.Column(db.Float(precision=4))
    low = db.Column(db.Float(precision=4))
    open_ = db.Column(db.Float(precision=4))
    close = db.Column(db.Float(precision=4))
    vol = db.Column(db.Integer)
    adj_close = db.Column(db.Float(precision=4))
    comp = db.Column(db.String(20))


    def __init__(self, date, high, low, open_, close, vol, adj_close, comp):
        self.date = date
        self.high = high
        self.low = low
        self.open_ = open_
        self.close = close
        self.vol = vol
        self.adj_close = adj_close
        self.comp = comp

    def __repr__(self):
        return "Stock Price ('{}', '{}', '{}', '{}')".format(self.date, self.vol, self.close, self.comp)

    @classmethod
    def find_all_by_query(cls, comp):
        return cls.query.filter_by(comp=comp).all()


def save_history_stock_price_to_db():
    """
        The goal of the function is read the list of S&P500 from wiki (a pickle file).
        Then, get the history stock price through Yahoo Finance API.
        The function just need to execute one time at first.
    """

    sp_99 = []
    with open('./database/tables/ticker_name.txt', 'r') as f0:
        lines = f0.readlines()
        for l in lines:
            c = l.split('\t')
            c[1] = c[1].replace('\n','')
            c[1] = c[1].replace(' ','')
            sp_99.append(c[1])
    # add S&P 500 index
    sp_99.append('^GSPC')
    # yf.pdr_override()
    print(len(sp_99))
    # get the history stock price
    start = dt.datetime(2012, 1, 1)
    end = dt.datetime(2020, 8, 5)

    for ticker in tqdm(sp_99, desc = 'get company price'):
        stock_list = []
        try:
            df = web.DataReader(ticker, 'yahoo', start, end)
            print(ticker ,'found')
            # df = web.get_data_yahoo(ticker, start=start, end = end)
            df.reset_index(inplace=True)

            for index, row in df.iterrows():
                date = row['Date'].to_pydatetime().date()
                stock_list.append(StockPrice(date, row['High'], row['Low'], row['Open'], \
                                                row['Close'], row['Volume'], row['Adj Close'], ticker))
            
        except:
            print(ticker + ' not found')
            print('Get Nothing.')

        # db.session.add_all(stock_list)
        # db.session.commit()


def update_daily_stock_price(sp500_file):
    with open(sp500_file, 'rb') as f:
        tickers = pickle.load(f)
    
    date = str(dt.datetime.now().date()).split('-')
    
    start = dt.datetime(int(date[0]), int(date[1]), int(date[2])-1)
    end = dt.datetime(int(date[0]), int(date[1]), int(date[2]))

    stock_list = []
    for ticker in tqdm(tickers):
        try:
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.reset_index(inplace=True)
            stock_data = df.values[-1]

            date = stock_data[0].to_pydatetime()
            stock_list.append(StockPrice(date, stock_data[1], stock_data[2], stock_data[3], stock_data[4], stock_data[5], stock_data[6], ticker))
        
        except:
            print('Get Nothing.')
            
    db.session.add_all(stock_list)
    db.session.commit()