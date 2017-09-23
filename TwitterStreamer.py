#Steps to replicate NBER Paper "WHAT CAN WE LEARN FROM EURO-DOLLAR TWEETS." Model:

#Build database of tweets from people who mention a given currency 

#Use paper's dictionary to parse each tweet's sentiment

#Divide tweeters into 'knowledgable' (aka positive sentiment tweets correlate with positive
#changes in exchange rates, and vice versa) and 'unknowledgable' traders (aka the sentiment of their tweets
#have basically no correlation with the market). Could also classify based on no. of followers

#Create live-twitter listener to parse the day's expert's sentiment and open a positive/negative
#position accordingly

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import csv, json, time, re, logging, schedule, sys
import os.path
import pandas as pd
from auth import get_quote
from twit_currency_dat import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

handler = logging.FileHandler('twitter_streamer.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)


def read_api_keys():
    global ACCESS_TOKEN
    global ACCESS_SECRET
    global CONSUMER_KEY
    global CONSUMER_SECRET

    file = open('twitter_api_keys.txt','r')
    s = file.read()
    s = s.split('\n')
    ACCESS_TOKEN = s[0]
    ACCESS_SECRET = s[1]
    CONSUMER_KEY = s[2]
    CONSUMER_SECRET = s[3]

# Save each tweet in the stream to file 
def run_stream(keyword='eurusd',filter_by_followers=None):
    try:
        read_api_keys()
        oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
        logging.info("Loaded API keys")
    except:
        logging.info("Unable to load API keys (missing or out of date")
        return
    # Initiate the connection to Twitter Streaming API
    twitter_stream = TwitterStream(auth=oauth)
    iterator_succeeded = False
    fails = 0
    while not iterator_succeeded:
        try:
            iterator = twitter_stream.statuses.filter(track=keyword,language="en")
            iterator_succeeded=True
            logging.info("Now listening for tweets")
        except TwitterHTTPError:
            if fails <= 5:
                wait_time = 60 * (2 ** fails)
            else:
                wait_time = 60 * 16
            fails += 1
            logging.info("HTTP Error. sleeping for {} seconds then attempt to reconnect".format(wait_time))
            iterator_succeeded = False
            time.sleep(wait_time)
    filename = r'tweet_data/'+ time.strftime("%d-%m-%y") + '_raw_tweets' + '.csv'
    if not os.path.exists('tweet_data'):
        os.makedirs('tweet_data')
    if not os.path.isfile(filename):
        with open(filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(['date_time', 'user_id','num_followers','tweet_text'])
    logger.info("Writing tweets to: {}".format(filename))
    for tweet in iterator:
        print('pre filter')
        print(tweet['text'])
        while not (int(time.strftime("%H")) == 23 and int(time.strftime("%M")) >= 58):
            fields = [tweet['created_at'],tweet['user']['id'],
            tweet['user']['followers_count'], tweet['text']]
            print(tweet['text'])
            if filter_by_followers:
                if filter_by_followers <= fields[2]:
                    with open(filename, 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow(fields)
            else:
                with open(filename, 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow(fields)
    logger.info("Stopped listening to the day's tweets")

def rate_tweet(tweet):
    for search_string in POS_SIMPLE:
        if re.search(search_string, tweet):
            print('in pos simple')
            return 1
    for search_string in NEG_SIMPLE:
        if re.search(search_string, tweet):
            print('in neg simple')
            return -1
    for req, prohibs in POS_COMPLX.items():
        if re.search(req, tweet):
            good = True
            for prohib in prohibs:
                if re.search(prohib, tweet):
                    good = False
                    break
            if good:
                return 1
    for req, prohibs in NEG_COMPLX.items():
        if re.search(req, tweet):
            bad = True
            for prohib in prohibs:
                if re.search(prohib, tweet):
                    bad = False
                    break
            if bad:
                return -1

    return 0

def process_days_tweets():
    logger.info("Begin processing tweets")
    raw_filename = r'tweet_data/' + time.strftime("%d-%m-%y") + '_raw_tweets' + '.csv'
    if not os.path.isfile(raw_filename):
        return
    df = pd.read_csv(raw_filename)
    counter = 0
    total_rating = 0
    fxe = float(get_quote('FXE')['adjusted_previous_close'])
    for index, data in df.iterrows():
        total_rating += rate_tweet(data['tweet_text'])
        counter += 1
    if counter != 0:
        total_rating = total_rating / counter
    else:
        total_rating = 0

    if not os.path.isfile('tweet_data/processed_data.csv'):
        with open(filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(['date','num_tweets','rating','FXE'])
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime("%d-%m-%y"), counter, total_rating])
        logger.info("Finished writing to file")
    logger.info("Finished writing summary data to: {}".format(filename))


if __name__ == '__main__':
    if '-o' in sys.argv:
        logger.info("Listener launched in override mode")
        run_stream()
    else:
        logger.info("Launched in normal mode")
    schedule.every().day.at("23:59").do(process_days_tweets)
    schedule.every().day.at("00:00").do(run_stream)

    while 1:
        schedule.run_pending()
        time.sleep(1)
    