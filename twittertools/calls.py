import datetime

def friends_id(user, session):
    print("Getting user friends")
    friends = []
    next_cursor = -1
    while next_cursor != 0:
        print("friends request")
        recurrent_error_flag = 0
        try:
            call = session.twitter.friends.ids(screen_name=user, cursor = next_cursor)
            friends= friends + call["ids"]
            next_cursor = call["next_cursor"]
        except:
            recurrent_error_flag += 1
            if recurrent_error_flag > 1:
                session.switch_keys(True)
            else:
                session.switch_keys(False)
    return friends

def followers_id(user, session):
    print("Getting user followers")
    followers = []
    next_cursor = -1
    while next_cursor != 0:
        print("followers request")
        recurrent_error_flag = 0
        try:
            call = session.twitter.followers.ids(screen_name=user, cursor = next_cursor)
            followers = followers + call["ids"]
            next_cursor = call["next_cursor"]
        except:
            recurrent_error_flag += 1
            if recurrent_error_flag > 1:
                session.switch_keys(True)
            else:
                session.switch_keys(False)
    return followers

def call_user_screenname(user, session, input_max_id = None):
    response = False
    recurrent_error_flag = 0
    while response == False:
        print("timeline request")
        try:
            if type(user) == int:
                if input_max_id is None:
                    return session.twitter.statuses.user_timeline(user_id=user, count=200)
                else:
                    return session.twitter.statuses.user_timeline(user_id=user, count=200, max_id = input_max_id )
            else:
                if input_max_id is None:
                    return session.twitter.statuses.user_timeline(screen_name=user, count=200)
                else:
                    return session.twitter.statuses.user_timeline(screen_name=user, count=200, max_id = input_max_id)
        except:
            recurrent_error_flag += 1
            if recurrent_error_flag > 0:
                session.switch_keys(True)
            else:
                session.switch_keys(False)
    return None

def extract_user_profile(full_timeline):
    i = 0
    profile = None
    while profile == None:
        if full_timeline[i]["retweeted"] == False:
            profile = full_timeline[i]["user"]
        i = i + 1
    return profile

def timeline(user, session):
    print("Retrieving user timeline...")
    user_timeline = call_user_screenname(user, session)
    full_timeline = user_timeline
    while len(user_timeline)!=0:
        last_tweet = full_timeline[-1]["id"] - 1
        user_timeline = call_user_screenname(user, session, last_tweet)
        full_timeline = full_timeline + user_timeline
    user_info = extract_user_profile(full_timeline)
    return full_timeline, user_info

def user_profile(user, session):
    print("Researching "+user+"...")
    user_timeline, user_info = timeline(user, session)
    profile = {
        "_id": user,
        "info": user_info,
        "timeline": user_timeline,
        "followers": followers_id(user, session),
        "friends": friends_id(user, session),
        "updated": datetime.datetime.now()
        }
    print("Profile Finish")
    return profile
