import tweepy
from tweepy import OAuthHandler
import json
from pprint import pprint

def store_tweet(tweet):
    json_tweet = json.dumps(tweet)
    pprint(json_tweet)
    with open('tweets.json', mode='a', encoding='utf-8') as feedsjson:
        json.dump(json_tweet, feedsjson)

with open('accountInfo.json') as data_file:
    accInfo = json.load(data_file)

# Create variables for each key, secret, token
consumer_key = accInfo["consumer_key"]
consumer_secret = accInfo["consumer_secret"]
access_token = accInfo["access_token"]
access_token_secret = accInfo["access_token_secret"]

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

query = '#thy'
max_tweets = 10

for tweets in tweepy.Cursor(api.search, q=query).items(max_tweets):
    store_tweet(tweets._json)
