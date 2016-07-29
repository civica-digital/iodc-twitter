import twittertools.db as db
import twittertools.sessions as sessions
import twittertools.calls as calls
import twittertools.tools as tools

try:
    while True:
        next_id = db.get_next_queue()
        calls.user_profile(next_id)
        db.delete_queue(next_id)
except:
    print("Terminó proceso")
