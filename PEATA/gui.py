import tkinter as tk
import tkinter.ttk as ttk
import threading
from tkinter import messagebox
from enum import Enum
from api import TikTokApi
from PIL import Image, ImageTk
from queryFormatter import QueryFormatter

class Endpoints(Enum):
    VIDEOS = 1,
    COMMENTS = 2,
    USER_INFO = 3

#TODO must fix OR and NOT operations as well
#TODO refactor code because this is a mess
#Refactor code by splitting it into smaller classes

class Gui:
    def __init__(self, cs, ci, ck, access_token):
        self.client_secret = cs
        self.client_id = ci
        self.client_key = ck
        self.access_token = access_token
        self.tiktok_api = TikTokApi()
        #self.tiktok_api = TikTokApi(self.client_key, self.client_secret, self.access_token)
        self.query_formatter = QueryFormatter()
    
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
        
        elif isinstance(data, list):
            label.insert(tk.END, f"{data}")
            return
        
        else:
            message = "No data was found with your parameters"
            label.insert(tk.END, f"{message}")
        label.config(state=tk.DISABLED)
        
    def main_frame(self):
        def show_exit():
            if messagebox.askyesno("Exit Program", "Are you sure you want to quit your session?"):
                root.destroy()
            
        root = tk.Tk()
        style = ttk.Style()
        style.theme_use('clam')
        root.title("Packaged Easier Access to APIs: TikTok Research API")
        root.attributes("-fullscreen", True)
        root.bind("<Escape>", lambda event: show_exit())
        
        #FRAMES for content placing 
        full_frame = tk.Frame(root, bg="#CAE1FF")
        full_frame.pack(fill="both", expand=True)
        
        header_frame = tk.Frame(full_frame, bg="#FFFFFF", height=100)
        header_frame.pack(fill="x", side="top")
        
        content_frame = tk.Frame(full_frame, bg="white")
        content_frame.pack(fill="both", expand=True)
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1, uniform="equal")
        content_frame.rowconfigure(1, weight=3, uniform="equal")
        
        top_frame = tk.Frame(content_frame, bg="#D1D1D1")
        top_frame.grid(row=0, column=0, columnspan= 2, sticky="nsew", padx=20)
        left_btm_frame = tk.Frame(content_frame, bg="#D1D1D1")
        left_btm_frame.grid(row=1, column=0, sticky="nsew", pady=20, padx=20)
        right_btm_frame = tk.Frame(content_frame, bg="#D1D1D1")
        right_btm_frame.grid(row=1, column=1, sticky="nsew", pady=20, padx=20)
        
        button_frame = tk.Frame(top_frame, bg="#D1D1D1")
        button_frame.pack(side="top", pady=70)
        
        video_btn_frame = tk.Frame(button_frame, bg="#D1D1D1")
        video_btn_frame.grid(row=0, column=0, padx=60)
        comment_btn_frame = tk.Frame(button_frame, bg="#D1D1D1")
        comment_btn_frame.grid(row=0, column=1, padx=60)
        user_btn_frame = tk.Frame(button_frame, bg="#D1D1D1")
        user_btn_frame.grid(row=0, column=2, padx=60)
        
        def destroy_children_widgets(frame):
            for widget in frame.winfo_children():
                widget.destroy()
            
        
        def api_call(endpoint, data, start_date, end_date):
            print("Trying to call api")
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
                                print("Called api")
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

        
        def video_queries():
            if hasattr(video_queries, "label"):
                return
            
            destroy_children_widgets(left_btm_frame)
            rows = []
            label = tk.Label(left_btm_frame, text="Enter parameters for video queries", font=("Arial", 10, "bold"))
            label.pack(side="top", pady=10)
            
            base_container = tk.Frame(left_btm_frame)
            base_container.pack(side="top", pady=5)
            
            startdate_label = tk.Label(left_btm_frame, text="Enter startdate (format: YYYYMMDD)")
            startdate_label.pack(side="top")
            startdate_var = tk.StringVar()
            startdate = tk.Entry(left_btm_frame, textvariable=startdate_var)
            startdate.pack(side="top", pady=5)
            
            enddate_label = tk.Label(left_btm_frame, text="Enter enddate, cannot be more than 30 days later than startdate")
            enddate_label.pack(side="top", pady=5)
            enddate_var = tk.StringVar()
            enddate = tk.Entry(left_btm_frame, textvariable=enddate_var)
            enddate.pack(side="top", pady=5)

            
            def add_dropdown_row(default_field=None, default_value=""):
                def remove_row():
                    destroy_children_widgets(container)
                    rows.remove((bool_option_var, video_fields_option_var, value_var))
                    
                container = tk.Frame(left_btm_frame)
                container.pack(side="top", pady=5)
                bool_option_var = tk.StringVar(value=bool_op[0])
                video_fields_option_var = tk.StringVar(value=default_field if default_field else video_fields[0])  
                value_var = tk.StringVar(value=default_value)
            
                
                rows.append((bool_option_var, video_fields_option_var, value_var))
                
                bool_var = tk.OptionMenu(container, bool_option_var, *bool_op)
                bool_var.pack(side="left")

                fields_var = tk.OptionMenu(container, video_fields_option_var, *video_fields)
                fields_var.pack(side="left")

                value_entry = tk.Entry(container, textvariable=value_var)
                value_entry.pack(side="left")
                
                #TODO not working as expected
                remove_btn = tk.Button(container, text="-", command=remove_row)
                remove_btn.pack(side="left")
            
            def submit():
                start_date = startdate_var.get()
                end_date = enddate_var.get()
                
                submitted_data = []
                for bool_var, field_var, value_var in rows:
                    t = (bool_var.get(), field_var.get(), value_var.get())
                    submitted_data.append(t)
                
                #TODO fix me ( the progress bar )
                progress_bar.start(10)
                thread = threading.Thread(target=api_call, args=(Endpoints.VIDEOS.name, submitted_data, start_date, end_date), daemon=True)
                thread.start()
                        
            
            add_dropdown_row(default_field="username", default_value="")
            add_dropdown_row(default_field="keyword", default_value="")
            
            add_row_btn = tk.Button(left_btm_frame, text="Add row", command=add_dropdown_row)
            add_row_btn.pack(side="bottom")
            submit_btn = tk.Button(left_btm_frame, text="Submit", command=submit)
            submit_btn.pack(side="bottom", pady=5)
        
        
        bool_op = ["AND", "OR", "NOT"]
        #TODO fix this so it is the complete list
        video_fields = ["id", "video_description", "username", "keyword", "create_time", "region_code", "share_count", "view_count", "like_count", "comment_count", "music_id", "effects_ids", "playlist_id", "voice_to_text", "is_stem_verified", "video_duration", "hashtag_info_list", "video_mention_list", "video_label"]

            
        def comment_queries():
            if hasattr(comment_queries, "label"):
                return
            
            destroy_children_widgets(left_btm_frame)
            
            label = tk.Label(left_btm_frame, text="Enter Video ID to fetch comments", font=("Arial", 10, "bold"))
            label.pack(side="top", pady=10)
        
            entry = tk.Entry(left_btm_frame, width=50)
            entry.pack(side="top", pady=10)
        
            comment_queries.label = label

            def submit():
                video_id = entry.get()
                label.config(text=f"Fetching comments for video ID: {video_id}...")
                #TODO needs multithreading because it is insane
                progress_bar.start(10)
                thread = threading.Thread(target=api_call, args=(Endpoints.COMMENTS.name, video_id, None, None), daemon=True)
                thread.start()
        
            submit_btn = tk.Button(left_btm_frame, text="Submit", command=submit)
            submit_btn.pack(side="top", pady=5)
        
        def user_queries():
            if hasattr(user_queries, "label"):
                return
            
            destroy_children_widgets(left_btm_frame)
            
            label = tk.Label(left_btm_frame, text="Enter username to fetch user information:", font=("Arial", 10, "bold"))
            label.pack(side="top", pady=10)
            entry = tk.Entry(left_btm_frame, width=50)
            entry.pack(side="top", pady=10)
            user_queries.label = label
            
            
            def submit():
                username = entry.get()
                label.config(text=f"Fetching info about {username}...")
                
                progress_bar.start(10)
                thread = threading.Thread(target=api_call, args=(Endpoints.USER_INFO.name, username, None, None), daemon=True)
                thread.start()
                
            submit_btn = tk.Button(left_btm_frame, text="Submit", command=submit)
            submit_btn.pack(side="top", pady=5)
        
        def download():
            download = []
        #CONTENT in frames
        title = tk.Label(header_frame, text="Packaged Easier to Access APIs", font=("Arial", 16, "bold"), bg="#FFFFFF")
        title.pack(fill="both")

        btn_style = ttk.Style()
        btn_style.configure("Custom.TButton",
                    font=("Segoe UI", 10, "bold"),
                    relief="flat",
                    foreground="white",
                    background="black",
                    focusthickness=3,
                    focuscolor="")
        
        #Buttons
        self.create_button_with_image("Videos", video_queries, video_btn_frame)
        self.create_button_with_image("Comments", comment_queries, comment_btn_frame)
        self.create_button_with_image("User info", user_queries, user_btn_frame)
        
        progress_bar = ttk.Progressbar(
            right_btm_frame,
            orient="horizontal",
            mode="indeterminate",
            length=100
            )
        progress_bar.grid(row=0, column=0, padx=10, pady=10)
        
        #Data sneak peak
        output = tk.Text(right_btm_frame, height=10, width=80, wrap=tk.WORD, bg="pink", font=("Arial", 10))
        output.grid(row=8, column=10, columnspan=3, pady=10)
        output.config(state=tk.DISABLED)#Editing is disabled

        scrollbar = tk.Scrollbar(right_btm_frame, command=output.yview)
        scrollbar.grid(row=8, column=13, sticky="ns")
        output.config(yscrollcommand=scrollbar.set)
        
        download_btn = tk.Button(right_btm_frame, text="Download as CSV file", command=download)
        download_btn.grid(row=9, column=1)
        
        root.mainloop()
