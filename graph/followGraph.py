import tweepy
from tweepy import OAuthHandler
import json
from datetime import datetime
from time import sleep
import pyley
import asyncio

import logging
import logging.handlers

LOGFILE = "info.log"

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

# create a file handler
HANDLER = logging.handlers.RotatingFileHandler(
    LOGFILE, maxBytes=100 * 1024 * 1024, backupCount=5)
HANDLER.setLevel(logging.INFO)

# create a logging format
FORMATTER = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
HANDLER.setFormatter(FORMATTER)

# add the handlers to the logger
LOGGER.addHandler(HANDLER)


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

searched_ids = []
LOGGER.info('iteration started')


def find_followers(name, cayley_client, user=None, depth=0):
    futures = []
    LOGGER.info('find followers and add properties')
    if user is None:
        user = api.get_user(screen_name=name)
    user_name = user.name
    user_screen_name = user.screen_name
    user_id = user.id_str
    user_followers_count = str(user.followers_count)
    user_friends_count = str(user.friends_count)
    user_tweet_count = str(user.statuses_count)
    user_created_at = str(user.created_at)
    user_lang = user.lang
    user_location = user.location
    user_time_zone = user.time_zone
    print(user_time_zone)
    futures.append(cayley_client.AddQuad(user_id, 'name', user_name))
    futures.append(cayley_client.AddQuad(user_id, 'screen_name', user_screen_name))
    futures.append(cayley_client.AddQuad(user_id, 'followers_count', user_followers_count))
    futures.append(cayley_client.AddQuad(user_id, 'friends_count', user_friends_count))
    futures.append(cayley_client.AddQuad(user_id, 'tweet_count', user_tweet_count))
    futures.append(cayley_client.AddQuad(user_id, 'created_at', user_created_at))
    futures.append(cayley_client.AddQuad(user_id, 'lang', user_lang))
    futures.append(cayley_client.AddQuad(user_id, 'location', user_location))
    futures.append(cayley_client.AddQuad(user_id, 'time_zone', user_time_zone))
    futures.append(cayley_client.AddQuad(user_id, 'user_update_date', str(datetime.now().date())))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(futures))
    # print(futures)
    if depth >= 3:
        LOGGER.info('Max depth reached!')
        return
    depth += 1
    pages = tweepy.Cursor(api.followers, user_id=user_id, count=200).pages()
    while True:
        try:
            for page in pages:
                LOGGER.info('new page')
                futures = []
                for follower in page:
                    follower_name = follower.name
                    follower_screen_name = follower.screen_name
                    follower_id = follower.id_str
                    LOGGER.info('follower' + follower_screen_name)

                    response = client.Send(g.Vertex(follower_id).In('followers_update_date').All()).result['result']
                    if response is not None:
                        update_date = response[0]['id']
                        update_date = datetime.strptime(update_date, '%Y-%m-%d')
                        days_past = (datetime.now() - update_date).days
                    else:
                        days_past = 999

                    if follower_id in searched_ids or days_past < 30:
                        LOGGER.info('Skipping already searched name' + follower_screen_name)
                        continue

                    futures.append(cayley_client.AddQuad(follower_id, 'follows', user_id))
                    # loop = asyncio.get_event_loop()
                    # loop.run_until_complete(asyncio.wait(futures))
                    # print(futures)
                    find_followers(follower_name, cayley_client, follower, depth=depth)

            searched_ids.append(name)
            futures.append(cayley_client.AddQuad(str(datetime.now().date()), 'followers_update_date', user_id))
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(futures))
            break
        except tweepy.TweepError as e:
            LOGGER.info('Tweep error')
            LOGGER.error(e.reason)
            sleep(5)
            continue

        except IOError as e:
            LOGGER.info('IOError')
            LOGGER.error(e.strerror)
            sleep(60)
            continue

        except StopIteration:
            break


find_followers(myName, client)
