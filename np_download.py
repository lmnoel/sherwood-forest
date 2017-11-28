import requests
from bs4 import BeautifulSoup
import re, os, logging, time, random
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


def nyt_scrape_year(year):
    count_not_found = 0
    total_downloaded = 0
    logger.info('Downloading year: {}'.format(year))
    top_level_directory = 'newspaper_data/'
    if not os.path.exists(top_level_directory):
        os.mkdir(top_level_directory)
    low_level_directory = top_level_directory + str(year)
    if not os.path.exists(low_level_directory):
        os.mkdir(low_level_directory)
    
    template_url = 'http://spiderbites.nytimes.com/free_{}/index.html'.format(year)
    #template_url = 'http://spiderbites.nytimes.com/free_1996/articles_1996_01_00000.html'
    #template_url = 'http://www.nytimes.com/1996/01/01/business/media-television-with-fenetic-debut-cnn-s-business-network-plays-catch-up-there.html'
    

    res = requests.get(template_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    year_pages = []
    for url in soup.find_all('a'):
        #print(url.get('href'))
        if 'free_' in url.get('href'):
            year_pages.append('http://spiderbites.nytimes.com' + url.get('href'))

    #return year_pages
    urls_to_scrape = []
    for year_page in year_pages:

        local_urls = requests.get(year_page)
        soup = BeautifulSoup(local_urls.text, 'html.parser')
        text = ''
        for url in soup.find_all('a'):
            #print(url.get('href'))
            url_plaintext = url.get('href')
            if re.search('http://www.nytimes.com/[0-9]{4}/[0-9]{2}/[0-9]{2}/.+',url_plaintext):
                if 'business' in url_plaintext or 'world' in url_plaintext:
                    urls_to_scrape.append(url_plaintext)


    for url in urls_to_scrape:
        t = threading.Thread(target=download_page, args = (low_level_directory,url))
        t.daemon = True
        t.start()
  
    return

def download_page(low_level_directory, url):
    res = requests.get(url)
    try:
        soup = BeautifulSoup(res.text, 'html.parser')
        paragraphs = soup.find_all('p',{'class':'story-body-text story-content'})
        paragraphs = [i.text for i in paragraphs]
        datetime = soup.find_all('meta',property='article:modified')[0]['content']

        article = '\n-----\n' + datetime +'\n-----\n' + '\n'.join(paragraphs)
        date = re.findall('(\d\d\d\d)-(\d\d)-(\d\d).+',datetime)
        date = date[0]
        filepath = low_level_directory + '/{}_{}/'.format(date[1], date[2])
        if not os.path.exists(filepath):
            os.mkdir(filepath)
        filename = filepath + 'nyt.txt'
        
        if os.path.exists(filename):
            file_mode = 'a'
        else:
            file_mode = 'w'
        writefile = open(filename, file_mode)
        writefile.write(article)
        writefile.close()
    except:
        logger.info('page not found: {}'.format(url,))

def nyt_scrape_all():
    for year in range(1996, 2018):
        nyt_scrape_year(year)