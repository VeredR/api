#from logging import exception
#from flask.wrappers import JSONMixin
from flask import Flask, jsonify, request
import requests
from api.models import user 
from api.models import sdkModel 
from api import errors


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
        url = "https://6u3td6zfza.execute-api.us-east-2.amazonaws.com/prod/ad/vast"
        r = {}
        r = requests.get(url)
        
        return r.content.decode('utf8')
    except requests.exceptions.ConnectionError as e:
        if not r: 
            return errors.error_response(e.errno,e.strerror)  
   



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
                    return app.make_response(rv = req)
            elif not req:
                return errors.error_response(412,"No VAST Retrived")
        elif len(request.args) != 5 or not "user"  in request.args or not "sdk" in request.args:
            return errors.bad_request("wrong input in request or missing")

    except Exception as e:
        
        return errors.bad_request(str(e))
        
        
    
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
@app.route('/impression', methods=['POST'])
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
        
        if "filterType" in request.args:
            if request.args["filterType"] == 'user':
               users = user.getAllUsers()
               if users != -1:
                    for useri in users:
                        imps = useri["impressions"]
                        reqs = useri["ad-requests"]
                        fillRate = imps // reqs
                        useri['fill-rate']= fillRate
                    return app.make_response(rv=users)
               elif users == -1:
                    return errors.error_response(412,"no users to calculate")
                    
            elif request.args["filterType"] == "sdk":
                sdks = sdkModel.getAllSdks()
                if sdks != -1:
                    for sdk in sdks:
                        imps = sdk["impressions"]
                        reqs = sdk["ad-requests"]
                        fillRate = imps // reqs
                        sdk.append('fill-rate',fillRate)
                    return app.make_response(rv=jsonify(sdks))
                elif sdks == -1:
                    errors.error_response(412,"no sdks to calculate")
                
            
    except Exception as e:
        return errors.error_response(e)


app.run()
