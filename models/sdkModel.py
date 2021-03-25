import redis
cache = redis.Redis(host='localhost', port=6379)

def saveSdkImps(sdk):
    try:
        cache.hincrby('sdk:'+sdk, 'impressions',1)
    except:
         return "failed to save "

def saveSdkReqs(sdk):
    try:
        cache.hincrby('sdk:'+sdk, 'requests',1)
    except :
         return "failed to save "

def getSdkImps(sdk):
    try:
        imps =cache.get("sdk:" + sdk,"impressions").decode("utf-8")
        return imps
    except:
        return -1

def getSdkReqs(sdk):
    try:
        reqs = cache.get("sdk:" + sdk,"requests").decode("utf-8")
        return reqs
    except:
        return -1

def getAllSdks():
    try:
        return cache.keys("*sdk*").decode("utf-8")
    except:
        return {}