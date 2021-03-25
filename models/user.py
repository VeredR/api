import redis
cache = redis.Redis(host='localhost', port=6379)


def saveUserImps(user):
    try:
        cache.hincrby('user:'+user, 'impressions',1)
    except:
         return "failed to save "

def saveUserReqs(user):
    try:
        cache.hincrby('user:' + user, 'requests',1)
    except:
         return "failed to save "

def getUserReqs(user):
    try:
        reqs = cache.get('user:'+user,"requests").decode("utf-8")
        return reqs
    except:
        return -1

def getUserImps(user):
    try:
        imps = cache.get('user:'+user,"impressions").decode("utf-8")
        return imps
    except:
        return -1

def getAllUsers():
    try:
        return cache.keys("*user*").decode("utf-8")
    except:
        return {}
