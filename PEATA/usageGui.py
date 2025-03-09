import tkinter as tk
from tkinter import messagebox
import requests

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
    
    def test_page(self):
        root = tk.Tk()
        root.title("Packaged Easier to Access APIs: TikTok Research API")
        root.attributes("-fullscreen", True)
        root.bind("<Escape>", lambda event: root.destroy())
        
        full_frame = tk.Frame(root, bg="#BFEFFF")
        full_frame.pack(fill="both", expand=True)
        
        def video_queries():
            #Initially, there should be "username", "startdate" and "enddate"
            #Make sure enddate can NOT be more than 30 days after start date
            #User can also press button to add more queries
            #And also change username
            #startdate and enddate is hard required
            videos = []
        
        def comment_queries():
            #Video ID is required, also the only field
            #Maybe insert a max count 
            #Inform users that having a large max count is time consuming
            comments = []

        
        def user_queries():
            #Username is required, also only field
            user = []
            entry = tk.Entry(choice_frame, width=50)
            entry.grid(row=5, column=3)
            
            def submit():
                user_input = entry.get()
                label.config(text=f"Username: {user_input}")
            
            submit_btn = tk.Button(choice_frame, text="Submit", command=submit)
            submit_btn.grid(row=5, column=4)
            label = tk.Label(choice_frame, text="", font=("Arial", 12))
            label.grid(row=6, column=1)
            
            
        choice_frame = tk.Frame(full_frame, width=900, height=900, bg="white", bd=2, relief="solid")
        choice_frame.pack(pady=10, padx=10)
        choice_frame.grid_propagate(False)
        
        title = tk.Label(choice_frame, text="Choose between queries", font=("Arial", 16, "bold"))
        title.grid(row=1, column=2, pady=10)
        
        video_btn = tk.Button(choice_frame, text="Video queries", command=video_queries)
        video_btn.grid(row=3, column=1)
        
        comment_btn = tk.Button(choice_frame, text="Comment queries (by video id)", command=comment_queries)
        comment_btn.grid(row=3, column=2)
        
        user_btn = tk.Button(choice_frame, text="User info queries (by username)", command=user_queries)
        user_btn.grid(row=3, column=3)
        
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

