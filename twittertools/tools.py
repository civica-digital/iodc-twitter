import datetime

def key_document(account):
    account_document = {
        "_id":account[2],
        "con_secret":account[4],
        "con_secret_key":account[5],
        "token":account[6],
        "token_key":account[7],
        "last_used":datetime.datetime.now(),
        "profile_calls": 180,
        "profile_epoch": datetime.datetime.now().timestamp(),
        "followers_calls": 15,
        "followers_epoch": datetime.datetime.now().timestamp(),
        "friends_calls": 15,
        "friends_epoch": datetime.datetime.now().timestamp(),
        "status_checks_calls":180,
        "status_checks_epoch": datetime.datetime.now().timestamp()
    }
    return account_document
