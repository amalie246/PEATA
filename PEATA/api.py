import requests
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=dotenv_path)

class TikTokApi:
    
    def __init__(self):
        self.client_key = os.getenv("CLIENT_KEY")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.access_token = self.obtain_access_token()
        self.BASE_URL = "https://open.tiktokapis.com/v2/research/video/query/"

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
            return json_resp['access_token']
        else:
            print("Something went wrong")
            return 0;
    
    def retrieve_video_data(self):
        #This is just an example of data, should make method more dynamic
        start_date = "20240504" #This is how the date should be formatted
        end_date = "20240528"
        query_params = {
            "fields" : "id,video_description,like_count,region_code", #Can set a lot more fields
            "max_count" : 10,
            "start_date" : start_date,
            "end_date" : end_date
        }
        query_body = {
            "query": {
        "and": [
            {
                "operation": "EQ",
                "field_name": "region_code",
                "field_values": ["NO"]
            },
            {
                "operation": "EQ",
                "field_name": "keyword",
                "field_values": ["politikk"]
            }
            ]
            },
            "start_date" : start_date,
            "end_date" : end_date
        }
        headers = {
            "Content-Type" : "application/json",
            "Authorization" : f"Bearer {self.access_token}"
        }
        
        response = requests.post(self.BASE_URL, json=query_body, params=query_params, headers=headers)
        
        if(response.status_code == 200):
            print("OK")
            data = response.json().get("data", [])
            videos = data.get("videos", [])
            print(videos)
        else:
            print("not ok..")
        
        return 0
    
tiktok = TikTokApi()
access_token = tiktok.access_token #This is how you use the access token
tiktok.retrieve_video_data()