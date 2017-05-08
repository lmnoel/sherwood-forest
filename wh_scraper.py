#Logan Noel
#
#Aptil 9 2017
#
#Scrape Executive Orders from whitehouse.gov

import requests, bs4
import sys
import urllib3
import csv
import re
import os.path
import time
from time import strftime
import pandas as pd
urllib3.disable_warnings()

class Order(object):

    def __init__(self,txt,filename):
        self.txt = txt
        self.filename = filename

def get_urls(verbose=False):
    valid = True
    page = -1
    url_list = []
    base_page = 'https://www.whitehouse.gov'
    while valid:
        page += 1
        eoBaseUrl = 'https://www.whitehouse.gov/briefing-room/presidential-actions/executive-orders?term_node_tid_depth=51&page=' + str(page)
        eoRes = requests.get(eoBaseUrl)
        eoRes.raise_for_status()
        soupObj = bs4.BeautifulSoup(eoRes.text, "html.parser")
        # get all the executive order links and titles
        # returns array like this: [<a href>title</a>, <a href>title</a>, ...]
        eoLinks = soupObj.select('h3 > a')
        num_urls = len(eoLinks)
        if num_urls == 0:
            valid = False
            break
        # for each link in the array,
        for link in range(num_urls):
          # get just the href
          hrefOnly = eoLinks[link].get('href')
          full_url = base_page + hrefOnly
          url_list.append(full_url)
          # get just the title
          titleOnly = eoLinks[link].getText()
    if verbose: print("{} EO(s) on whitehouse.gov".format(len(url_list)))
    return url_list


def from_url_get_text(url_string):
    '''
    Converts URL to BS4 Soup object.

    Input: url: string
    Returns: bs4 soup
    '''
    pm = urllib3.PoolManager()

    html = pm.urlopen(url = url_string, method = "GET").data
    soup = bs4.BeautifulSoup(html,'html.parser')
    title = soup.title.text
    text = ''
    for tag in soup.find_all("p"):
        text += tag.text

    text = re.sub('[\xa0]','',text)
    return text, title[:-26]


def write_textfile(text,title,path):    
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = path + '/'+ title
    file = open(file_name,'w') 
    file.write(text) 
    file.close() 

def write_datafile(df):
    pd.DataFrame.to_csv(df, 'eo_data.csv', index=False,encoding="utf-8")


def read_datafile(verbose=False):
    if os.path.isfile('eo_data.csv'):
        df = pd.read_csv('eo_data.csv', encoding="utf-8")
    else:
        cols = ["id", "url", "txtfile", "open_time","open_price","close_time","close_price"]
        df = pd.DataFrame(columns=cols)
    df.set_index('id')
    if verbose: print("{} EO(s) currently on file".format(len(df)))
    return df

def scrape(verbose=False):
    if verbose: urls = get_urls(verbose=True)
    if not verbose: urls = get_urls()
    
    df = read_datafile()
    to_download = list(set(urls) - set(df['url']))
    if verbose: print("to download:",len(to_download))
    if len(to_download) == 0:
        if verbose: print('Already up-to-date')
        return False
    orders = []
    for url in to_download:
        text, title = from_url_get_text(url)
        title += '.txt'
        write_textfile(text, title, 'eo_textfiles')
        id_ = len(df) + 1
        temp_data = pd.DataFrame({'id':id_, 'url':url, 'txtfile':title, 
            'open_time':time.strftime("%c"), 'open_price':'None', 'close_time': 'None', 
            'close_price': 'None'}, index=[id_])
        df = pd.concat([df, temp_data])
        orders.append(Order(text, title))
    write_datafile(df)   
    if verbose: print("Downloaded {} EO(s)".format(len(to_download)))
    return orders

def test():
    n = 0
    while 1:
        print(strftime("%c"))
        n+= 1
        print(n)
        start = time.time()
        titles = scrape(verbose=True)
        end = time.time()

if __name__ == '__main__':
    test()
    #start = time.time()
    #titles = scrape(verbose=True)
    #end = time.time()
    #print('Took {} seconds'.format(end - start))

