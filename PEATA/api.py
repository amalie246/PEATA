import requests
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CLIENT_KEY = os.getenv("CLIENT_KEY")
ENDPOINT_URL = "https://open.tiktokapis.com/v2/oauth/token/"

#Obtain a client access token, add this to the authorization header
def obtain_access_token(client_key, client_secret):
    access_token_headers = {'Content-Type' : 'application/x-www-form-urlencoded', 
                            'Cache-Control' : 'no-cache'}
    req_body_params = {
        'client_key': CLIENT_KEY,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }

    response = requests.post(ENDPOINT_URL, headers=access_token_headers, data=req_body_params)
    
    if response.status_code == 200:
        print(response.status_code)
        print(response.json())
        
        json_resp = response.json();
        return 0; #return json_resp['access_token']
    else:
        print("Something went wrong")
        return 0;

    
access_token = obtain_access_token(CLIENT_KEY, CLIENT_SECRET)