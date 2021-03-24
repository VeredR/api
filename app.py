
from logging import exception
from flask.wrappers import JSONMixin
from flask import Flask, jsonify
from flask import Status
import requests
import redis

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def saveUserImps(userName):
    try:
        cache.hincrby('user:'+userName, 'impressions',1)
    except:
        return "failed to save"
def saveSdkImps(sdk):
    try:
        cache.hincrby('sdk:'+sdk, 'impressions',1)
    except:
         return "failed to save"
def saveImpression(userName,sdk):
    
    saveUserImps(userName)
    saveSdkImps(sdk)

def saveAdReqPerUser(userName):
    try:
        cache.hincrby('user:'+userName, 'requests',1)
    except:
         return "failed to save"
def saveAdReqPerSdk(sdk):
    try:
        cache.hincrby('sdk:'+sdk, 'requests',1)
    except:
         return "failed to save"

def saveAdReqs(userName,sdk):
    saveUserImps(userName)
    saveSdkImps(sdk)    

'''
GetAd

Request
SDK Version 
SessionId
Platform
User name
Country code
Logic 
Send a GET request to the following endpoint and get an XML in a  VAST ad format 
https://6u3td6zfza.execute-api.us-east-2.amazonaws.com/prod/ad/vast
Save/increment in an external database/key-value store how many ad requests per user
Save/increment in an external database/key-value store how many ad requests per SDK version
Response
Return the XML as it was returned from the external API 

'''
@app.route('/get-ad', methods=['GET'])
def GetAd(request):
    if request:
        r =requests.get('https://6u3td6zfza.execute-api.us-east-2.amazonaws.com/prod/ad/vast')# getting XML in a VAST format
        saveAdReqs(request['user-name'],request['sdk'])
        return r
    elif not request:
        return 'wrong input in request or missing'
    


        
    
''''
Impression
Request
SDK Version 
SessionId
Platform
User name
Country code
Logic 
Save/increment in an external database/key-value store how many Impressions per user
Save/increment in an external database/key-value store how many Impressions per SDK version
As a response returns HTTP 200
'''   
@app.route('/impression', methods=['GET'])
def Impression(request):
    if request:
       saveImpression(request['user-name'],request['sdk'])
        
    elif not request:
        return Status.HTTP_400_BAD_REQUEST
    
    return app.HTTPResponse(status=200, body="impression saved")

def getUserImps(users):
    try:
        imps = 0
        for user in users:
            imps+=cache.get(user,"impressions").decode("utf-8")
        return imps
    except:
        return -1
def getSdkImps(sdks):
    try:
        imps = 0
        for sdk in sdks:
            imps+=cache.get(sdk,"impressions").decode("utf-8")
        return imps
    except:
        return -1
def getUserReqs(users):
    try:
        reqs = 0
        for user in users:
            reqs+=cache.get(user,"requests").decode("utf-8")
        return reqs
    except:
        return -1
def getSdkReqs(sdks):
    try:
        reqs = 0
        for sdk in sdks:
            reqs+=cache.get(sdk,"requests").decode("utf-8")
        return reqs
    except:
        return -1
''' 
GetStats
Request
FilterType
Can be either user or SDK version
Logic
Retrieve from the database/key-value store the relevant information based on the input filter type
Calculate:
Impressions per User/SDKVersion
Ad requests per User/SDKVersion
Fill rate (= Impressions/Ad requests) User/SDKVersion
Response
Returns the calculated values about as a JSON object
 '''
@app.route('/get-stat', methods=['GET'])
def GetStats(FilterType):
    try:
        imps = 0
        reqs = 0
        fillRate = 0.0
        if FilterType == 'user':
            keys = cache.keys("*"+FilterType+"*").decode("utf-8")
            imps = getUserImps(keys)
            reqs = getUserReqs(keys)
        elif FilterType == "SDK version":
            keys = cache.keys("*sdk*").decode("utf-8")
            imps = getSdkImps(keys)
            reqs = getSdkReqs(keys)
        
        fillRate = imps // reqs
        return jsonify({'impressions':imps,'add-requests':reqs,'fill-rate':fillRate})
    except:
        return "something went wrong"
app.run()
