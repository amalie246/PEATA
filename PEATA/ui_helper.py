import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from enum import Enum
from api import TikTokApi

class Endpoints(Enum):
    VIDEOS = 1,
    COMMENTS = 2,
    USER_INFO = 3
    
class UiHelper:
    def __init__(self):
        self.tiktok_api = TikTokApi()
    
    def create_button_with_image(self, text, command, frame):
        btn_image = Image.open("images/GenBtn.png")
        btn_image = btn_image.crop(btn_image.getbbox())
        gen_btn_img = ImageTk.PhotoImage(btn_image)
        
        button = tk.Button(frame, image=gen_btn_img, command=command)
        button.image = gen_btn_img
        button.pack(padx=10)
        
        text_label = tk.Label(frame, text=text, background="#323232", font=("Arial", 10, "bold"), fg="white")
        text_label.place(relx=0.5, rely=0.5, anchor="center")
        
        return button
    
    def update_ui(self, data, label):
        label.config(state=tk.NORMAL)
        label.delete(1.0, tk.END)
        
        if "error" in data:
            message = "Error occured during fetching:"
            label.insert(tk.END, f"{message}\n{data}")
            return
        
        elif len(data) > 0:
            label.insert(tk.END, f"{data}")
            return
        
        else:
            message = "No data was found with your parameters"
            label.insert(tk.END, f"{message}")
        label.config(state=tk.DISABLED)
        
    def api_call(self, endpoint, data, start_date, end_date, output, progress_bar):
        try:
            if endpoint == Endpoints.VIDEOS.name:
                videos = []
                submitted_data = data
                
                t1 = submitted_data[0]
                t2 = submitted_data[1]
                
                if len(submitted_data) == 2:
                        if "AND" in t1 and "username" in t1:
                            if "AND" in t2 and "keyword" in t2:
                                username = t1[2]
                                keyword = t2[2]
                                videos = self.tiktok_api.get_videos(username, keyword, start_date, end_date)
                                
                else:
                    and_clauses = [(t[1], t[2], "EQ") for t in submitted_data if t[0] == "AND"]
                    or_clauses = [(t[1], t[2], "EQ") for t in submitted_data if t[0] == "OR"]
                    not_clauses = [(t[1], t[2], "EQ") for t in submitted_data if t[0] == "NOT"]
                        
                    args = []
                    if len(and_clauses) > 0:
                        query_formatted_and_clauses = self.query_formatter.query_AND_clause(and_clauses)
                        args.append(query_formatted_and_clauses)
                    if len(or_clauses) > 0:
                        query_formatted_or_clauses = self.query_formatter.query_OR_clause(or_clauses)
                        args.append(query_formatted_or_clauses)
                    if len(not_clauses) > 0:
                        query_formatted_not_clauses = self.query_formatter.query_NOT_clause(not_clauses)
                        args.append(query_formatted_not_clauses)
                        
                    query_body = self.query_formatter.query_builder(start_date, end_date, query_formatted_and_clauses)
                    print(query_body)
                    videos = self.tiktok_api.get_videos_by_dynamic_query_body(query_body, start_date, end_date)
                    print(videos)


                output.after(0, self.update_ui, videos, output)
            elif endpoint == Endpoints.COMMENTS.name:
                comments = self.tiktok_api.get_video_comments(data)
                output.after(0, self.update_ui, comments, output)
                
            elif endpoint == Endpoints.USER_INFO.name:
                user_info = self.tiktok_api.get_public_user_info(data)
                output.after(0, self.update_ui, user_info, output)
                
            else:
                raise ValueError("invalid endpoint type")

        except Exception as e:
            print(f"Error fetching videos: {e}")
            output.after(0, self.update_ui, f"Error: {e}", output)

        finally:
            progress_bar.stop()