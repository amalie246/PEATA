import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from api import TikTokApi

#TODO for this class
#   1 - Make it so that users can choose between getting videos, user info or comments
#   2 - Dropdown menu (dynamic) for multiple fields for query
#   3 - Connect this with TikTokApi class
#   4 - A simple query for videos by date and username

class Gui:
    def __init__(self, cs, ci, ck):
        self.client_secret = cs
        self.client_id = ci
        self.client_key = ck
        self.tiktok_api = TikTokApi()
        
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
        
        def video_queries():
            videos = []
        
        def comment_queries():
            comments = []
        
        def user_queries():
            if hasattr(user_queries, "label"):
                return
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
                    padding=10,
                    borderwidth=2,
                    relief="flat",
                    foreground="white",
                    background="black",
                    focusthickness=3,
                    focuscolor="")
        
        video_btn = ttk.Button(button_frame, text="Video queries", command=video_queries, style="Custom.TButton")
        video_btn.pack(side="left", pady=10, padx=50)
        comment_btn = ttk.Button(button_frame, text="Comments (by video id)", command=comment_queries, style="Custom.TButton")
        comment_btn.pack(side="left", pady=10, padx=50)
        user_btn = ttk.Button(button_frame, text="User info queries", command=user_queries, style="Custom.TButton")
        user_btn.pack(side="left", pady=10, padx=50)
        
        temp_label = tk.Text(right_btm_frame, height=10, width=80, wrap=tk.WORD, bg="pink", font=("Arial", 10))
        temp_label.grid(row=8, column=10, columnspan=3, pady=10)
        temp_label.config(state=tk.DISABLED)#Editing is disabled

        scrollbar = tk.Scrollbar(right_btm_frame, command=temp_label.yview)
        scrollbar.grid(row=8, column=13, sticky="ns")
        temp_label.config(yscrollcommand=scrollbar.set)
        
        download_btn = tk.Button(right_btm_frame, text="Download as CSV file", command=download)
        download_btn.grid(row=9, column=1)
        
        root.mainloop()
        
    
    def page(self):
        #LT/LTE/GT/GTE must be used for date i think
        #And i think IN is in a gange of some sort
        boolean_operations = ["and", "or", "not"]
        eq_operations = ["EQ", "IN", "LT", "LTE", "GT", "GTE"]
        
        def video_queries():
            #This is where the dynamic query body can be
           video_fields = ["id", "video_description", "create_time", "region_code", "share_count", "view_count", "like_count", "comment_count", "music_id", "effects_ids", "playlist_id", "voice_to_text", "is_stem_verified", "video_duration", "hashtag_info_list", "video_mention_list", "video_label"]
           dates = ["startdate", "enddate"]
        
        def user_info_queries():
            username = []
        
        def comment_queries():
            username = []
        
        
        root = tk.Tk()
        root.title("Packaged Easier to Access APIs: TikTok Research API")
        root.geometry("1000x1000")
        root.configure(bg="lightblue")
        
        def add_dropdown_row():
            row_index = len(dropdown_rows)
            clickedBool = tk.StringVar()
            clickedBool.set( "and" )
            clickedEq = tk.StringVar()
            clickedEq.set("EQ")
            
            bool_drop = tk.OptionMenu(dropdown_frame, clickedBool, *boolean_operations)
            bool_drop.grid(row=row_index, column=0, padx=10)
            eq_drop = tk.OptionMenu(dropdown_frame, clickedEq, *eq_operations)
            eq_drop.grid(row=row_index, column=2, padx=10)
            
            dropdown_rows.append((clickedBool, clickedEq))
            
        def show_selection():
            selections = []
            for bool_var, eq_var in dropdown_rows:
                selections.append(f"{bool_var.get()} - {eq_var.get()}")
                
            label.config(text="Your selections: " + ", ".join(selections))
            
        dropdown_rows = []
            
        dropdown_frame = tk.Frame(root)
        dropdown_frame.pack(pady=20)
        
        add_dropdown_row()
        add_btn = tk.Button(dropdown_frame, text="+", command=add_dropdown_row)
        add_btn.grid(row=9, column=0, pady=10)
        
        button = tk.Button(dropdown_frame, text="Submit", command=show_selection)
        button.grid(row=3, column=1, pady=10)
        label = tk.Label(dropdown_frame, text=" ")
        label.grid(row=10, column=1, pady=10)
        
        
        def show_popup():
            messagebox.showinfo("Information", "This is a popup box!")

        button = tk.Button(root, text="Click Me!", command=show_popup)
        button.pack(pady=50) 
        
        root.mainloop()

