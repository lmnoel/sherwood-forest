import subprocess
from news_api import *
import os.path
import schedule
import pandas as pd
from time import strftime
import time
from auth import *

def process_headlines():
    process = subprocess.Popen(['java', '-jar', 'NHTextProcessor.jar'],
    	stdout=subprocess.PIPE)
    rating = process.stdout.read().decode('utf-8').split()
    return rating
    

def update_input():
    api_key = read_api_key()
    headlines = get_all_headlines(api_key)

    write_textfile(headlines, 'input.txt','NHResources')

def write_textfile(text,title,path):    
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = path + '/'+ title
    file = open(file_name,'w') 
    for row in text:
        if row:
            file.write(row) 
    file.close()

def read_nh_datafile(verbose=False):
    if os.path.isfile('nh_data.csv'):
        df = pd.read_csv('nh_data.csv', encoding="utf-8")
    else:
        cols = ["rating", "date", "VXX", "IVV", "morning_test", "id"]
        df = pd.DataFrame(columns=cols)
    df.set_index('id')
    return df

def write_nh_datafile(df):
    pd.DataFrame.to_csv(df, 'nh_data.csv', index=False,encoding="utf-8")

def job(morning_test):
    try:
        update_input()
        rating = process_headlines()
        VXX_price = get_quote("VXX")
        IVV_price = get_quote("IVV")
    except:
        rating = 'unable to access server'
        VXX_price = -1
        IVV_price = -1
    df = read_nh_datafile()
    id_ = len(df)
    temp_data = pd.DataFrame({'id':id_, 'rating':rating, 'VXX':VXX_price,
        'IVV':IVV_price, 'morning_test':morning_test, 
        'date':time.strftime("%c")}, index=['id'])
    df = pd.concat([df, temp_data])
    write_nh_datafile(df)
    return df

if __name__ == '__main__':
    schedule.every().monday.at("09:28").do(job(True))
    schedule.every().tuesday.at("09:28").do(job(True))
    schedule.every().wednesday.at("09:28").do(job(True))
    schedule.every().thursday.at("09:28").do(job(True))
    schedule.every().friday.at("09:28").do(job(True))
    schedule.every().saturday.at("09:28").do(job(True))
    schedule.every().sunday.at("09:28").do(job(True))
    schedule.every().monday.at("15:58").do(job(False))
    schedule.every().tuesday.at("15:58").do(job(False))
    schedule.every().wednesday.at("15:58").do(job(False))
    schedule.every().thursday.at("15:58").do(job(False))
    schedule.every().friday.at("15:58").do(job(False))
    schedule.every().saturday.at("15:58").do(job(False))
    schedule.every().sunday.at("15:58").do(job(False))
    while 1:
        schedule.run_pending()
        time.sleep(1)
