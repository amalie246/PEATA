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
        
    
    def create_button(self, text, command, frame):
        button = tk.Button(frame, command=command, text=text,
                           fg="white", bg="#232323",
                           font=("Helvetica", 10, "bold"),
                           width=30, height=2)
        button.pack(padx=10, pady=10)
        
        
        return button
    
    def display_data_chunked(self, data, output, index):
        output.config(state=tk.NORMAL)
        chunk_size = 1
        if index >= len(data):
            return
    
        for i in range(index, min(index + chunk_size, len(data))):
            output.insert(tk.END, f"{data[i]}\n\n")
        
        output.after(50, self.display_data_chunked, data, output, index + chunk_size)
    
    
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
                videos = []
                submitted_data = data
            
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
                      
                    query_body = self.query_formatter.query_builder(start_date, end_date, args)
                    videos = self.tiktok_api.get_videos_by_dynamic_query_body(query_body, start_date, end_date)

                self.latest_data = videos
                output.delete(1.0, tk.END)
                output.after(0, self.display_data_chunked, videos, output, 0)
                
            elif endpoint == Endpoints.COMMENTS.name:
                comments = self.tiktok_api.get_video_comments(data)
                self.latest_data = comments
                output.delete(1.0, tk.END)
                output.after(0, self.display_data_chunked, comments, output, 0)
                
                
            elif endpoint == Endpoints.USER_INFO.name:
                user_info = self.tiktok_api.get_public_user_info(data)
                self.latest_data = user_info
                output.delete(1.0, tk.END)
                output.after(0, self.update_ui, user_info, output)
                
            else:
                raise ValueError("invalid endpoint type")

        except Exception as e:
            print(f"Error fetching data: {e}")
            output.after(0, self.update_ui, f"Error: {e}", output)

        finally:
            output.after(0, progress_bar.stop())
        
    
    def download(self, endpoint_type_name, messagebox, file_format="csv"):
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{endpoint_type_name}_{timestamp}"

        if self.latest_data is None:
            messagebox.showerror("Download failed", "No data available to download.")
            return

        try:
            if file_format == "csv":
                ret = self.file_processor.export_data_as_csv(filename, self.latest_data)
                if ret == 0:
                    messagebox.showinfo("Download complete", f"Data downloaded as CSV: {filename}.csv")
                
                else:
                    messagebox.showerror("Download failed", "Failed to save CSV file.")
            elif file_format == "excel":
                self.file_processor.data = self.latest_data
                self.file_processor.file_path = None
                ret = self.file_processor.export_as_excel(filename, self.latest_data)
                if ret == 0:
                    messagebox.showinfo("Download complete", f"Data downloaded as Excel: {filename}.xlsx")
                else:
                    messagebox.showerror("Download failed", "Failed to save Excel file.")
            else:
                messagebox.showerror("Download failed", "Unsupported file format selected.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during download: {e}")

            