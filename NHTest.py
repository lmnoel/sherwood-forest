import subprocess
from news_api import *
import os.path
import schedule
import pandas as pd
from time import strftime
import time
from auth import *
import csv

SOURCES = ['bloomberg','cnbc', 'financial-times','fortune','reuters','the-wall-street-journal',
            'associated-press', 'business-insider', 'cnn', 'fortune', 'the-economist', 'the-new-york-times',
            'the-washington-post']

#IMPORTAN NOTE! This program the system time is on eastern.
#Also, remember to check for inconsistancies in and around daylight savings

def process_headlines():
    process = subprocess.Popen(['java', '-jar', 'NHTextProcessor.jar'],
    	stdout=subprocess.PIPE)
    rating = process.stdout.read().decode('utf-8').split()
    return float(rating[0])
    
def gmt_minutes():
    hours = time.gmtime().tm_hour
    minutes = time.gmtime().tm_min
    return hours * 60 + minutes

def update_input():
    api_key = read_api_key()
    headlines = get_all_headlines(api_key)

    write_textfile(headlines, 'input.txt','NHresources')

def update_one_input(source):
    api_key = read_api_key()
    headlines = get_headline(source, api_key)

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
        cols = ["id", "date", "GLD", "IVV", "morning_test"] + SOURCES
        df = pd.DataFrame(columns=cols)
    return df

def job():
    ratings = []
    for source in SOURCES:
        update_one_input(source)
        ratings.append(process_headlines())
    try:
        GLD_price = get_quote("GLD")['previous_close']
    except:
        GLD_price = -1
    try:    
        IVV_price = get_quote("IVV")['previous_close']
    except:
        IVV_price = -1
    if gmt_minutes() < 900:
        morning_test = True
    else:
        morning_test = False
    df = read_nh_datafile()
    id_ = len(df)
    fields = [id_, time.strftime("%c"), GLD_price, IVV_price, morning_test] + ratings
    if not os.path.isfile('nh_data.csv'):
        with open(r'nh_data.csv', 'a') as f:
            cols = ["id", "date", "GLD", "IVV", "morning_test"] + SOURCES
            writer = csv.writer(f)
            writer.writerow(cols)
    with open(r'nh_data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

if __name__ == '__main__':
    TIMES = ["09:28","15:58"]
    for time_ in TIMES:
        schedule.every().monday.at(time_).do(job)
        schedule.every().tuesday.at(time_).do(job)
        schedule.every().wednesday.at(time_).do(job)
        schedule.every().thursday.at(time_).do(job)
        schedule.every().friday.at(time_).do(job)
    while 1:
        schedule.run_pending()
        time.sleep(1)
