import time

from twitter import *

import twittertools.db as db
import twittertools.tools as tools


class session:

    def __init__(self):
        keys = db.search_last_key()
        self.twitter = Twitter(auth = OAuth(keys["token"], keys["token_key"], keys["con_secret"], keys["con_secret_key"]))
        self.current_key = keys["_id"]


    def switch_keys(self, halt, field):
        if halt == True:
            print("[Manually reached an error from API, switching keys after 15 minutes]")
            time.sleep(900)
        keys = db.search_available_key(field)
        self.twitter = Twitter(auth = OAuth(keys["token"], keys["token_key"], keys["con_secret"], keys["con_secret_key"]))
        self.current_key = keys["_id"]
        print(self.current_key)

    def control_call_count(self):
        db.use_key(self, self.current_key)
        return None


def main():
    with open("twittertools/accounts.csv", "r") as ins:
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
