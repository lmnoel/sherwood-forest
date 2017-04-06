import time
import requests
import csv

def get_quote(ticker):

    r = requests.get('https://api.robinhood.com/quotes/{}/'.format(ticker))

    return r.json()

def netfonds_quote(ticker):
    time_str = time.strftime("%y%m%d")
    r = requests.get('')



def get_time():

    current_hr = time.gmtime().tm_hour - 4
    current_min = time.gmtime().tm_min
    current_sec = time.gmtime().tm_sec

    return current_hr, current_min, current_sec

def execute():
    history = []
    current_hr, current_min, current_sec = get_time()
    count = 0
    while count < 100000000000000:
        count += 1
        data = get_quote('SPY')
        ask_price = data['ask_price']
        bid_price = data['bid_price']
        last_trade_price = data['last_trade_price']
        updated_time = data['updated_at']
        val = ((current_hr,current_min, current_sec),ask_price, bid_price,last_trade_price,updated_time)
        history.append(val)
        current_hr, current_min, current_sec = get_time()
    report(history)

def report(history):
    with open('res_test_report.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile,delimiter=',')
        for row in history:
            writer.writerow(row)


if __name__ == '__main__':
    execute()
