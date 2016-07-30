import datetime


def friends_id(user, session):
    from twittertools.db import insert_pending
    print("Getting user friends")
    friends = []
    next_cursor = -1
    recurrent_error_flag = 0
    while next_cursor != 0:
        print("friends request")
        session.switch_keys(False,"friends")
        try:
            if type(user) == int:
                call = session.twitter.friends.ids(user_id=user, cursor = next_cursor)
            else:
                call = session.twitter.friends.ids(screen_name=user, cursor = next_cursor)
            friends= friends + call["ids"]
            next_cursor = call["next_cursor"]
        except Exception as exception:
            if "401" in str(exception):
                insert_pending(user)
                next_cursor = 0
            recurrent_error_flag += 1
            if recurrent_error_flag > 1:
                session.switch_keys(True, "friends")
        session.control_call_count()
    return friends

def followers_id(user, session):
    from twittertools.db import insert_pending
    print("Getting user followers")
    followers = []
    next_cursor = -1
    recurrent_error_flag = 0
    while next_cursor != 0:
        print("followers request")
        session.switch_keys(False,"followers")
        try:
            if type(user) == int:
                call = session.twitter.followers.ids(user_id=user, cursor = next_cursor)
            else:
                call = session.twitter.followers.ids(screen_name=user, cursor = next_cursor)
            followers = followers + call["ids"]
            next_cursor = call["next_cursor"]
        except Exception as exception:
            if "401" in str(exception):
                insert_pending(user)
                next_cursor = 0
            recurrent_error_flag += 1
            if recurrent_error_flag > 1:
                session.switch_keys(True, "followers")
        session.control_call_count()
    return followers

def call_user_screenname(user, session, input_max_id = None):
    from twittertools.db import insert_pending
    response = False
    recurrent_error_flag = 0
    session.switch_keys(False, "profile")
    output = []
    while response == False:
        print("timeline request")
        try:
            if type(user) == int:
                if input_max_id is None:
                    output = session.twitter.statuses.user_timeline(user_id=user, count=200)
                else:
                    output = session.twitter.statuses.user_timeline(user_id=user, count=200, max_id = input_max_id )
            else:
                if input_max_id is None:
                    output = session.twitter.statuses.user_timeline(screen_name=user, count=200)
                else:
                    output = session.twitter.statuses.user_timeline(screen_name=user, count=200, max_id = input_max_id)
            response= True
        except Exception as exception:
            if "401" in str(exception):
                insert_pending(user)
                response = True
            recurrent_error_flag += 1
            if recurrent_error_flag > 1:
                session.switch_keys(True, "profile")
    session.control_call_count()
    return output

def extract_user_profile(full_timeline):
    i = 0
    profile = None
    if len(full_timeline) > 0:
        while profile == None:
            if full_timeline[i]["retweeted"] == False:
                profile = full_timeline[i]["user"]
            i = i + 1
    else:
        profile = []
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
    print("Researching "+str(user)+"...")
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

def api_status(session):
    api_current = session.twitter.application.rate_limit_status()
    resources = api_current["resources"]
    output = {}
    output["profile_calls"]= resources["statuses"]["/statuses/user_timeline"]["remaining"]
    output["profile_epoch"]= resources["statuses"]["/statuses/user_timeline"]["reset"]
    output["followers_calls"]= resources["followers"]["/followers/ids"]["remaining"]
    output["followers_epoch"]= resources["followers"]["/followers/ids"]["reset"]
    output["friends_calls"]= resources["friends"]["/friends/ids"]["remaining"]
    output["friends_epoch"]= resources["friends"]["/friends/ids"]["reset"]
    output["status_checks_calls"]= resources["application"]["/application/rate_limit_status"]["remaining"]
    output["status_checks_epoch"]= resources["application"]["/application/rate_limit_status"]["reset"]
    return(output)
