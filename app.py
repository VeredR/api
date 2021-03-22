
from logging import exception
from flask.wrappers import JSONMixin
from flask import Flask, jsonify
from flask import Status
import requests
import redis

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def saveUserImps(userName,):
    try:
        if not cache.exists(userName):#impressions per user
            cache.hset("impressions","user name",userName,1)
        elif cache.exists(userName):
            imps = cache.get(userName) +1
            cache.hset("impressions","user name",userName,imps)
    except:
        return
def saveSdkImps(sdk):
    try:
        if not cache.exists(sdk):#impressions per sdk version
            cache.hset("impressions","SDK Version",sdk,1)

        elif cache.exists(sdk):
            imps = cache.get(sdk) + 1
            cache.hset("impressions","SDK Version",sdk,imps)
    except:
        return
def saveImpression(userName,sdk):
    
    saveUserImps(userName)
    saveSdkImps(sdk)

def saveAdReqPerUser(userName,add):
    try:
        if not cache.exists(userName):#ad req per user
            cache.hset("requests","advertisesment",add,"user name",userName,1)
        elif cache.exists(userName):
            reqs = cache.get(userName) +1
            cache.hset("requests","advertisesment",add,"user name",userName,reqs)
    except:
        return
def saveAdReqPerSdk(sdk,add):
    try:
        if not cache.exists(sdk):#ad req per sdk version
            cache.hset("adds","advertisesment",add,"SDK Version",sdk,1)

        elif cache.exists(add):
            reqs = cache.get(sdk) + 1
            cache.hset("adds","advertisesment",add,"SDK Version",sdk,reqs)
    except:
        return
def saveAdReqs(userName,sdk,add):
    saveUserImps(userName,add)
    saveSdkImps(sdk,add)    

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
    
    imps = cache.hmget("impressions",FilterType)# impressions per filter (user/sdk version)   
    addReqs = cache.hmget("requests",FilterType) # add requests per filter (use/ sdk version)
    fillRate = imps // addReqs
    return jsonify({'impressions':imps,'add-requests':addReqs,'fill-rate':fillRate})

app.run()
