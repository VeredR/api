# api
Docker REST API written in Python with Flask and Redis modules 

# Design:

dao - represents the data access object, in our case the redis cache
models: 
for each entity(user, sdkModel) with the same functions inside the code to establish seperation.

controller called app, gets all the http requests:

1. the first function is a get request (retrieves the vast format xml)
2. the second function is a post request (because it sends impression data and saves it, not retrieving data but http 200 response)
3. the third function is a get request because we retrive the impressions, requests and fill rate for each user/sdk version


# Three functions:

1. get-add: 
gets an XML of VAST format, and saving the add request per user and sdk version.

the url to check if it works should look like this: (this is not a secure env, since it runs localy)
http://localhost:5000/get-ad?user=[USER_NAME]&sdk=[SDK_VERSION]&country-code=[COUNTRY_CODE]&seesionId=[SESSION_ID]&platform=[PLATFORM]

where [SOMETHING] is the string / number you should enter to check

2. impression: 
saving impression and on success returning 200 

the url to check if it works should look like this: (this is not a secure env, since it runs localy)
http://localhost:5000/impression?user=[USER_NAME]&sdk=[SDK_VERSION]&country-code=[COUNTRY_CODE]&seesionId=[SESSION_ID]&platform=[PLATFORM]

where [SOMETHING] is the string / number you should enter to check

3. get-stat: 
getting a json per user/sdk of the user name/ sdk version (depending on the filterType) 
and the number of impressions, ad requests, and fill rate (impressions/requests) per user name/sdk version.

the url to check if it works should look like this: (this is not a secure env, since it runs localy)
http://localhost:5000/get-stat?filterType=[FILTER_TYPE]

where [FILTER_TYPE] is the string you should enter to get either users or sdks data

# General Settings:
1. Flask port is 5000 (default)
2. Redis port is 6379 (default)

