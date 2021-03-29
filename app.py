from logging import exception
from flask.wrappers import JSONMixin
from flask import Flask, jsonify, request
import requests
from time import sleep
#from api import app
from api.models import user 
from api.models import sdkModel 
from api import errors
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry



#import os 
 

app = Flask(__name__)

def saveImpression(userName,sdk):
    try:
        user.saveUserImps(userName)
        sdkModel.saveSdkImps(sdk)
        return True
    except:
         return False


def saveAdReqs(userName,sdk):
    try:
        user.saveUserReqs(userName)
        sdkModel.saveSdkReqs(sdk)
        return True
    except:
         return False    

def sendRequest():
    try:
        url = 'https://6u3td6zfza.execute-us-east-2.amazonaws.com/prod/ad/vast'
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        r = session.get(url)
        return r.json()
    except requests.exceptions.ConnectionError:
        r.status_code == "Connection refused"
        return False
   



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
https://6u3td6zfza.execute-us-east-2.amazonaws.com/prod/ad/vast
Save/increment in an external database/key-value store how many ad requests per user
Save/increment in an external database/key-value store how many ad requests per SDK version
Response
Return the XML as it was returned from the external API 

'''
@app.route('/get-ad', methods=['GET'])
def GetAd():
   
    try:
        if len(request.args) == 5 and 'sdk' in request.args and "user" in request.args: 
            req = sendRequest()
            if req:# XML in a VAST format in a json format
                if saveAdReqs(request.args['user'],request.args['sdk']):
                    return app.HTTPResponse(status=200,body = r)
            elif not req:
                return errors.error_response(412)
        elif len(request.args) != 5 or not "user"  in request.args or not "sdk" in request.args:
            return errors.bad_request("wrong input in request or missing")

    except Exception as e:
        
        return errors.bad_request(e)#app.HTTPResponse(status=400, body="could not save ad-request or get the add")
        
        
    
'''
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
@app.route('/impression', methods=['POST'],)
def impression():
    if  len(request.args) == 5 and "sdk" in request.args and "user" in request.args:
        if saveImpression(request.args['user'],request.args['sdk']): 
            return app.make_response(rv="impression saved") 
        else:
            return errors.bad_request("could not save impression")
    elif len(request.args) != 5 or not "sdk" in request.args or not "user" in request.args:
        return errors.bad_request("insufficient args")
    
   






''' 
GetStats
Request
FilterType
Can be either user or SDK version
Logic
Retrieve from the database/key-value store the relevant information based on the input filter type
Calculat:
Impressions per User/SDKVersion
Ad requests per User/SDKVersion
Fill rate (= Impressions/Ad requests) User/SDKVersion
Response
Returns the calculated values about as a JSON object
 '''
@app.route('/get-stat', methods=['GET'])
def GetStats():
    try:
        
        ans = {}
        if "filterType" in request.args:
            if request.args["filterType"] == 'user':
               users = user.getAllUsers()
               if users:
                    for useri in users:
                        ans[useri[5:]] ={}
                        imps = user.getUserImps(useri)
                        ans[useri[5:]].append('impressions',imps)
                        reqs = user.getUserReqs(useri)
                        ans[useri[5:]].append('add-requests',reqs)
                        fillRate = imps // reqs
                        ans[useri[5:]].append('fill-rate',fillRate)
               elif not users:
                    return errors.error_response(412,"no users to calculate")
                    
            elif request.args["filterType"] == "sdk":
                sdks = sdkModel.getAllSdks()
                if sdks:
                    for sdki in sdks:
                        
                        imps = sdkModel.getSdkImps(sdki)
                        reqs = sdkModel.getSdkReqs(sdki)
                        fillRate = imps // reqs
                        ans[sdki] = {'impressions':imps,'add-requests':reqs,'fill-rate':fillRate}
                elif not sdks:
                    errors.error_response(412,"no sdks to calculate")
                
            return app.make_response(rv=jsonify(ans))
    except Exception as e:
        return errors.error_response(e)


app.run()
