import tkinter as tk
import tkinter.ttk as ttk

class CommentQueryWidget(tk.Frame):
    def __init__(self, parent, on_submit):
        super().__init__(parent, bg="#3A3A3A")
        self.on_submit = on_submit

        self.build_ui()

    def build_ui(self):
        self.label = tk.Label(self, text="Enter Video ID to fetch comments", font=("Helvetica", 8, "bold"), fg="white", bg="#3A3A3A")
        self.label.pack(side="top", pady=10)
    
        self.entry = tk.Entry(self, width=50, font=("Helvetica", 8), bg="lightgrey", fg="black", insertbackground="white")
        self.entry.pack(side="top", pady=10)
        
        self.submit_btn = tk.Button(self, text="Submit", command=self.submit)
        self.submit_btn.pack(side="top", pady=5)
    
    
    def submit(self):
        video_id = self.entry.get()
        if video_id:
            self.on_submit(video_id) 