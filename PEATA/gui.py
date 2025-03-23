import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from api import TikTokApi
from PIL import Image, ImageTk

#TODO for this class
#   1 - Make it so that users can choose between getting videos, user info or comments
#   2 - Dropdown menu (dynamic) for multiple fields for query
#   3 - Connect this with TikTokApi class
#   4 - A simple query for videos by date and username

class Gui:
    def __init__(self, cs, ci, ck, access_token):
        self.client_secret = cs
        self.client_id = ci
        self.client_key = ck
        self.access_token = access_token
        self.tiktok_api = TikTokApi(self.client_key, self.client_secret, self.access_token)
        
    def test_page(self):
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
        
        def video_queries():
            if hasattr(video_queries, "label"):
                return
            
            destroy_children_widgets(left_btm_frame)
            rows = []
            label = tk.Label(left_btm_frame, text="Enter parameters for video queries", font=("Arial", 10, "bold"))
            label.pack(side="top", pady=10)
            
            base_container = tk.Frame(left_btm_frame)
            base_container.pack(side="top", pady=5)
            #Needs at least one parameter, startdate and enddate
            #Should set username and keyword as default
            bool_op = ["AND", "OR", "NOT"]
            video_fields = ["id", "video_description", "create_time", "region_code", "share_count", "view_count", "like_count", "comment_count", "music_id", "effects_ids", "playlist_id", "voice_to_text", "is_stem_verified", "video_duration", "hashtag_info_list", "video_mention_list", "video_label"]
            dates = ["startdate", "enddate"]
            op = ["EQ"]
            
            def add_dropdown_row():
                #This should add another row if "add" button is clicked
                index = len(rows)
                container = tk.Frame(left_btm_frame)
                container.pack(side="top", pady=5)
                
                bool_var = tk.OptionMenu(container, bool_option_var, bool_op[0], *bool_op)
                bool_var.pack(side="left")
                fields_var = tk.OptionMenu(container, video_fields_option_var, video_fields[0], *video_fields)
                fields_var.pack(side="left")
            
            add_param = tk.Button(left_btm_frame, text="+", command=add_dropdown_row)
            add_param.pack(side="bottom", pady=5)
        
            bool_option_var = tk.StringVar()
            video_fields_option_var = tk.StringVar()
            
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
                comments = self.tiktok_api.get_video_comments(video_id)
                
                temp_label.config(state=tk.NORMAL)
                temp_label.delete(1.0, tk.END)
                temp_label.insert(tk.END, f"Comments:\n{comments}")
                temp_label.config(state=tk.DISABLED)
        
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
                user_info = self.tiktok_api.get_public_user_info(username)
                temp_label.config(state=tk.NORMAL)
                temp_label.delete(1.0, tk.END)
                temp_label.insert(tk.END, f"{user_info}")
                temp_label.config(state=tk.DISABLED)
                
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
        
        btn_image = Image.open("images/GenBtn.png")
        btn_image = btn_image.crop(btn_image.getbbox())
        gen_btn_img = ImageTk.PhotoImage(btn_image)
        
        video_btn_bg = tk.Button(video_btn_frame, image=gen_btn_img, command=video_queries)
        video_btn_bg.image = gen_btn_img
        video_btn_bg.pack(padx=10)
        
        video_text_label = tk.Label(video_btn_frame, text="Videos", background="#323232", font=("Arial", 10, "bold"), fg="white")
        video_text_label.place(relx=0.5, rely=0.5, anchor="center")
        
        comment_btn_bg = tk.Button(comment_btn_frame, image=gen_btn_img, command=comment_queries)
        comment_btn_bg.image = gen_btn_img
        comment_btn_bg.pack(padx=10)
        
        comment_text_label = tk.Label(comment_btn_frame, text="Comments", background="#323232", font=("Arial", 10, "bold"), fg="white")
        comment_text_label.place(relx=0.5, rely=0.5, anchor="center")
        
        user_btn_bg = tk.Button(user_btn_frame, image=gen_btn_img, command=user_queries)
        user_btn_bg.image = gen_btn_img
        user_btn_bg.pack(padx=10)
        
        user_text_label = tk.Label(user_btn_frame, text="User info", background="#323232", font=("Arial", 10, "bold"), fg="white")
        user_text_label.place(relx=0.5, rely=0.5, anchor="center")
        
        temp_label = tk.Text(right_btm_frame, height=10, width=80, wrap=tk.WORD, bg="pink", font=("Arial", 10))
        temp_label.grid(row=8, column=10, columnspan=3, pady=10)
        temp_label.config(state=tk.DISABLED)#Editing is disabled

        scrollbar = tk.Scrollbar(right_btm_frame, command=temp_label.yview)
        scrollbar.grid(row=8, column=13, sticky="ns")
        temp_label.config(yscrollcommand=scrollbar.set)
        
        download_btn = tk.Button(right_btm_frame, text="Download as CSV file", command=download)
        download_btn.grid(row=9, column=1)
        
        root.mainloop()
