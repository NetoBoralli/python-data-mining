# from tweepy import Stream
# from tweepy import OAuthHandler
# from tweepy.streaming import StreamListener
# from tweepy import Cursor
# import tweepy
# from pymongo import MongoClient
# import json
# import datetime

# client = MongoClient('localhost', 27017)
# db = client.TwitterStream
# collection = db.tweets

# keywords = ['chocolate']
# language = ['pt']

# consumer_key = 'j3nP1EkKSDQrbDh1csIaZjfmy'
# consumer_secret = 'BpqdIBGVS89WCnIZLHrzq46leYc2tCX0wz4vXOiVmCHju6JRXq'
# access_token = '181700274-Xd8OZTf2EwKsEZrMG4SvP02Y24AtPKpPFQrlUGOy'
# access_secret = 'P5g1VMCtJcghnDFVWym27NU0TJ0ucs5vQOmqqcRKcpqOB'

# class Listener(StreamListener):

#     def on_data(self, data):
#         t = json.loads(data)

#         tweet_id = t['id_str']
#         username = t['user']['screen_name']
#         followers = t['user']['followers_count']
#         text = t['text']
#         hashtags = t['entities']['hashtags']
#         dt = t['created_at']
#         language = t['lang']

#         created = datetime.datetime.strptime(dt, '%a %b %d %H:%M:%S +0000 %Y')

#         tweet = {'id':tweet_id, 'username': username, 'followers': followers, 'text':text, 'hashtags':hashtags, 'language':language, 'created':created}

#         collection.insert_one(tweet)

#         print(username + ':' + ' ' + dt + '-' + text)
#         return True

#     def on_error(self, status):
#         print(status)

# if __name__ == '__main__':
#     auth = OAuthHandler(consumer_key, consumer_secret)
#     auth.set_access_token(access_token, access_secret)
#     api = tweepy.API(auth)
#     for result in tweepy.Cursor(api.search, q='chocolate', count=100, lang='pt', since_id=1).items():
#         collection.insert(result._json)

import tweepy
import sys
import jsonpickle
import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.TwitterStream
collection = db.tweetests

consumer_key = 'j3nP1EkKSDQrbDh1csIaZjfmy'
consumer_secret = 'BpqdIBGVS89WCnIZLHrzq46leYc2tCX0wz4vXOiVmCHju6JRXq'
access_token = '181700274-Xd8OZTf2EwKsEZrMG4SvP02Y24AtPKpPFQrlUGOy'
access_secret = 'P5g1VMCtJcghnDFVWym27NU0TJ0ucs5vQOmqqcRKcpqOB'

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
        # if (maxId <= 0):
        #     newTweets = api.search(q=keywords, count=tweetLimit, lang='pt')
        # else:
        #     newTweets = api.search(q=keywords, count=tweetLimit, lang='pt',
        #                             max_id=str(maxId - 1))
        # if not newTweets:
        #     print("No tweets found")
        #     break
        # for tweet in newTweets:
        # 	collection.insert_one(tweet._json)

        # tweetCount += len(newTweets)
        # print(newTweets[0].created_at)
        # # print("Downloaded {0} tweets".format(tweetCount))
        # max_id = newTweets[-1].id

        for result in tweepy.Cursor(api.search, q=keywords, count=tweetLimit, lang='pt').items():
            collection.insert(result._json)
            tweetCount += 1
            if tweetCount == limit:
                break
            # todo: put limitatior when the same tweet is found again (created_at == today)
            print(result.created_at)
            
    except tweepy.TweepError as e:
        print("error : " + str(e))
        break

print ("{0} tweets found, saved on MongoDB".format(tweetCount))
