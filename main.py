#This file runs the code needed for EO trading

###TODO:
#Create a function to backanalyze eo's
#create a scheduler for liquidation
#rewordk csv's to handle all data
#exception catching https://schedule.readthedocs.io/en/stable/faq.html#what-if-my-task-throws-an-exception

import time
from time import strftime
import schedule
from auth import *
from wh_scraper import *
import random
import subprocess
from paper_trading import *
from auth import *
from email_alerts import *


###CONSTANTS###
TRADE_OPEN_TEMPLATE = '''
                Triggered EO trader. EO was: {}\n
                cat determined: {}\n
                rating determined: {}\n
                mexico mentions: {}\n
                china mentions: {}\n
                calculation duration: {} seconds\n
                '''

TRADE_CLOSE_TEMPLATE = '''
                {} LIQUIDATED.\n
                Time: {} \n
                Gain on trade was: {}\n
                '''

MARKET_OPEN_IN_MINUTES = 13 * 60 + 30
MARKET_CLOSE_IN_MINUTES = 20 * 60

###CONSTANTS###

def gmt_minutes():
    return time.gmtime().tm_hour * 60 + time.gmtime().tm_min

def time_to_sell():
    THIRTY_MINS_IN_SECONDS = 1800
    if gmt_minutes() < (MARKET_CLOSE_IN_MINUTES - 35):
        time = gmt_minutes() + 30
    else:
        time = (MARKET_CLOSE_IN_MINUTES - gmt_minutes() - 2)
    time_string = "{}:{}".format(time // 60, time % 60)
    return time_string

    
#bug with sale scheduling still
def schedule_sell(position):
    position.close_price = position.current_price()
    position.net_gain = (position.close_price - position.open_price) / position.open_price
    df = read_trade_datafile()
    temp_data = pd.DataFrame({'ticker': position.ticker,'open_price':position.open_price,
                'close_price':position.close_price, 'close_time':time.strftime("%c"), 
                'linked_eo':position.linked_eo.filename, 'net_gain':position.net_gain, 
                'id':position.linked_eo.id_, 'open_time': position.open_time},index=['id'])
    df = pd.concat([df, temp_data])
    write_trade_datafile(df)
    text = TRADE_CLOSE_TEMPLATE.format(position.ticker, time.strftime("%c"),  position.net_gain)
    print(text)
    #wide_alert("Executive Order Trade Event", text)
    return schedule.CancelJob


def write_trade_datafile(df):
    pd.DataFrame.to_csv(df, 'trade_data.csv', index=False,encoding="utf-8")


def read_trade_datafile(verbose=False):
    if os.path.isfile('trade_data.csv'):
        df = pd.read_csv('trade_data.csv', encoding="utf-8")
    else:
        cols = ["id", "open_time", "open_price", "close_time", "close_price", "ticker", "linked_eo", "net_gain"]
        df = pd.DataFrame(columns=cols)
    df.set_index('id')
    return df

def run_main(verbose=True):
    if verbose: print("started listening for the day. time:",time.strftime("%c"))
    while gmt_minutes() < MARKET_CLOSE_IN_MINUTES + 1:
        start_calc = time.time()
        schedule.run_pending()
        try:
            orders = scrape()
        except Exception:
            orders = []
            if verbose: print('Was temporarily kicked from wh.gov')
        if orders:
            print('there were orders')
            positions = []
            for order in orders:
                write_textfile(order.txt, 'input.txt', 'resources')
                if verbose: print('found an eo')
                process = subprocess.Popen(['java', '-jar', 'java/textProcessor.jar'],
                    stdout=subprocess.PIPE)
                args = process.stdout.read().decode('utf-8').split()
                order.cat = args[0]
                order.rating = args[1]
                order.mexico_mentions = args[2]
                order.china_mentions = args[3]
                print('cat:',order.cat)
                position = trade(order)
                time_of_trade = time.time()
                calc_duration = time_of_trade - start_calc
                if verbose: print("calculation duration:", calc_duration)
                text = TRADE_OPEN_TEMPLATE.format(order.filename, order.cat, order.rating, 
                    order.mexico_mentions, order.china_mentions, calc_duration)
                if verbose: print(text)
                #wide_alert("Executive Order Trade Event",text)
                if position:
                    if verbose: print('added new position in', position.ticker)
                    positions.append(position)
                #optimizie this reading/writing
                df = read_eo_datafile()
                df.set_value(order.id_, 'cat', order.cat)
                df.set_value(order.id_, 'rating', order.rating)
                df.set_value(order.id_, 'mexico_mentions', int(order.mexico_mentions))
                df.set_value(order.id_, 'china_mentions', int(order.china_mentions))
                write_eo_datafile(df)
            for position in positions:
                time_string = time_to_sell()
                schedule.every().day.at(time.strftime(time_string)).do(schedule_sell(position))


    if verbose: print("done listening for the day. time:",time.strftime("%c"))


if __name__ == '__main__':
    print('if nothing happens, market is closed. you can go to line 38 and temporarily replace 20 with a larger number')
    schedule.every().monday.at("08:28").do(run_main)
    schedule.every().tuesday.at("08:28").do(run_main)
    schedule.every().wednesday.at("08:28").do(run_main)
    schedule.every().thursday.at("08:28").do(run_main)
    schedule.every().friday.at("08:28").do(run_main)
    if gmt_minutes() > MARKET_OPEN_IN_MINUTES and gmt_minutes() < MARKET_CLOSE_IN_MINUTES:
        print('started late')
        run_main()
    
    while 1:
        schedule.run_pending()
        time.sleep(1)