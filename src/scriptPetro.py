import tweepy
import sys
import jsonpickle
import json
from pymongo import MongoClient

client = MongoClient(host=['192.168.100.84:27018'])
db = client.TwitterStream
collection = db.tweets

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,
				   wait_on_rate_limit_notify=True)

keywords = ['chocolate']
language = ['pt']
limit = 10000000 
tweetLimit = 100

maxId = -1

tweetCount = 0

while tweetCount < limit:
    try:
        if (maxId <= 0):
            newTweets = api.search(q=keywords, count=tweetLimit)
        else:
            newTweets = api.search(q=keywords, count=tweetLimit,
                                    max_id=str(maxId - 1))
        if not newTweets:
            print("No tweets found")
            break
        for tweet in newTweets:
        	collection.insert_one(tweet._json)
         
        tweetCount += len(newTweets)
        print("Downloaded {0} tweets".format(tweetCount))
        max_id = newTweets[-1].id
    except tweepy.TweepError as e:
        print("error : " + str(e))
        break

print ("{0} tweets found, saved on MongoDB".format(tweetCount))
