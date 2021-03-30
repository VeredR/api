import redis
cache = redis.Redis(host='localhost', port=6379)

def saveSdkImps(sdk):
    try:
        if cache.exists('sdk:'+str(sdk)):
            cache.hincrby('sdk:'+str(sdk), 'impressions',1)
        elif not cache.exists('sdk:'+sdk):
            cache.hset('sdk:'+sdk,'impressions',1,'requests',0)
    except:
         return "failed to save "

def saveSdkReqs(sdk):
    try:
        if cache.exists('sdk:'+sdk):
            cache.hincrby('sdk:'+sdk, 'requests',1)
        elif not cache.exists('sdk:'+sdk):
            cache.hset('sdk:'+sdk,'requests',1,'impressions',0)
    except:
         return "failed to save "

def getSdkImps(sdk):
    try:
        imps =cache.hget(sdk,"impressions")
        return imps.decode("utf-8")
    except:
        return -1

def getSdkReqs(sdk):
    try:
        reqs = cache.hget(sdk,"requests")
        return reqs.decode("utf-8")
    except:
        return -1

def getAllSdks():
    try:

        sdks ={}
        for sdk in cache.scan_iter("sdk*"):
            sdk = sdk.decode('utf-8')
            imps = getSdkImps(sdk)
            reqs = getSdkReqs(sdk)
            key = sdk[4:]
            
            sdks.append(key)
            sdks[key].append("impressions", imps)
            sdks[key].append("ad-requests", reqs)
        return sdks
    except:
        return -1