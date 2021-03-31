import redis
from api import errors

from . import dao

cache = dao.getCache()

def saveUserImps(user):
    try:
        if cache.exists('user:'+user):
            cache.hincrby('user:' + user, 'impressions',1)
        elif not cache.exists('user:'+user):
            cache.hincrby('user:' + user, 'impressions',1)
            cache.hincrby('user:' + user,'requests',0)
    except Exception as e:
         return errors.error_response(412,e)  

def saveUserReqs(user):
    try:
        if cache.exists('user:'+user):
            cache.hincrby('user:' + user, 'requests',1)
        elif not cache.exists('user:'+user):
            cache.hincrby('user:' + user, 'requests',1)
            cache.hincrby('user:' + user,'impressions',0)
    except Exception as e:
         return errors.error_response(412,e)  

def getUserReqs(user):
    try:
        reqs = cache.hget(user,"requests")
        return int(reqs.decode("utf-8"))
    except:
        return -1

def getUserImps(user):
    try:
        imps = cache.hget(user,"impressions")
        return int(imps.decode("utf-8"))
    except:
        return -1

def getAllUsers():
    try:
        users = {}
        for useri in cache.scan_iter("user*"):
            if useri:
                user = {}
                useri = useri.decode('utf-8')
                imps = getUserImps(useri)
                reqs = getUserReqs(useri)
                key = useri[5:]
                user = {key:{"user-name":key,"impressions":imps,"ad-requests":reqs}}
                users.update(user)
            elif useri is None:
                break
        if users:
            return users
        elif not users:
            return -1
    except Exception as e:
        
        return errors.error_response(412,e) 
