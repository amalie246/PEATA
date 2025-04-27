import requests
import os
import json
import csv
import logging

BASE_URL = "https://open.tiktokapis.com/v2"

class TikTokApi:
    def __init__(self, client_key,client_secret, access_token):
         self.client_key = client_key
         self.client_secret = client_secret
         self.access_token = access_token
         
         self.VIDEO_QUERY_URL = BASE_URL + "/research/video/query/"
         self.USER_INFO_URL = BASE_URL + "/research/user/info/"
         self.VIDEO_COMMENTS_URL = BASE_URL + "/research/video/comment/list/"
       

    
    def get_videos(self, username, keyword, startdate, enddate):
        url = f"{self.VIDEO_QUERY_URL}?fields=id,video_description,create_time, region_code,share_count,view_count,like_count,comment_count, music_id,hashtag_names, username,effect_ids,playlist_id,voice_to_text, is_stem_verified, video_duration,hashtag_info_list, sticker_info_list, effect_info_list, video_mention_list,video_label,video_tag"
        query_params = {
                "fields" : "id,video_description,create_time, region_code,share_count,view_count,like_count,comment_count, music_id,hashtag_names, username,effect_ids,playlist_id,voice_to_text, is_stem_verified, favourites_count, video_duration,hashtag_info_list, sticker_info_list, effect_info_list, video_mention_list,video_label,video_tag",
                "max_count" : 100,
                "start_date" : startdate,
                "end_date" : enddate
        }
        
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
                "end_date" : enddate,
                "cursor": 0
        }
                            
        headers = {
                "Content-Type" : "application/json",
                "Authorization" : f"Bearer {self.access_token}"
            }
        
        does_have_more = True
        all_videos = []
        cursor = 0
        search_id = None
        
        while does_have_more:
            query_body["cursor"] = cursor
            if search_id:
                query_body["search_id"] = search_id
                
            response = requests.post(url, json=query_body, params=query_params, headers=headers)
            
            if response.status_code == 200:
                response_json = response.json()
                error = response_json.get("error", {})
                if error.get("code") == "daily_quota_limit_exceeded":
                    print("API quota exceeded. Stopping fetch.")
                    break
                
                data = response_json.get("data", []) 
                videos = data.get("videos", [])
                all_videos.extend(videos)
                
                
                if not len(all_videos):
                    print("No videos to return")
                    break
                
                search_id = data.get("search_id", search_id)                
                check_pagination = data["has_more"]
                if check_pagination == False:
                    return all_videos
                
                if "cursor" in data:
                    cursor = data["cursor"]
                else:
                    does_have_more = False
                
            else:
                logging.error("Something went wrong")
                error = response.json()
                return error
            
        return all_videos
        

    
    def get_videos_by_dynamic_query_body(self, query_body, start_date, end_date):
        print(query_body)
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
        cursor = 0
        search_id = None
        
        while does_have_more:
            query_body["cursor"] = cursor
            
            if search_id:
                query_body["search_id"] = search_id
            response = requests.post(self.VIDEO_QUERY_URL, json=query_body, params=query_params, headers=headers)
            
            if response.status_code == 200:
                data = response.json().get("data", [])
                videos = data.get("videos", [])
                all_videos.extend(videos)
                
                if len(all_videos) == 0:
                    return all_videos
                
                search_id = data.get("search_id", search_id)                
                check_pagination = data["has_more"]
                if check_pagination == False:
                    return all_videos
                
                if "cursor" in data:
                    cursor = data["cursor"]
                else:
                    does_have_more = False
                
            else:
                logging.error("something went wrong")
                error = response.json()
                print(error)
                return error
        
        print(all_videos)
        return all_videos
        
    
    def get_video_comments(self, video_id):
        url = f"{self.VIDEO_COMMENTS_URL}?fields=id,like_count,create_time,text,video_id,parent_comment_id"
    
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
            }

        data = {
            "video_id": video_id,
            "max_count": 100,
            "cursor": 0
            }
    
        all_comments = []

        while True:
            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                response_json = response.json()

                error = response_json.get("error", {})
                if error.get("code") == "daily_quota_limit_exceeded":
                    print("API quota exceeded")
                    break

                comments_data = response_json.get("data", {})
                comments = comments_data.get("comments", [])
                print("Fetched comments:", comments)

                if not comments:
                    print("No more comments.")
                    break

                all_comments.extend(comments)
                
                next_cursor = comments_data.get("cursor", None)
                if next_cursor is not None:
                    data["cursor"] = next_cursor
                else:
                    break
            else:
                logging.error("Something went wrong")
                print("Error response:", response.json())
                break 

        return all_comments



    
    def get_public_user_info(self, username):
        url = f"{self.USER_INFO_URL}?fields=display_name,bio_description,avatar_url,is_verified,follower_count,following_count,likes_count,video_count"
        
        headers = {
            "Content-Type" : "application/json",
            "Authorization" : f"Bearer {self.access_token}"
        }
        
        data = {
            "username" : username
        }
        
        response = requests.post(url, headers=headers, json=data)
        print(response.json())
        
        if(response.status_code == 200):
            user_info = response.json().get("data", None)
            if not user_info:
                return None
            
            return user_info
        else:
            logging.error("Something went wrong")
            error = response.json()
            return error
