#Steps to replicate NBER Paper "WHAT CAN WE LEARN FROM EURO-DOLLAR TWEETS?" Model:

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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

handler = logging.FileHandler('twitter_streamer.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

POS_SIMPLE = [
    '*buy??fxe*',
    '*long??fxe*',
    '*buy?signal*',
    '*upside*breakout*',
    '*eur?usd*bull*intact*',
    '*expect*move*higher*',
    '*oversold*eur*',
    '*eur?usd*oversold*',
    '*ascending*triangle*',
    '*increase*bullish*bet*',
    '*bought*rebound*',
    '*will*move*higher*today*',
    '*bought*dip*',
    '*bought*bounce*',
    '*will*higher*today*',
    '*should?buy*dip*',
    '*rally*has*leg*',
    '*buy*above*moving*average*',
    '*tradable*bottom*',
    '*eur?usd*good?buy*',
    '*raise*eur*exposure*',
    '*will*see*higher*',
    '*going?to*see*higher*',
    '*eur?usd*bias*upside*',
    '*eur?usd*bias*positive*',
    '*eur?usd?will?rise*',
    '*eur?usd?will?continue?to?rise*',
    '*euro?bottoming*',
    '*eur?usd?bottoming*',
    '*staying?long?eur?usd*',
    '*staying?long??eur?usd*',
    '*eur?usd*heads*higher*','*eur?usd*heading*higher*'
    '*bottom?is?in*'
    '*oversold*bounce*'
    '*sticking*with*long*'
    '*potential?buy*'
    '*resume*bull*trend*'
    '*dollar*further*loss*'
    '*long?favor*'
    '*suggest*bull*control*'
    '*suggest*advance*continue*'
    '*spark*eur*buy*',
    '*initiat*eur*buy*',
    '*eurusd?could?bottom*',
    '*euro?could?bottom*',
    '*further*rise*ahead*',
    '*further*advance*ahead*',
    '*stay??eurusd?long*',
    '*stay?eurusd?long*',
    '*stay??eur?usd?long*',
    '*stay?eur?usd?long*',
    '*currently?long??eurusd*',
    '*currently?long?eurusd*',
    '*currently?long??eur?usd*',
    '*currently?long?eur?usd*',
    '*increase*eurusd?long*',
    '*increase*long?eurusd*',
    r'*increase*eur\usd?long*',
    r'*increase*long?eur\usd*',
    '*increase*eurusd?long*',
    '*decrease*eurusd?long*', 
    '*hold*eurusd?long*', 
    '*keep*eurusd?long*', 
    '*increase*eur?usd?long*', 
    '*decrease*eur?usd?long*', 
    '*hold*eur?usd?long*', 
    '*keep*eur?usd?long*'
]

NEG_SIMPLE = [
    '*short?fxe*',
    '*short??fxe*',
    '*buy?uup*',
    '*buy??uup*',
    '*eurusd*buying?put*',
    '*eur?usd*buying?put*',
    '*eur*overbought*',
    '*expect*move*lower*',
    '*descending*triangle*',
    '*sell?resistance*',
    '*selling?resistance*',
    '*down*accelerate*trend*',
    '*buy?euo*',
    '*buy??euo*',
    '*eurusd?will?fall*',
    '*eur?usd?will?fall*',
    '*staying?short*eur?usd*',
    '*staying?short*eurusd*',
    '*fade*rally*',
    '*eur*overpriced*',
    '*signals?sell*eur*',
    '*bias*down*',
    '*eur*overvalued*',
    '*stall*retrace*',
    '*top?is?in*',
    '*deeper?correction*',
    '*sticking*with*short*',
    '*sell*bounce*',
    '*will*see*lower*',
    '*prepare*eur*downturn*',
    '*recovery*fail*',
    '*bear*intact*',
    '*eyes*downside*target*',
    '*eur*look?bad*',
    '*eur*looks?bad*',
    '*eur?usd*has*topped*',
    '*eurusd*has*topped*',
    '*buy the u.s. dollar*',
    '*buy?the?dollar*',
    '*potential?sell*',
    '*downside*remain*',
    '*eur*eyes*downside*',
    '*stay??eurusd?short*',
    '*stay?eurusd?short*',
    '*stay??eur?usd?short*',
    '*stay?eur?usd?short*',
    '*eur?usd*bias*downside*',
    '*eur?usd*bias*negative*',
    '*eurusd*bias*downside*',
    '*eurusd*bias*negative*',
    '*increase*eur?usd?short*',
    '*decrease*eur?usd?short*',
    r'*hold*eur\usd?short*',
    r'*keep*eur\usd?short*',
    '*eurusd*over?bought*',
    '*euro*over?bought*',
    '*eur?usd*over?bought*',
    '*eurusd*overbought*',
    '*euro*overbought*',
    '*eur?usd*overbought*',
    '*further?selling*',
    '*further?eurusd?selling*',
    '*further??eurusd?selling*',
    '*further?eur?usd?selling*',
    '*further??eur?usd?selling*',
    '*increase*eurusd?short*',
    '*increase*short?eurusd*',
    '*increase*eur?usd?short*',
    '*increase*short?eur?usd*',
    '*look*to*sell*',
    '*look*to*buy*put*',
    '*will*selling?the?eur*',
    '*am?selling?the?eur*',
    '*will*head*lower*',
    '*heads*lower*',
    '*heading*lower*',
    '*increase*eurusd?short*',
    '*decrease*eurusd?short*',
    '*hold*eurusd?short*',
    '*keep*eurusd?short*',
    '*currently?short??eurusd*',
    '*currently?short?eurusd*',
    '*currently?short??eur?usd*',
    '*currently?short?eur?usd*'
]

POS_COMPLX = {
    '*buy??eur*' : ['*close*buy*eur*' , '*exit*buy*eur*', r'*close*buy?eurusd*', r'*close*buy?eurusd*', r'*close*buy??eur\usd*', '*buy*,*eur*', r'*buy*:*eur*', r'*buy*fade*', r'*close*buy??eur\usd*', r'*never*buy*eur*'],
    '*buy?eur*' : ['*close*buy*eur*' , '*exit*buy*eur*', r'*close*buy?eurusd*', r'*close*buy?eurusd*', r'*close*buy??eur\usd*', '*buy*,*eur*', r'*buy*:*eur*', r'*buy*fade*', r'*close*buy??eur\usd*', r'*never*buy*eur*'],
    '*buy*lot*eur*' : ['*close*buy*lot*eur*'],
    '*long??eur*' : ['*long?term*', '*was?long*', '*close*long??eur*', '*close*long?eur*', '*exit*long??eur*', '*exit*long?eur*'],
    '*bullish*' : ['*absent*', '*absence*', '*void*', '*lack*', '*bullish*fail*', '*fail*bullish*', '*bullish*invalid*', '*bullish*break*', '*nothing*bullish*', '*missing*', '*were?bullish*', '*was?bullish*', '*no?bullish*', '*not?bullish*', '*market is bullish*'],
    '*covered*short*' : ['*short?term*'],
    '*buy?the?eur*' : ['*never?buy?the?eur*', '*not?buy?the?eur*'],
    '*eur?usd*look?good*' : ['*eur?usd*not*look?good*'],
    '*eur?usd*looks?good*' : ['*eur?usd*not*looks?good*'],
    '*double*long*' : ['*long?term*'],
    '*took*long*position*' : ['*long?term*'],
    '*out*of*eur*short*' : ['*short?term*' , '*stop*out*of*eur*short*'],
    '*add*eur*long*' : ['*long?term*' , '*addict*' , '*dadd*'],
    '*increase*eur*long*' : ['*long?term*' , '*long?off*'],
    '*up*accelerate*trend*' : ['*update*'],
    '*signals?buy*eur*': ['*forexsignals*'],
    '*long?signal*' : ['*long?term*' , '*wait*for*long?signal*'],
    '*higher?high*' : ['*if*higher?high*'],
    '*take*eur?usd*long*': ['*took*profit*'],
    '*took*eur?usd*long*' : ['*took*profit*' , '*took*opportunity*'],
    '*further*buying*' : ['*buying*usd*'],
    '*further*eur*gain*' : ['*against*'],
    '*dip*buy*' : ['*dip*;*eurusd*', '*dip*;*eur?usd*', '*buy*dips?in?cable*', '*buy*dip?in?cable*' '*sell*rall*'],
    '*buy*dip*' : ['*dip*;*eurusd*', '*dip*;*eur?usd*', '*buy*dips?in?cable*', '*buy*dip?in?cable*' '*sell*rall*'],
    '*look*to*buy*' : ['*looks?like*' , '*look*to*buy*put*'],
    '*buying?the?eur*' : ['*buying?the?eur*was*', '*about*buying?the?eur*', '*buying?the?eur*tomorrow*'],
    '*trigger*further*eurusd*gain*' : ['*against*'],
    '*trigger*further*eur?usd*gain*' : ['*against*'],
    '*offer*long*entr*' : ['*long?term*'],
    '*look*to*long*' : ['*long?term*' , '*looks*'],
    '*eur?usd*may*extend*gain*' : ['*against*'],
    '*eurusd*may*extend*gain*' : ['*against*'],
    '*eur?usd*will*extend*gain*' : ['*against*'],
    '*eurusd*will*extend*gain*' : ['*against*'],
    '*eur?usd*set*extend*gain*' : ['*against*'],
    '*eurusd*set*extend*gain*' : ['*against*'],
    'eurusd*targets?higher*' : ['*higher?low*'],
    '*eur?usd*target?higher*' : ['*higher?low*']
}

NEG_COMPLX = {
    '*bearish*' :['*absent*', '*bearish*void*', '*bearish*lack*', '*missing*', '*bearish*fail*', '*void*bearish*', '*lack*bearish*', '*fail*bearish*', '*bearish*break*', '*were?bearish*', '*was?bearish*', '*not?bearish*', '*bearish*invalid*', '*nothing*bearish*',
    '*market is bearish*', '*no?bearish*'],
    '*short?eurusd*' : ['*covered*short*', '*exit*short*', '*stop*short*eur*', '*close*short*'],
    '*short??eurusd*' : ['*covered*short*', '*exit*short*', '*stop*short*eur*', '*close*short*'],
    '*short?eur?usd*' : ['*covered*short*', '*exit*short*', '*stop*short*eur*', '*close*short*'],
    '*short??eur?usd*' : ['*covered*short*', '*exit*short*', '*stop*short*eur*', '*close*short*'],
    '*short?euro*' : ['*covered*short*', '*exit*short*', '*stop*short*eur*', '*close*short*'],
    '*took*short*position*' : ['*short?term*'],
    '*short?signal*' : ['*short?term*'],
    '*sell?signal*' : ['*buy*signal*'],
    '*shorted??euro*' : ['*short?term*'],
    '*shorted??eurusd*' : ['*short?term*'],
    '*shorted??eur?usd*' : ['*short?term*'],
    '*sell?eurusd*' : ['*close*sell*eur*', '*exit*sell*eur*', '*stop*sell*eur*', '*if*sell*eur*', '*where*sell*eur*', '*no?reason*sell*eur*'], 
    '*sell??eurusd*' : ['*close*sell*eur*', '*exit*sell*eur*', '*stop*sell*eur*', '*if*sell*eur*', '*where*sell*eur*', '*no?reason*sell*eur*'], 
    '*sell?eur?usd*' : ['*close*sell*eur*', '*exit*sell*eur*', '*stop*sell*eur*', '*if*sell*eur*', '*where*sell*eur*', '*no?reason*sell*eur*'],
    '*sell??eur?usd*' : ['*close*sell*eur*', '*exit*sell*eur*', '*stop*sell*eur*', '*if*sell*eur*', '*where*sell*eur*', '*no?reason*sell*eur*'],
    '*sell the eur*' : ['*where*sell the eur*'],
    '*short the eur*' : ['*was*short the eur*'],
    '*add*eur*short*' : ['*short?term*' , '*addict*' , '*dadd*'],
    '*sold*rally*' : ['*oversold*'],
    '*sold*bounce*' : ['*oversold*bounce*'],
    '*eurusd*toppy*' : ['*stopp*' , '*dollar?topp*' , '*audusd??topp*'],
    '*eurusd*topping*' : ['*stopp*' , '*dollar?topp*' , '*audusd??topp*'],
    '*eur?usd*toppy*' : ['*stopp*' , '*dollar?topp*' , '*audusd??topp*'],
    '*eur?usd*topping*' : ['*stopp*' , '*dollar?topp*' , '*audusd??topp*'],
    '*bounce*sold*' : ['*oversold*'],
    '*good?short*' : ['*short?term*'],
    '*take*eur*short*' : ['*take*profit*eur*short*', '*take*out*eur*short*', '*take*rest*eur*short*'],
    '*took*eur*short*' : ['*took*profit*eur*short*', '*took*out*eur*short*', '*took*rest*eur*short*'],
    '*further*loss*' : ['*dollar*further*loss*'],
    '*further?fall*' : ['*dollar*further?fall*'],
    '*next*leg*lower*' : ['*long?term*']
}


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
def run_stream(keywords=['EURUSD'],filter_by_followers=None):
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
    while not iterator_succeeded:
        try:
            # Get a sample of the public data following through Twitter
            iterator = twitter_stream.statuses.filter(track=keywords,language="en")
            iterator_succeeded=True
            logging.info("Now listening for tweets")
        except TwitterHTTPError:
            logging.info("Exceeded call limit. will sleep for 30 seconds then attempt to reconnect")
            iterator_succeeded = False
            time.sleep(30)
    filename = r'tweet_data/'+ time.strftime("%d-%m-%y") + '_raw_tweets' + '.csv'
    if not os.path.exists('tweet_data'):
        os.makedirs('tweet_data')
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(['date_time', 'user_id','num_followers','tweet_text'])
    logger.info("Writing tweets to: {}".format(filename))
    for tweet in iterator:
        while not (int(time.strftime("%H")) == 23 and int(time.strftime("%M")) >= 58):
            fields = [tweet['created_at'],tweet['user']['id'],
            tweet['user']['followers_count'], tweet['text']]
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
            return 1
    for search_string in NEG_SIMPLE:
        if re.search(search_string, tweet):
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
    if '-0' in sys.argv:
        logger.info("Listener launched in override mode")
        run_stream()
    else:
        logger.info("Launched in normal mode")
    schedule.every().day.at("23:59").do(process_days_tweets)
    schedule.every().day.at("00:00").do(run_stream)

    while 1:
        schedule.run_pending()
        time.sleep(1)
    