from pymongo import MongoClient
import datetime
import os
import time

MONGO_URL = os.environ["mongo_server"]

client = MongoClient(MONGO_URL)

db = client.profiles
tweets = db.tweets
queue = db.queue
keys = db.keys
pending = db.pending

def insert_profile(document):
    tweets.update({"_id":document["_id"]}, document, upsert= True)
    return None

def search_profile(profile_id):
    profile = list(tweets.find({"_id":profile_id}).limit(1))[0]
    return profile

def get_next_queue():
    next_id = list(queue.find({}).limit(1))[0]["_id"]
    return next_id

def delete_queue(id):
    queue.remove({"_id":id})
    return None

def insert_queue(id):
    if type(id) is list:
        for unique_id in id:
            queue.update({"_id":unique_id}, {"_id":unique_id}, upsert= True)
    else:
        queue.update({"_id":id}, {"_id":id}, upsert= True)
    return None

def insert_pending(id):
    if type(id) is list:
        for unique_id in id:
            pending.update({"_id":unique_id}, {"_id":unique_id}, upsert= True)
    else:
        pending.update({"_id":id}, {"_id":id}, upsert= True)
    return None

def insert_key(document):
    keys.update({"_id":document["_id"]}, document, upsert= True)
    return None

def search_last_key():
    last_key = list(keys.find().sort([("last_used",1)]).limit(1))[0]
    return last_key

def search_available_key(field):
    calls_field = field + "_calls"
    epoch_field = field + "_epoch"
    last_key = list(keys.find().sort([(calls_field,-1)]).limit(1))[0]
    if field == "profile":
        limit = 15
    else:
        limit = 0
    if last_key[calls_field] == limit:
        last_key = list(keys.find().sort([(epoch_field,1)]).limit(1))[0]
        epoch_time = last_key[epoch_field]
        now = datetime.datetime.now().timestamp()
        time_delta = epoch_time - now
        print("Waiting "+ str(time_delta) + " seconds for the API key to be available")
        time.sleep(time_delta + 5)
    return last_key

def use_key(session, key_id):
    from twittertools.calls import api_status

    key_info = list(keys.find({"_id":key_id}))[0]
    key_info["last_used"] = datetime.datetime.now()
    api_limits = api_status(session)
    key_info["profile_calls"]= api_limits["profile_calls"]
    key_info["profile_epoch"]= api_limits["profile_epoch"]
    key_info["followers_calls"]= api_limits["followers_calls"]
    key_info["followers_epoch"]= api_limits["followers_epoch"]
    key_info["friends_calls"]= api_limits["friends_calls"]
    key_info["friends_epoch"]= api_limits["friends_epoch"]
    key_info["status_checks_calls"]= api_limits["status_checks_calls"]
    key_info["status_checks_epoch"]= api_limits["status_checks_epoch"]
    keys.update({"_id":key_id}, key_info, upsert= True)
    return None
