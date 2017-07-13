import glob, os, os.path, csv, time, threading, schedule
from auth import get_quote
from time import strftime
from datetime import datetime
SP100 = [
    'AAPL',
    'ABBV',
    'ABT',
    'ACN',
    'AGN',
    'AIG',
    'ALL',
    'AMGN',
    'AMZN',
    'AXP',
    'BA',
    'BAC',
    'BIIB',
    'BK',
    'BLK',
    'BMY',
    'BRK.B',
    'C',
    'CAT',
    'CELG',
    'CL',
    'CMCSA',
    'COF',
    'COP',
    'COST',
    'CSCO',
    'CVS',
    'CVX',
    'DD',
    'DHR',
    'DIS',
    'DOW',
    'DUK',
    'EMR',
    'EXC',
    'F',
    'FB',
    'FDX',
    'FOX',
    'FOXA',
    'GD',
    'GE',
    'GILD',
    'GM',
    'GOOG',
    'GOOGL',
    'GS',
    'HAL',
    'HD',
    'HON',
    'IBM',
    'INTC',
    'JNJ',
    'JPM',
    'KHC',
    'KMI',
    'KO',
    'LLY',
    'LMT',
    'LOW',
    'MA',
    'MCD',
    'MDLZ',
    'MDT',
    'MET',
    'MMM',
    'MO',
    'MON',
    'MRK',
    'MS',
    'MSFT',
    'NEE',
    'NKE',
    'ORCL',
    'OXY',
    'PCLN',
    'PEP',
    'PFE',
    'PG',
    'PM',
    'PYPL',
    'QCOM',
    'RTN',
    'SBUX',
    'SLB',
    'SO',
    'SPG',
    'T',
    'TGT',
    'TWX',
    'TXN',
    'UNH',
    'UNP',
    'UPS',
    'USB',
    'UTX',
    'V',
    'VZ',
    'WBA',
    'WFC',
    'WMT',
    'XOM'
]

def update_data(path, ticker):
    try:
        price = get_quote(ticker)['ask_price']
    except:
        price = 'FAILED'
    filename = path + '/' + ticker + '.csv'
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime("%x"), time.strftime("%X"), price])

def update_all(path):
    if not os.path.exists(path):
        os.makedirs(path)
    for ticker in SP100:
        t = threading.Thread(target=update_data, args = (path, ticker))
        t.start()

def job():
    try:
        dow = time.strftime('%w')
        if dow == '0' or dow == '6':
            return
        present = datetime.now()
        today929 = present.replace(hour=9, minute=29,second=0, microsecond=0)
        today1601 = present.replace(hour=16, minute=1,second=0, microsecond=0)
        if present > today929 and present < today1601:
            update_all('SP100_data')

    except:
        pass



if __name__ == '__main__':
    for hour in range(9,17):
        for minute in range(0,60):
            sum_mins = hour * 60 + minute
            if sum_mins >= 568 and sum_mins <= 962:
                if hour == 9:
                    hour_str = '0{}:'.format(hour)
                else:
                    hour_str = '{}:'.format(hour)
                if minute < 10:
                    min_str = '0{}'.format(minute)
                else:
                    min_str = '{}'.format(minute)
                time_str = hour_str + min_str
                schedule.every().day.at(time_str).do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
