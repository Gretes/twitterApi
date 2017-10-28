import tweepy
from tweepy import OAuthHandler
import json
from pprint import pprint

with open('accountInfo.json') as data_file:
    accInfo = json.load(data_file)

pprint(accInfo)

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
    pprint(tweets._json)
# json.dumps(searched_tweets)
