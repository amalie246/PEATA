import tkinter as tk
import tkinter.ttk as ttk
import json
from PIL import Image, ImageTk
from api import TikTokApi
from endpoint_type import Endpoints
from file_processor import FileProcessor
from query_formatter import QueryFormatter
from datetime import datetime

class UiHelper:
    def __init__(self, client_key, client_secret, access_token):
        self.tiktok_api = TikTokApi(client_key, client_secret, access_token)
        self.file_processor = FileProcessor()
        self.latest_data = None
        self.query_formatter = QueryFormatter()
        self.images = {}
        
    
    def create_button_with_image(self, text, command, frame):
        btn_image = Image.open("images/GenBtn.png")
        btn_image = btn_image.crop(btn_image.getbbox())
        
        gen_btn_img = ImageTk.PhotoImage(btn_image, master=frame)
        
        self.images[text] = gen_btn_img
        
        button = tk.Button(frame, image=gen_btn_img, command=command)
        button.image = gen_btn_img
        button.pack(padx=10)
        
        text_label = tk.Label(frame, text=text, background="#323232", font=("Arial", 10, "bold"), fg="white")
        text_label.place(relx=0.5, rely=0.5, anchor="center")
        text_label.bind("<Button-1>", lambda event: command())
        
        return button
    
    def display_videos_chunked(self, videos, output, index):
        output.config(state=tk.NORMAL)
        chunk_size = 1
        if index >= len(videos):
            return
    
        for i in range(index, min(index + chunk_size, len(videos))):
            output.insert(tk.END, f"{videos[i]}\n\n")
        
        output.after(50, self.display_videos_chunked, videos, output, index + chunk_size)
    
    
    def update_ui(self, data, label):
        label.config(state=tk.NORMAL)
        label.delete(1.0, tk.END)
        
        if not len(data):
            message = "No data was found with your parameters"
            label.insert(tk.END, f"{message}")
            
        if "error" in data:
            message = "Error occured during fetching:"
            label.insert(tk.END, f"{message}\n{data}")
        
        else:
            label.insert(tk.END, f"{data}")
        
        label.config(state=tk.DISABLED)
        
        
    def api_call(self, endpoint, data, start_date, end_date, output, progress_bar):
        try:
            if endpoint == Endpoints.VIDEOS.name:
                print("in videos block")
                videos = []
                submitted_data = data
                print(f"submitted data: {submitted_data}")
            
                if len(submitted_data) == 2 and "AND" in submitted_data[0] and "username" in submitted_data[0] and "AND" in submitted_data[1] and "keyword" in submitted_data[1]:
                    username = submitted_data[0][2]
                    keyword = submitted_data[1][2]
                
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
                      
                    print("len: ", len(args))
                    query_body = self.query_formatter.query_builder(start_date, end_date, args)
                    print("made query body: ", query_body)
                    videos = self.tiktok_api.get_videos_by_dynamic_query_body(query_body, start_date, end_date)
                    print(videos)

                self.latest_data = videos
                output.after(0, self.display_videos_chunked, videos, output, 0)
                
            elif endpoint == Endpoints.COMMENTS.name:
                comments = self.tiktok_api.get_video_comments(data)
                self.latest_data = comments
                output.after(0, self.update_ui, comments, output)
                
            elif endpoint == Endpoints.USER_INFO.name:
                user_info = self.tiktok_api.get_public_user_info(data)
                self.latest_data = user_info
                output.after(0, self.update_ui, user_info, output)
                
            else:
                raise ValueError("invalid endpoint type")

        except Exception as e:
            print(f"Error fetching data: {e}")
            output.after(0, self.update_ui, f"Error: {e}", output)

        finally:
            output.after(0, progress_bar.stop())
        
    
    def download(self, endpoint_type_name, messagebox):
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{endpoint_type_name}{timestamp}.csv"
        ret = self.file_processor.export_data(filename, self.latest_data)
        
        if ret == 0:
            messagebox.showinfo("Download complete", "Your data has been downloaded as CSV and Excel, and can be found in the data-folder.")
        else:
            messagebox.showerror("Download failed", "Your data could not be downloaded")