from pymongo import MongoClient
import datetime
from pprint import pprint

client = MongoClient('mongodb://veli:kamil7insan@ds237445.mlab.com:37445/heroku_wzpvdrhs')
db = client['heroku_wzpvdrhs']
collection = db.bein1

# dili turkce olan post sayisi
# print(collection.find({"lang": "tr"}).count())

created_at = collection.find_one(sort=[["id", -1]])["created_at"]
print(datetime.datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y').strftime("%Y-%m-%d %H:%M:%S"))

# for post in collection.find():
#     pprint(post)