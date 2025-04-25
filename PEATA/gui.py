import tkinter as tk
import tkinter.ttk as ttk
import threading
from tkinter import messagebox
from api import TikTokApi
from ui_helper import UiHelper
from query_formatter import QueryFormatter
from endpoint_type import Endpoints

class Gui:
    def __init__(self, master, cs, ci, ck, access_token):
        self.master = master
        self.client_secret = cs
        self.client_id = ci
        self.client_key = ck
        self.access_token = access_token
        self.tiktok_api = TikTokApi(self.client_key, self.client_secret, self.access_token)
        self.ui = UiHelper(self.client_key, self.client_secret, self.access_token)
        self.track_type = None

        
    def main_frame(self):
        def show_exit():
            if messagebox.askyesno("Exit Program", "Are you sure you want to quit your session?"):
                root.destroy()
            
        root = tk.Toplevel(self.master)
        style = ttk.Style()
        style.theme_use('clam')
        root.title("Packaged Easier Access to APIs: TikTok Research API")
        root.attributes("-fullscreen", True)
        root.bind("<Escape>", lambda event: show_exit())
        
        #FRAMES for content placing 
        full_frame = tk.Frame(root, bg="#3A3A3A")
        full_frame.pack(fill="both", expand=True)
        
        header_frame = tk.Frame(full_frame, bg="#FFFFFF", height=100)
        header_frame.pack(fill="x", side="top")
        
        content_frame = tk.Frame(full_frame, bg="grey")
        content_frame.pack(fill="both", expand=True)
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1, uniform="equal")
        content_frame.rowconfigure(1, weight=3, uniform="equal")
        
        top_frame = tk.Frame(content_frame, bg="#3A3A3A")
        top_frame.grid(row=0, column=0, columnspan= 2, sticky="nsew", padx=20)
        left_btm_frame = tk.Frame(content_frame, bg="#3A3A3A")
        left_btm_frame.grid(row=1, column=0, sticky="nsew", pady=20, padx=20)
        right_btm_frame = tk.Frame(content_frame, bg="#3A3A3A")
        right_btm_frame.grid(row=1, column=1, sticky="nsew", pady=20, padx=20)
        
        button_frame = tk.Frame(top_frame, bg="#3A3A3A")
        button_frame.pack(side="top", pady=70)
        
        video_btn_frame = tk.Frame(button_frame, bg="#3A3A3A")
        video_btn_frame.grid(row=0, column=0, padx=60)
        comment_btn_frame = tk.Frame(button_frame, bg="#3A3A3A")
        comment_btn_frame.grid(row=0, column=1, padx=60)
        user_btn_frame = tk.Frame(button_frame, bg="#3A3A3A")
        user_btn_frame.grid(row=0, column=2, padx=60)
        
        def destroy_children_widgets(frame):
            for widget in frame.winfo_children():
                widget.destroy()
            
        
        def video_queries():
            if hasattr(video_queries, "label"):
                return
            
            self.track_type = Endpoints.VIDEOS.name
            destroy_children_widgets(left_btm_frame)
            rows = []
            label = tk.Label(left_btm_frame, text="Enter parameters for video queries", font=("Helvetica", 8, "bold"), fg="white", bg="#3A3A3A")
            label.pack(side="top", pady=10)
            
            base_container = tk.Frame(left_btm_frame)
            base_container.pack(side="top", pady=5)
            
            startdate_label = tk.Label(left_btm_frame, text="Enter startdate (format: YYYYMMDD)", font=("Helvetica", 8, "bold"), fg="white", bg="#3A3A3A")
            startdate_label.pack(side="top")
            startdate_var = tk.StringVar()
            startdate = tk.Entry(left_btm_frame, textvariable=startdate_var, font=("Helvetica", 8), bg="lightgrey", fg="black", insertbackground="white")
            startdate.pack(side="top", pady=5)
            
            enddate_label = tk.Label(left_btm_frame, text="Enter enddate, cannot be more than 30 days later than startdate", font=("Helvetica", 8, "bold"), fg="white", bg="#3A3A3A")
            enddate_label.pack(side="top", pady=5)
            enddate_var = tk.StringVar()
            enddate = tk.Entry(left_btm_frame, textvariable=enddate_var, font=("Helvetica", 8), bg="lightgrey", fg="black", insertbackground="white")
            enddate.pack(side="top", pady=5)

            rows = []
            containers = []

            def add_dropdown_row(default_field=None, default_value=""):
                def remove_row():
                    # Remove this row's data and container
                    idx = containers.index(container)
                    containers.pop(idx)
                    rows.pop(idx)
                    container.destroy()
                    
                for cont in containers:
                    cont.pack_forget()
                    cont.pack(side="top", pady=5)

                container = tk.Frame(left_btm_frame)
                container.pack(side="top", pady=5)
        
                bool_option_var = tk.StringVar(value=bool_op[0])
                video_fields_option_var = tk.StringVar(value=default_field if default_field else video_fields[0])  
                value_var = tk.StringVar(value=default_value)
            
                rows.append((bool_option_var, video_fields_option_var, value_var))
                containers.append(container)
        
                bool_var = tk.OptionMenu(container, bool_option_var, *bool_op)
                bool_var.pack(side="left")
                bool_var.config(fg="black")

                fields_var = tk.OptionMenu(container, video_fields_option_var, *video_fields)
                fields_var.pack(side="left")
                fields_var.config(fg="black")
        
                value_entry = tk.Entry(container, textvariable=value_var)
                value_entry.pack(side="left")
        
                remove_btn = tk.Button(container, text="-", command=remove_row)
                remove_btn.pack(side="left")
            
            def submit():
                start_date = startdate_var.get()
                end_date = enddate_var.get()
                
                submitted_data = []
                for bool_var, field_var, value_var in rows:
                    t = (bool_var.get(), field_var.get(), value_var.get())
                    submitted_data.append(t)
                
                progress_bar.start(10)
                thread = threading.Thread(target=self.ui.api_call, args=(Endpoints.VIDEOS.name, submitted_data, start_date, end_date, output, progress_bar), daemon=True)
                thread.start()
                        
            
            add_dropdown_row(default_field="username", default_value="")
            add_dropdown_row(default_field="keyword", default_value="")
            
            add_row_btn = tk.Button(left_btm_frame, text="Add row", command=add_dropdown_row)
            add_row_btn.pack(side="bottom")
            submit_btn = tk.Button(left_btm_frame, text="Submit", command=submit)
            submit_btn.pack(side="bottom", pady=5)
        
        
        bool_op = ["AND", "OR", "NOT"]
        video_fields = ["username", "keyword", "create_date", "region_code", "video_id", "hashtag_name", "music_id", "effect_id", "video_length"]

            
        def comment_queries():
            if hasattr(comment_queries, "label"):
                return
            
            self.track_type = Endpoints.COMMENTS.name
            destroy_children_widgets(left_btm_frame)
            
            label = tk.Label(left_btm_frame, text="Enter Video ID to fetch comments", font=("Helvetica", 8, "bold"), fg="white", bg="#3A3A3A")
            label.pack(side="top", pady=10)
        
            entry = tk.Entry(left_btm_frame, width=50, font=("Helvetica", 8), bg="lightgrey", fg="black", insertbackground="white")
            entry.pack(side="top", pady=10)
        
            comment_queries.label = label

            def submit():
                video_id = entry.get()
                label.config(text=f"Fetching comments for video ID: {video_id}...")
                #TODO needs multithreading because it is insane
                progress_bar.start(10)
                thread = threading.Thread(target=self.ui.api_call, args=(Endpoints.COMMENTS.name, video_id, None, None, output, progress_bar), daemon=True)
                thread.start()
        
            submit_btn = tk.Button(left_btm_frame, text="Submit", command=submit)
            submit_btn.pack(side="top", pady=5)
        
        def user_queries():
            if hasattr(user_queries, "label"):
                return
            
            self.track_type = Endpoints.USER_INFO.name
            destroy_children_widgets(left_btm_frame)
            
            label = tk.Label(left_btm_frame, text="Enter username to fetch user information:", font=("Helvetica", 8, "bold"), fg="white", bg="#3A3A3A")
            label.pack(side="top", pady=10)
            entry = tk.Entry(left_btm_frame, width=50)
            entry.pack(side="top", pady=10)
            user_queries.label = label
            
            
            def submit():
                username = entry.get()
                label.config(text=f"Fetching info about {username}...")
                
                progress_bar.start(10)
                thread = threading.Thread(target=self.ui.api_call, args=(Endpoints.USER_INFO.name, username, None, None, output, progress_bar), daemon=True)
                thread.start()
                
            submit_btn = tk.Button(left_btm_frame, text="Submit", command=submit)
            submit_btn.pack(side="top", pady=5)
        
        def download():
            self.ui.download(self.track_type)
            
        
        #CONTENT in frames
        title = tk.Label(header_frame, text="Packaged Easier to Access APIs", font=("Helvetica", 12, "bold"), fg="white", bg="grey")
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
        self.ui.create_button_with_image("Videos", video_queries, video_btn_frame)
        self.ui.create_button_with_image("Comments", comment_queries, comment_btn_frame)
        self.ui.create_button_with_image("User info", user_queries, user_btn_frame)
        
        progress_bar = ttk.Progressbar(
            right_btm_frame,
            orient="horizontal",
            mode="indeterminate",
            length=100
            )
        progress_bar.grid(row=0, column=0, padx=10, pady=10)
        
        #Data sneak peak
        output = tk.Text(right_btm_frame, height=25, width=90, wrap=tk.WORD, fg="white", bg="black", font=("Arial", 10))
        output.grid(row=9, column=10, columnspan=3, pady=10)
        output.config(state=tk.DISABLED)#Editing is disabled

        scrollbar = tk.Scrollbar(right_btm_frame, command=output.yview)
        scrollbar.grid(row=9, column=13, sticky="ns")
        output.config(yscrollcommand=scrollbar.set)
        
        download_btn = tk.Button(right_btm_frame, text="Download as CSV file", command=download)
        download_btn.grid(row=14, column=11)
        
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk() 
    gui = Gui(root, "a", "b", "c", "d")
    gui.main_frame()
    root.mainloop()