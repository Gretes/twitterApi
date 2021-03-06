import tweepy
from tweepy import OAuthHandler
import json
from pymongo import MongoClient
from time import sleep
import sys
from datetime import datetime


client = MongoClient('mongodb://veli:kamil7insan@ds237445.mlab.com:37445/heroku_wzpvdrhs')
db = client['heroku_wzpvdrhs']
collection = db.bein1

last_item = collection.find_one(sort=[["id", -1]])
start_date = datetime.strptime(last_item["created_at"], '%a %b %d %H:%M:%S +0000 %Y').strftime("%Y-%m-%d")
max_id = last_item["id_str"]

print(collection, '\n', start_date, max_id)

collection = db.bein1

class TW(object):
    def __init__(self):
        self.tweetbank = []

    def addtweet(self, tweet):
        self.tweetbank.append(tweet)

    def printme(self):
        self.tweetbank.reverse()
        for tweet in self.tweetbank:
            print(tweet['created_at'])

    def store_tweet(tweet):
        while True:
            try:
                result = collection.insert_one(tweet)
                print(tweet)
            except Exception as e:
                exception_name, exception_value = sys.exc_info()[:2]
                print(exception_name, exception_value)
                continue

            if (result.acknowledged):
                print('added')
                break

with open('accountInfo.json') as data_file:
    accInfo = json.load(data_file)

# Create variables for each key, secret, token
consumer_key = accInfo["consumer_key"]
consumer_secret = accInfo["consumer_secret"]
access_token = accInfo["access_token"]
access_token_secret = accInfo["access_token_secret"]

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

query = '@beINSPORTS_TR'
max_tweets = 10
tweets = tweepy.Cursor(api.search, q=query, since=start_date, count=100).items(max_tweets)

tw = TW()
while True:
    try:
        for tweet in tweets:
            sleep(0.25)
            print(tweet.created_at, tweet.user.name)
            tw.addtweet(tweet._json)
            # store_tweet(tweet._json)
        tw.printme()
        break
    except tweepy.TweepError:
        print('DEBUG: tweepy error')
        sleep(60)
        continue

    except IOError:
        print('DEBUG: io error')
        sleep(60)
        continue

    except StopIteration:
        break

print("Finished!!!")

exit(1)
