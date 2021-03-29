'''from app.api import bp
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

@app.route('/get-ad', methods=['GET'])
def GetAd():
   try:
        if "sdk" in request.args and "sessionId" in request.args and "platform" in request.args and "user" in request.args and "country-code" in request.args:
            r =request.get('https://6u3td6zfza.execute-api.us-east-2.amazonaws.com/prod/ad/vast')# getting XML in a VAST format
            saveAdReqs(request.args['user'],request.args['sdk'])
            return r.json()
        elif not "sdk" in request.args and "sessionId"  in request.args and "platform" in request.args and "user" in request.args and "country-code" in request.args:
            app.HTTPResponse(status=400,body = "wrong input in request or missing")
            return jsonify({})
   except:
        app.HTTPResponse(status=400, body="impression saved")
        '''