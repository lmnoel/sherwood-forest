import requests
import csv
import os

API_KEY = 'KRFXDF9PUE9BNKJ6'
tickers = ['SPY', 'GLD'] #if you want to downlaod multiple files at once

def download_data(ticker, begin_date='2018-03-23', end_date='2015-03-23', output_type='csv'):
    res = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}&datatype={}&outputsize=full'.format(ticker, API_KEY, output_type))
    if output_type == 'json':
        return res.json()
    else:
        return res.text.split('\r\n')
    return res


def run():

    if not os.path.exists('quotes/'):
        os.mkdir('quotes')
    for ticker in tickers:
        res = download_data(ticker=ticker)
        filename = 'quotes/{}_data.csv'.format(ticker)
        with open(filename, 'w') as csvwriter:
            writer = csv.writer(csvwriter)
            for line in res:
                writer.writerow(line.split(','))

if __name__ == '__main__':
    run()