#Steps to replicate NBER Paper "WHAT CAN WE LEARN FROM EURO-DOLLAR TWEETS?" Model:

#Build database of tweets from people who mention a given currency 

#Use paper's dictionary to parse each tweet's sentiment

#Divide tweeters into 'knowledgable' (aka positive sentiment tweets correlate with positive
#changes in exchange rates, and vice versa) and 'unknowledgable' traders (aka the sentiment of their tweets
#have basically no correlation with the market). Could also classify based on no. of followers

#Create live-twitter listener to parse the day's expert's sentiment and open a positive/negative
#position accordingly