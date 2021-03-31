import redis
import os

redis_host = os.getenv('redisHost','localhost')
redis_port = os.getenv('redisPort',6379)

cache = redis.Redis(host=redis_host, port=redis_port)

def getCache():
    return cache