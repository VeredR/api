import redis
cache = redis.Redis(host='localhost', port=6379)


def saveUserImps(user):
    try:
        if cache.exists('user:'+user):
            cache.hincrby('user:' + user, 'impressions',1)
        elif not cache.exists('user:'+user):
            cache.hset('user:' + user, 'impressions',1,'requests',0)

    except:
         return "failed to save "

def saveUserReqs(user):
    try:
        if cache.exists('user:'+user):
            cache.hincrby('user:' + user, 'requests',1)
        elif not cache.exists('user:'+user):
            cache.hset('user:' + user, 'requests',1,'impressions',0)
    except:
         return "failed to save "

def getUserReqs(user):
    try:
        reqs = cache.hget(user,"requests").decode("utf-8")
        return reqs
    except:
        return -1

def getUserImps(user):
    try:
        imps = cache.hget(user,"impressions").decode("utf-8")
        return imps
    except:
        return -1

def getAllUsers():
    try:
        users = {}
        
        for user in cache.scan_iter("user*"):
            user = user.decode('utf-8')
            imps = getUserImps(user)
            reqs = getUserReqs(user)
            key = user[5:]
            users.append(key)
            users[key].append("impressions",imps)
            users[key].append("ad-requests",reqs)
        return users
    except:
        return -1
