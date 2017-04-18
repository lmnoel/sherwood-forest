#This file runs the code needed for EO trading

import time
from apscheduler.schedulers.blocking import BlockingScheduler
from auth import *
from wh_scraper import *

import subprocess
from paper_trading import *
from auth import *
from email_alerts import *


def go(verbose=False):
    portfolio = Portfolio()
    portfolio.add_cash(100000)
    time_of_trade = None
    if verbose: print('Started listening for the day')
    while time.gmtime.tm_hr < 20:
        start_calc = time.time()
        titles = []
        titles = main()
        if time_of_trade:
            if time.time() - time_of_trade > 30*60:
                end_cash = portfolio.liquidate()
                time_of_trade = None
                gain = (end_cash - 100000) / 100000
                text = '''
                POSITION LIQUIDATED.\n
                Gain on trade was: {}%\n
                '''
                wide_alert("Executive Order Trade Event", text)

        if titles:
            process = subprocess.Popen(['java', '-jar', 'java/textProcessor.jar'],
                stdout=subprocess.PIPE)
            args = process.stdout.read().decode('utf-8').split()
            cat = args[0]
            rating = args[1]
            mexico_mentions = args[2]
            china_mentions = args[3]
            portfolio = trade(cat, rating, mexico_mentions, china_mentions, portfolio)
            time_of_trade = time.time()
            calc_duration = time_of_trade - start_calc
            text = '''
            Triggered EO trader. EO was: {}\n
            cat determined: {}\n
            rating determined: {}\n
            mexico mentions: {}\n
            china mentions: {}\n
            calculation duration: {} seconds\n
            '''.format(titles[0],cat, rating, mexico_mentions, china_mentions, calc_duration)
            wide_alert("Executive Order Trade Event",text)
    if verbose: print("stopped listening for the day")




if __name__ == '__main__':


    sched = BlockingScheduler()

    sched.add_job(go, 'cron', day='0-5', hour='8',minute='28')

    sched.start()



