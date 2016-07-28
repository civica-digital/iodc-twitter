import time
import db

from twitter import *

import tools

def get_key():
    last_key = db.search_last_key()
    db.use_key(last_key["_id"])
    return last_key

class session:

    def __init__(self):
        keys = get_key()
        self.twitter = Twitter(auth = OAuth(keys["token"], keys["token_key"], keys["con_secret"], keys["con_secret_key"]))

    def switch_keys(self, halt):
        print("Switching Keys...")
        if halt == True:
            "[Overall rate limit reached, waiting for one minute]"
            time.sleep(60)
        keys = get_key()
        self.twitter = Twitter(auth = OAuth(keys["token"], keys["token_key"], keys["con_secret"], keys["con_secret_key"]))

def main():
    with open("accounts.csv", "r") as ins:
        accounts = []
        for line in ins:
            line = line.replace("\n","")
            accounts.append(line.split(","))
    accounts.pop(0)
    for account in accounts:
        document = tools.key_document(account)
        db.insert_key(document)
    print("Migration Finished")
    return None

if __name__ == "__main__":
    main()
