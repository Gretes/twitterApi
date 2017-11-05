from pymongo import MongoClient
from pprint import pprint

client = MongoClient('mongodb://veli:kamil7insan@ds237445.mlab.com:37445/heroku_wzpvdrhs')
db = client['heroku_wzpvdrhs']
collection = db.thy

# dili turkce olan post sayisi
print(collection.find({"lang": "tr"}).count())


for post in collection.find({"lang": "tr"}):
    pprint(post)
