from api.errors import error_response
import redis
from api import errors
cache = redis.Redis(host='localhost', port=6379)

def saveSdkImps(sdk):
    try:
        if cache.exists('sdk:'+sdk):
            cache.hincrby('sdk:'+sdk, 'impressions',1)
          
        elif not cache.exists('sdk:'+sdk):
            cache.hincrby('sdk:'+sdk, 'impressions',1)
            cache.hset('sdk:'+sdk,'requests',0)
    except Exception as e:
         return errors.error_response(412,e)  

def saveSdkReqs(sdk):
    try:
        if cache.exists('sdk:'+sdk):
            cache.hincrby('sdk:'+sdk, 'requests',1)
        elif not cache.exists('sdk:'+sdk):
            cache.hincrby('sdk:'+sdk,'requests',1)
            cache.hset('sdk:'+sdk,'impressions',0)
    except Exception as e:
         return errors.error_response(412,str(e))  

def getSdkImps(sdk):
    try:
        imps =cache.hget(sdk,"impressions")
        return int(imps.decode("utf-8"))
    except:
        return -1

def getSdkReqs(sdk):
    try:
        reqs = cache.hget(sdk,"requests")
        return int(reqs.decode("utf-8"))
    except:
        return -1

def getAllSdks():
    try:
        sdks ={}
        for sdki in cache.scan_iter("sdk*"):
            sdk = {}
            sdki= sdki.decode('utf-8')
            imps = getSdkImps(sdki)
            reqs = getSdkReqs(sdki)
            key = sdki[4:]
            sdk = {key:{"sdk-version":key,"impressions":imps,"ad-requests":reqs}}
            sdks.update(sdk)
            
        if sdks:    
            return sdks
        elif not sdks:
            return -1

    except Exception as e:
        return errors.error_response(412,e) 