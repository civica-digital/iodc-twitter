from pymongo import MongoClient
import datetime
import os

MONGO_URL = os.environ["mongo_server"]

client = MongoClient(MONGO_URL)

db = client.profiles
tweets = db.tweets
queue = db.queue
keys = db.keys

def insert_profile(document):
    tweets.update({"_id":document["_id"]}, document, upsert= True)
    return None

def search_profile(profile_id):
    profile = list(tweets.find({"_id":profile_id}).limit(1))[0]
    return profile

def get_next_queue():
    next_id = db.queue.find({}).limit(1)
    return next_id

def delete_queue(id):
    queue.remove({"_id":id})
    return None

def insert_queue(id):
    if type(id) is list:
        for unique_id in id:
            queue.update({"_id":unique_id}, {"_id":unique_id}, upsert= True)
    else:
        queue.update({"_id":id}, {"_id":unique_id}, upsert= True)
    return None

def insert_key(document):
    keys.update({"_id":document["_id"]}, document, upsert= True)
    return None

def search_last_key():
    last_key = list(keys.find().sort([("last_used",1)]).limit(1))[0]
    return last_key

def use_key(key_id):
    key_info = list(keys.find({"_id":key_id}))[0]
    key_info["last_used"] = datetime.datetime.now()
    keys.update({"_id":key_id}, key_info, upsert= True)
    return None
