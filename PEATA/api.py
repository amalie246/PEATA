import requests
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=dotenv_path)
#access_token = obtain_access_token(CLIENT_KEY, CLIENT_SECRET)
#print(access_token)

class TikTokApi:
    
    def __init__(self):
        self.client_key = os.getenv("CLIENT_KEY")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.access_token = self.obtain_access_token()

    #Obtain a client access token, add this to the authorization header
    def obtain_access_token(self):
        ENDPOINT_URL = "https://open.tiktokapis.com/v2/oauth/token/"
        access_token_headers = {'Content-Type' : 'application/x-www-form-urlencoded', 
                                'Cache-Control' : 'no-cache'}
        req_body_params = {
            'client_key': self.client_key,
            'client_secret': self.client_secret,
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
tiktok = TikTokApi()
access_token = tiktok.obtain_access_token()