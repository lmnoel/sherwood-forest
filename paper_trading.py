import time
import requests
import csv
from auth import *


IND_FUND_MAP = {
    'Energy' : 'IYE',
    'Infrastructure' : 'PAVE',
    'Finance' : 'IYF'
}

COUNT_FUND_MAP = {
    'china' : 'CYB',
    'mexico' : 'FXM',
    'dollar' : 'USDU'
}

class Portfolio(object):
    '''
    '''
    def __init__(self):
        self.ledger = []
        self.cash = 0

    def add_stock(self, stock):
        self.ledger.append(stock)

    def holdings(self):
        return self.ledger

    def cash(self):
        return self.cash

    def add_cash(self, cash):
        self.cash += cash
        return self.cash

    def remove_cash(self, cash):
        self.cash -= cash
        return self.cash

    def equity(self):
        rv = 0
        for stock in self.holdings():
            rv += stock.current_value()
        return rv

    def total_value(self):
        cash = self.cash
        equity = self.equity()

        return cash + equity

    def total_return(self):
        rv = 0
        for stock in self.holdings():
            rv += stock.current_return()

        return rv

    def liquidate(self):
        rv = 0
        for stock in self.holdings():
            rv += stock.sell()
        self.add_cash(rv)
        self.ledger = []
        return rv

class Stock(object):
    '''
    '''
    def __init__(self, ticker, share_price, linked_eo, num_shares=0):
        self.ticker = ticker
        self.open_price = float(share_price)
        self.open_time = time.strftime("%c")
        self.acquisition_cost = float(share_price) * num_shares
        self.num_shares = int(num_shares)
        self.linked_eo = linked_eo
        self.net_gain = 0

    def current_price(self):
        quote = get_quote(self.ticker)
        current_price = quote['ask_price']

        return float(current_price)

    def current_value(self):
        price = self.current_price()
        return price * self.num_shares


    def current_return(self):
        current_value = self.current_value()
        return current_value - self.acquisition_cost

    def sell(self):
        #temp code, for paper trading
        return self.current_value()

def get_time():

    current_hr = time.gmtime().tm_hour - 4
    current_min = time.gmtime().tm_min
    current_sec = time.gmtime().tm_sec

    return current_hr, current_min, current_sec


def market_is_open():
    hr, min_, sec = get_time()
    cum_mins = 60 * hr + min_ + sec / 60
    dow = time.strftime("%w")
    if dow == 0 or dow == 6:
        return False
    if cum_mins > 990 or cum_mins < 510:
        return False
    return True


def report(history):
    with open('report.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile,delimiter=',')
        for row in history:
            writer.writerow(row)

def trade(order):
    ticker = None
    keyword = order.cat
    if not market_is_open() or abs(rating) < 0.3:
        return None
    if order.mexico_mentions > 2:
        if rating < -0.3:
            ticker = COUNT_FUND_MAP['dollar']
        else:
            ticker = COUNT_FUND_MAP['mexico']
    elif order.china_mentions > 2:
        if rating < -0.3:
            ticker = COUNT_FUND_MAP['dollar']
        else:
            ticker = COUNT_FUND_MAP['china']
    elif keyword in IND_FUND_MAP.keys():
        ticker = IND_FUND_MAP[keyword]
    elif keyword == 'Trade':
        if rating > .3:
            ticker = 'USDU'
    if ticker:
        print('ticker is:',ticker)
        current_price = get_quote(ticker)['ask_price']
        position = Stock(ticker, current_price, order)
        return position
    else:
        return None
        
