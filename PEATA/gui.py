import tkinter as tk
import tkinter.ttk as ttk
import threading
from tkinter import messagebox
from api import TikTokApi
from ui_controller import UiController
from query_formatter import QueryFormatter
from endpoint_type import Endpoints
from ui_config import UiConfig
from video_query_widget import VideoQueryWidget
from comment_query_widget import CommentQueryWidget
from user_query_widget import UserQueryWidget

class Gui:
    def __init__(self, master, cs, ci, ck, access_token):
        self.master = master
        self.client_secret = cs
        self.client_id = ci
        self.client_key = ck
        self.access_token = access_token
        self.ui_controller = UiController(self.client_key, self.client_secret, self.access_token)
        self.ui_config = UiConfig()
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
            
            def handle_submit(conditions, start, end):
                progress_bar.start(10)
                thread = threading.Thread(
                    target=self.ui_controller.api_call,
                    args=(Endpoints.VIDEOS.name, conditions, start, end, output, progress_bar),
                    daemon=True
                    )
                thread.start()
            
            video_query_widget = VideoQueryWidget(left_btm_frame, on_submit=handle_submit)
            video_query_widget.pack(fill="both", expand=True)

            
        def comment_queries():
            if hasattr(comment_queries, "label"):
                return
            
            self.track_type = Endpoints.COMMENTS.name
            destroy_children_widgets(left_btm_frame)
            

            def handle_submit(video_id):
                progress_bar.start(10)
                thread = threading.Thread(
                    target=self.ui_controller.api_call,
                    args=(Endpoints.COMMENTS.name, video_id, None, None, output, progress_bar),
                    daemon=True
                    )
                thread.start()
            
            comment_query_widget = CommentQueryWidget(left_btm_frame, on_submit=handle_submit)
            comment_query_widget.pack(fill="both", expand=True)
        
        def user_queries():
            if hasattr(user_queries, "label"):
                return
            
            self.track_type = Endpoints.USER_INFO.name
            destroy_children_widgets(left_btm_frame)
            
            def handle_submit(username):
                progress_bar.start(10)
                thread = threading.Thread(
                    target=self.ui_controller.api_call,
                    args=(Endpoints.USER_INFO.name, username, None, None, output, progress_bar),
                    daemon=True
                    )
                thread.start()
                
            user_query_widget = UserQueryWidget(left_btm_frame, on_submit=handle_submit)   
            user_query_widget.pack(fill="both", expand=True)
            
        
        def download_csv():
            def run_download():
                progress_bar.start(10)
                self.ui_controller.download(self.track_type, messagebox, file_format="csv")
                progress_bar.stop()

            threading.Thread(target=run_download, daemon=True).start()

        def download_excel():
            def run_download():
                progress_bar.start(10)
                self.ui_controller.download(self.track_type, messagebox, file_format="excel")
                progress_bar.stop()

            threading.Thread(target=run_download, daemon=True).start()


            
        
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
        self.ui_config.create_button("Videos", video_queries, video_btn_frame)
        self.ui_config.create_button("Comments", comment_queries, comment_btn_frame)
        self.ui_config.create_button("User info", user_queries, user_btn_frame)
        
        progress_bar = ttk.Progressbar(
            right_btm_frame,
            orient="horizontal",
            mode="indeterminate",
            length=100
            )
        progress_bar.grid(row=8, column=10, columnspan=3, padx=50, pady=(10, 0), sticky="ew")
        
        #Data sneak peak
        output = tk.Text(right_btm_frame, height=25, width=90, wrap=tk.WORD, fg="white", bg="black", font=("Arial", 10))
        output.grid(row=9, column=10, columnspan=3, pady=10)
        output.config(state=tk.DISABLED)

        scrollbar = tk.Scrollbar(right_btm_frame, command=output.yview)
        scrollbar.grid(row=9, column=13, sticky="ns")
        output.config(yscrollcommand=scrollbar.set)
        
        download_csv_btn = tk.Button(right_btm_frame, text="Download as CSV", command=download_csv)
        download_csv_btn.grid(row=14, column=10, pady=10)

        download_excel_btn = tk.Button(right_btm_frame, text="Download as Excel", command=download_excel)
        download_excel_btn.grid(row=14, column=11, pady=10)

        
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk() 
    gui = Gui(root, "a", "b", "c", "d")
    gui.main_frame()
    root.mainloop()