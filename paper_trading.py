import time
import requests
import csv
from auth import *

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
    def __init__(self, ticker, share_price, num_shares):
        self.ticker = ticker
        self.acquisition_price = float(share_price)
        self.acquisition_time = time.time()
        self.acquisition_cost = float(share_price) * num_shares
        self.num_shares = int(num_shares)
        return

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

def execute():
    history = []
    current_hr, current_min, current_sec = get_time()
    while current_hr <= 16 and current_min <= 30:
        data = get_quote('SPY')
        price = data['ask_price']
        trade_time = data['updated_at']
        val = ((current_hr,current_min, current_sec),price, trade_time)
        history.append(val)
        if current_min == 30:
            report(history)
        time.sleep(60)
        current_hr, current_min, current_sec = get_time()

def report(history):
    with open('report.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile,delimiter=',')
        for row in history:
            writer.writerow(row)


if __name__ == '__main__':
    aapl = Stock('AAPL',120,10)
    msft = Stock('MSFT',70,15)
    p = Portfolio()
    p.add_stock(aapl)
    p.add_stock(msft)
    p.add_cash(40)

    #execute()
