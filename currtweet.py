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
import csv
import json
import time
from time import strftime
import os.path

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

read_api_keys()
oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)

try:
    # Get a sample of the public data following through Twitter
    iterator = twitter_stream.statuses.filter(track="pound, dollar, euro",language="en")
except TwitterHTTPError:
    print("Exceeded call limit")

# Save each tweet in the stream to file 
def run_stream():
    for tweet in iterator:
        filename = r'tweet_data/'+ time.strftime("%d-%m-%y") + '.csv'
        if not os.path.exists('tweet_data'):
            os.makedirs('tweet_data')
        fields = [tweet['created_at'],tweet['user']['id'],
            tweet['user']['followers_count'], tweet['text']]
        with open(filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
        print(fields)

if __name__ == '__main__':
    run_stream()
    