import subprocess
from news_api import *
import os.path
import schedule
import pandas as pd
from time import strftime
import time
from auth import *
import csv

#IMPORTAN NOTE! This program the system time is on eastern.
#Also, remember to check for inconsistancies in and around daylight savings

def process_headlines():
    process = subprocess.Popen(['java', '-jar', 'NHTextProcessor.jar'],
    	stdout=subprocess.PIPE)
    rating = process.stdout.read().decode('utf-8').split()
    return rating
    
def gmt_minutes():
    hours = time.gmtime().tm_hour
    minutes = time.gmtime().tm_min
    return hours * 60 + minutes

def update_input():
    api_key = read_api_key()
    headlines = get_all_headlines(api_key)

    write_textfile(headlines, 'input.txt','NHresources')

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
        cols = ["id", "date", "rating", "VXX", "IVV", "morning_test"]
        df = pd.DataFrame(columns=cols)
    return df

def job():
    try:
        update_input()
        rating = process_headlines()
        rating = float(rating[0])
        VXX_price = get_quote("VXX")
        IVV_price = get_quote("IVV")
        print("VXX: {}, IVV: {}, rating: {}".format(VXX_price, IVV_price, rating))
    except:
        rating = 0
        VXX_price = -1
        IVV_price = -1
    if gmt_minutes() < 900:
        morning_test = True
    else:
        morning_test = False
    df = read_nh_datafile()
    id_ = len(df)
    fields = [id_, time.strftime("%c"), rating, VXX_price, IVV_price, morning_test]
    with open(r'nh_data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

if __name__ == '__main__':
    schedule.every().monday.at("09:28").do(job)
    schedule.every().tuesday.at("09:28").do(job)
    schedule.every().wednesday.at("09:28").do(job)
    schedule.every().thursday.at("09:28").do(job)
    schedule.every().friday.at("09:28").do(job)
    schedule.every().saturday.at("09:28").do(job)
    schedule.every().sunday.at("09:28").do(job)
    schedule.every().monday.at("15:58").do(job)
    schedule.every().tuesday.at("15:58").do(job)
    schedule.every().wednesday.at("15:58").do(job)
    schedule.every().thursday.at("15:58").do(job)
    schedule.every().friday.at("15:58").do(job)
    schedule.every().saturday.at("15:58").do(job)
    schedule.every().sunday.at("15:58").do(job)
    while 1:
        schedule.run_pending()
        time.sleep(1)
