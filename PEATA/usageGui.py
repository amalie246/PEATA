import tkinter as tk
from tkinter import messagebox
import requests

class Gui:
    def __init__(self, cs, ci, ck):
        self.client_secret = cs
        self.client_id = ci
        self.client_key = ck
    
    def page(self):
        root = tk.Tk()
        root.title("Test Box")
        root.geometry("300x200")
        
        def show_popup():
            messagebox.showinfo("Information", "This is a popup box!")

        button = tk.Button(root, text="Click Me!", command=show_popup)
        button.pack(pady=50) 
        
        root.mainloop()

