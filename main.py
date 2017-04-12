#This file runs the code needed for EO trading

import time
from auth import *
from wh_scraper import *
<<<<<<< HEAD
<<<<<<< HEAD
import subprocess
=======
from paper_trading import *
>>>>>>> origin/master
=======
from paper_trading import *
>>>>>>> origin/master

def go():
    #run during a reasonable trading window
    while time.gmtime().tm_hour < 22:
        titles = []
        titles = main()
        if titles:

            process = subprocess.Popen(['java', '-jar', 'java/textProcessor.jar'],
                stdout=subprocess.PIPE)
            args = process.stdout.read().decode('utf-8').split()
            #args[0] = category
            #args[1] = rating
            #args[2] = mexicoMentions
            #args[3] = chinaMentions

            #javacode
            #trade(args_from_NLP)
            pass
    return

if __name__ == '__main__':
    go()