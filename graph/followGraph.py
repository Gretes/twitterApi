import tweepy
from tweepy import OAuthHandler
import json
from datetime import datetime
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

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5,
                 retry_errors=set([503]))

myName = 'hrnzkan'

# Create cayley client
client = pyley.CayleyClient("http://intelcon.freeddns.org:64210", "v1")
g = pyley.GraphObject()

searched_names = []

def find_followers(name, cayley_client, user_id=None, n=200, depth=0):
    if depth == 0:
        user = api.get_user(screen_name=name)
        user_name = user.name
        user_screen_name = user.screen_name
        user_id = user.id_str
        user_followers_count = user.followers_count
        user_friends_count = user.friends_count
        user_tweet_count = user.statuses_count
        user_created_at = str(user.created_at)
        user_lang = user.lang
        user_location = user.location
        user_time_zone = user.time_zone
        cayley_client.AddQuad(user_id, 'name', user_name)
        cayley_client.AddQuad(user_id, 'screen_name', user_screen_name)
        cayley_client.AddQuad(user_id, 'followers_count', user_followers_count)
        cayley_client.AddQuad(user_id, 'friends_count', user_friends_count)
        cayley_client.AddQuad(user_id, 'tweet_count', user_tweet_count)
        cayley_client.AddQuad(user_id, 'created_at', user_created_at)
        cayley_client.AddQuad(user_id, 'lang', user_lang)
        cayley_client.AddQuad(user_id, 'location', user_location)
        cayley_client.AddQuad(user_id, 'time_zone', user_time_zone)
        cayley_client.AddQuad(user_id, 'user_update_date', str(datetime.now().date()))
    if depth >= 3:
        print('Max depth reached!')
        return
    searched_names.append(name)
    depth += 1
    f_count = 0
    pages = tweepy.Cursor(api.followers, screen_name=name, count=n).pages()
    while True:
        try:
            for page in pages:
                for follower in page:
                    follower_name = follower.name
                    follower_screen_name = follower.screen_name
                    follower_id = follower.id_str
                    follower_follower_count = follower.followers_count
                    follower_friends_count = follower.friends_count
                    follower_tweet_count = follower.statuses_count
                    follower_created_at = str(follower.created_at)
                    follower_lang = follower.lang
                    follower_location = follower.location
                    follower_time_zone = follower.time_zone

                    response = client.Send(g.Vertex(follower_id).In('followers_update_date').All()).result['result']
                    if response is not None:
                        update_date = response[0]['id']
                        update_date = datetime.strptime(update_date, '%Y-%m-%d')
                        days_past = (datetime.now() - update_date).days
                    else:
                        days_past = 999

                    print(follower_name, depth)
                    if follower_name in searched_names or days_past < 30:
                        print('Skipping already searched name', follower_name)
                        continue

                    cayley_client.AddQuad(follower_id, 'name', follower_name)
                    cayley_client.AddQuad(follower_id, 'screen_name', follower_screen_name)
                    cayley_client.AddQuad(follower_id, 'followers_count', follower_follower_count)
                    cayley_client.AddQuad(follower_id, 'friends_count', follower_friends_count)
                    cayley_client.AddQuad(follower_id, 'tweet_count', follower_tweet_count)
                    cayley_client.AddQuad(follower_id, 'created_at', follower_created_at)
                    cayley_client.AddQuad(follower_id, 'lang', follower_lang)
                    cayley_client.AddQuad(follower_id, 'location', follower_location)
                    cayley_client.AddQuad(follower_id, 'time_zone', follower_time_zone)
                    cayley_client.AddQuad(follower_id, 'user_update_date', str(datetime.now().date()))
                    cayley_client.AddQuad(follower_id, 'follows', user_id)
                    find_followers(follower_name, cayley_client, follower_id, depth=depth)

            cayley_client.AddQuad(str(datetime.now().date()), 'followers_update_date', user_id)
            break
        except tweepy.TweepError as e:
            print('DEBUG: tweepy error')
            sleep(5)
            continue

        except IOError:
            print('DEBUG: io error')
            sleep(60)
            continue

        except StopIteration:
            break

find_followers(myName, client)