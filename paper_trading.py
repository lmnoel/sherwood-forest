import time
import requests
import csv

def get_quote(ticker):

    r = requests.get('https://api.robinhood.com/quotes/{}/'.format(ticker))

    return r.json()

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
    execute()
