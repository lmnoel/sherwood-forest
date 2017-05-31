import subprocess
from news_api import *
import os.path
import schedule
import pandas as pd
from time import strftime
import time

def process_headlines():
    process = subprocess.Popen(['java', '-jar', 'NHTextProcessor.jar'],
    	stdout=subprocess.PIPE)
    rating = process.stdout.read().decode('utf-8').split()

    return rating[0]

def update_input():
    api_key = read_api_key()
    headlines = get_all_descs(api_key)

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
        cols = ["rating", "date", "id"]
        df = pd.DataFrame(columns=cols)
    df.set_index('id')
    return df

def write_nh_datafile(df):
    pd.DataFrame.to_csv(df, 'nh_data.csv', index=False,encoding="utf-8")

def job():
    try:
    update_input()
    rating = process_headlines()
    except:
        rating = 'unable to access server'
    df = read_nh_datafile()
    id_ = len(df)
    temp_data = pd.DataFrame({'id':id_, 'rating':rating, 
        'date':time.strftime("%c")}, index=['id'])
    df = pd.concat([df, temp_data])
    write_nh_datafile(df)

if __name__ == '__main__':
    job()
    schedule.every().monday.at("08:28").do(job)
    schedule.every().tuesday.at("08:28").do(job)
    schedule.every().wednesday.at("08:28").do(job)
    schedule.every().thursday.at("08:28").do(job)
    schedule.every().friday.at("08:28").do(job)
    schedule.every().saturday.at("08:28").do(job)
    schedule.every().sunday.at("08:28").do(job)
    while 1:
        schedule.run_pending()
        time.sleep(1)