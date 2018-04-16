import tweepy
from tweepy import OAuthHandler
import json
from time import sleep
import pyley

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

myName = 'hrnzkan'

# Create cayley client
client = pyley.CayleyClient("http://192.168.1.103:64210", "v1")

searched_names = []

def find_followers(name, cayley_client, n=5, depth=0):
    if depth >= 3:
        print('Max depth reached!')
        return
    searched_names.append(name)
    depth += 1
    f_count = 0
    pages = tweepy.Cursor(api.followers, screen_name=name, count=5).pages()
    while True:
        try:
            for page in pages:
                for follower in page:
                    follower_name = follower.screen_name
                    print(follower_name, depth)
                    if follower_name in searched_names:
                        print('Skipping already searched name', follower_name)
                        continue
                    if f_count >= n:
                        return
                    cayley_client.AddQuad(follower_name, 'follows', name)
                    find_followers(follower_name, cayley_client, depth=depth)
                    f_count += 1
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

find_followers(myName, client)