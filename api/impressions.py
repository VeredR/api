''''from app.api import bp

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
 
@app.route('/impression', methods=['PUT'])
def impression():
    if  "sdk" in request.args and "sessionId" in request.args and "platform" in request.args and "user" in request.args and "country-code" in request.args:
       saveImpression(request['user-name'],request['sdk']) 
       app.HTTPResponse(status=200, body="impression saved")  
    elif  not "sdk" in request.args and "sessionId" in request.args and "platform" in request.args and "user" in request.args and "country-code" in request.args:
        app.HTTPResponse(status=400,body = "insufficient args")
    
   
'''