from twittertools.db import insert_profile, delete_queue, get_next_queue
import twittertools.sessions as sessions
from twittertools.calls import user_profile
import os

os.environ["mongo_server"] = "192.168.99.100:32768"
twitter_session = sessions.session()
next_id = get_next_queue()
current_profile = user_profile(next_id, twitter_session)
insert_profile(current_profile)
delete_queue(next_id)

try:
    while True:
        next_id = get_next_queue()
        current_profile = user_profile(next_id, twitter_session)
        insert_profile(current_profile)
        delete_queue(next_id)
except:
    print("Terminó proceso")
