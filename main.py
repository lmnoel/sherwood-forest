#This file runs the code needed for EO trading

import time
from auth import *
from wh_scraper import *
from paper_trading import *

def go():
    #run during a reasonable trading window
    while time.gmtime().tm_hour < 22:
        titles = []
        titles = main()
        if titles:
            #javacode
            #trade(args_from_NLP)
            pass
    return

if __name__ == '__main__':
    go()