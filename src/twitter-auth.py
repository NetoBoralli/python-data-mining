import tweepy
import json
from tweepy import OAuthHandler

consumer_key = 'consumer_key'
consumer_secret = 'consumer_secret'
access_token = 'access_token'
access_secret = 'access_secret'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

# for status in tweepy.Cursor(api.home_timeline).items(10):
#     print(status.text)

def process_or_store(tweet):
    print(json.dumps(tweet))

for status in tweepy.Cursor(api.home_timeline).items(10):
    process_or_store(status._json)

for friend in tweepy.Cursor(api.friends).items():
    process_or_store(friend._json)

for tweet in tweepy.Cursor(api.user_timeline).items():
    process_or_store(tweet._json)

