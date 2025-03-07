import requests
from dotenv import load_dotenv
import os
import json
import csv

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=dotenv_path)
BASE_URL = "https://open.tiktokapis.com/v2"

class TikTokApi:
    
    def __init__(self):
        self.client_key = os.getenv("CLIENT_KEY")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.access_token = self.obtain_access_token()
        
        self.VIDEO_QUERY_URL = BASE_URL + "/research/video/query/"
        self.USER_INFO_URL = BASE_URL + "/research/user/info/"
        self.VIDEO_COMMENTS_URL = BASE_URL + "/research/video/comment/list/"

        
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

    
    #This method only is able to get username AND keyword, in a EQ operation
    #Also only returns 100 videos, needs to handle pagination
    def get_videos(self, username, keyword, startdate, enddate):
        #All fields, NOTE TO SELF: Remove unneccesary fields if needed
        query_params = {
                "fields" : "id,video_description,create_time,region_code,share_count,view_count,like_count,comment_count,music_id,hashtag_names,username,effect_ids,playlist_id,voice_to_text,is_stem_verified,video_duration,hashtag_info_list,video_mention_list,video_label",
                "max_count" : 100,
                "start_date" : startdate,
                "end_date" : enddate
        }
        
        #EQ, IN, GT/GTE, LT/LTE, can also combine these..
        query_body = {
            "query":   {
                    "and" : [{
                            "operation" : "EQ",
                            "field_name" : "keyword",
                            "field_values" : [f"{keyword}"]
                        }, {
                            "operation" : "EQ",
                            "field_name" : "username",
                            "field_values" : [f"{username}"]
                        }]
                },
                "start_date" : startdate,
                "end_date" : enddate
        }
                            
        headers = {
                "Content-Type" : "application/json",
                "Authorization" : f"Bearer {self.access_token}"
            }
        
        does_have_more = True
        all_videos = []
        
        while does_have_more:
            response = requests.post(self.VIDEO_QUERY_URL, json=query_body, params=query_params, headers=headers)

            if response.status_code == 200:
                data = response.json().get("data", [])
                videos = data.get("videos", [])
                all_videos.extend(videos)
                
                check_pagination = data["has_more"]
                
                if check_pagination == False:
                    break
                
            else:
                print(response.json())
                
        print(all_videos)
        print("Amount of videos retrieved: %d" % (len(all_videos)))
        return all_videos
        

    
    def get_videos_by_dynamic_query_body(self, query_body, start_date, end_date):
        query_params = {
                "fields" : "id,video_description,create_time,region_code,share_count,view_count,like_count,comment_count,music_id,hashtag_names,username,effect_ids,playlist_id,is_stem_verified,video_duration,hashtag_info_list,video_mention_list,video_label",
                "max_count" : 100,
                "start_date" : start_date,
                "end_date" : end_date
        }
        
        headers = {
                "Content-Type" : "application/json",
                "Authorization" : f"Bearer {self.access_token}"
        }
        
        does_have_more = True
        all_videos = []
        
        while does_have_more:
            response = requests.post(self.VIDEO_QUERY_URL, json=query_body, params=query_params, headers=headers)
            
            if response.status_code == 200:
                data = response.json().get("data", [])
                videos = data.get("videos", [])
                all_videos.extend(videos)
                
                check_pagination = data["has_more"]
                if check_pagination == False:
                    break
            else:
                print(response.json())
        
        print(all_videos)
        print("Amount of videos retrieved: %d" % (len(all_videos)))
        return all_videos
        
        
        

    #Edge case - extreme long processing time for many comments!
    def get_video_comments(self, video_id):
        url = f"{self.VIDEO_COMMENTS_URL}?fields=id,like_count,create_time,text,video_id,parent_comment_id"
        
        headers = {
            "Content-Type" : "application/json",
            "Authorization" : f"Bearer {self.access_token}"
        }
    
        data = {
            "video_id" : video_id,
           "max_count" : 100,
           "cursor": 0
            
        }
        all_comments = []
        iteration = 0
        
        #TODO this is a max count for comments set at 400..
        does_have_more = True
        while does_have_more:
            iteration = iteration + 1
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                comments = response.json()
                all_comments.extend(comments["data"]["comments"])
                
                check_pagination = comments["data"]["has_more"]
                
                if check_pagination == False:
                    break
                if iteration == 4:
                    break
            
        print(all_comments)
        print("Amount of comments: %d" % (len(all_comments)))
        return all_comments
    
   
    
   #har lyst til å få denne til å funke
    def get_music_info(self, music_id):
        url = f"{BASE_URL}/research/music/query/"
        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {self.access_token}"
    }
        data = {
        "query": {
            "and": [
                {"operation": "EQ", "field_name": "id", "field_values": [music_id]}
            ]
        },
        "fields": "id,title,author_name,album_name,cover_url,duration",
        "max_count": 1 
    }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            print(f"Feil ved henting av musikkinfo (status {response.status_code}): {response.text}")
        return None
        try:
            json_response = response.json()
            if not json_response or "data" not in json_response:
                print("Feil: Ingen data returnert fra API-et.")
            return None
            music_data = json_response["data"].get("music", [])
            if not music_data:
                print("Ingen musikk funnet for denne ID-en.")
            return None
            return music_data[0]
        except requests.exceptions.JSONDecodeError:
            print("JSONDecodeError: API-et returnerte ikke gyldig JSON.")
            print("Rå respons fra API:", response.text)
        return None


    
    def get_public_user_info(self, username):
        #Get user info with get_videos_dynamic_params
        
        #can switch out fields to let user choose this themselves, although not needed at this moment
        url = f"{self.USER_INFO_URL}?fields=display_name,bio_description,avatar_url,is_verified,follower_count,following_count,likes_count,video_count"
        
        headers = {
            "Content-Type" : "application/json",
            "Authorization" : f"Bearer {self.access_token}"
        }
        
        data = {
            "username" : username
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if(response.status_code == 200):
            user_info = response.json();
            print(user_info)
            return user_info
        else:
            return "Invalid"
