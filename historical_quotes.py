import requests

API_KEY = 'KRFXDF9PUE9BNKJ6'

def download_data(ticker, begin_date='2018-03-23', end_date='2015-03-23', output_type='csv'):
    res = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}&datatype={}&outputsize=full'.format(ticker, API_KEY, output_type))
    if output_type == 'json':
        return res.json()
    else:
        return res.text.split('\r\n')
    return res
