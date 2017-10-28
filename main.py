import tweepy
from tweepy import OAuthHandler
import json
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('mongodb://veli:kamil7insan@ds237445.mlab.com:37445/heroku_wzpvdrhs')
db = client['heroku_wzpvdrhs']
collection = db.thy

print(collection)

def store_tweet(tweet):
    json_tweet = json.dumps(tweet)
    # pprint(json_tweet)
    collection.insert_one(tweet)

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


exit(1)