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
    return text, title[0:-26]


def write_textfile(text, name):
    file = open(name + '.txt','w') 
    file.write(text) 
    file.close() 

def write_datafile(urls):
 
    outputFile = open('eo_data.csv', 'w', newline='\n')
    outputWriter = csv.writer(outputFile)
    outputWriter.writerow(urls)

    outputFile.close()

def read_datafile(verbose=False):
    file = open('eo_data.csv')
    reader = csv.reader(file)
    data = list(reader)
    if verbose: print("{} EO(s) currently on file".format(len(data[0])))
    return data[0]

def main(verbose=False):
    if verbose: urls = get_urls(verbose=True)
    if not verbose: urls = get_urls()
    if os.path.isfile('eo_data.csv'):
        if verbose:
            existing_urls = read_datafile(verbose=True)
        else:
            existing_urls = read_datafile()
        to_download = list(set(urls) - set(existing_urls))
        if len(to_download) == 0:
            if verbose: print('Already up-to-date')
            return
    else:
        to_download = urls
    titles = []
    for url in to_download:
        text, title = from_url_get_text(url)
        titles.append(title)
        write_textfile(text,title)
    if verbose: print("Downloaded {} EO(s)".format(len(to_download)))
    write_datafile(urls)
    return titles

if __name__ == '__main__':
    start = time.time()
    titles = main(verbose=False)
    end = time.time()
    print('Took {} seconds'.format(end - start))

