import datetime

def key_document(account):
    account_document = {
        "_id":account[0],
        "con_secret":account[2],
        "con_secret_key":account[3],
        "token":account[4],
        "token_key":account[5],
        "last_used":datetime.datetime.now()
    }
    return account_document
