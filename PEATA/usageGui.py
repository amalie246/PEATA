import tkinter as tk
from tkinter import messagebox
import requests

class Gui:
    def __init__(self, cs, ci, ck):
        self.client_secret = cs
        self.client_id = ci
        self.client_key = ck
    
    def page(self):
        boolean_operations = ["and", "or", "not"]
        #LT/LTE/GT/GTE must be used for date i think
        #And i think IN is in a gange of some sort
        eq_operations = ["EQ", "IN", "LT", "LTE", "GT", "GTE"]
        video_fields = []
        user_info_fields = []
        comment_fields = []
        
        root = tk.Tk()
        root.title("Test Box")
        root.geometry("300x200")
        def show_selection():
            selected_option = dropdown_boolean_operations.get()
        
        dropdown_boolean_operations = tk.StringVar(root)
        #sdropdown_boolean_operations.set[boolean_operations[0]]
        
        dropdown_boolean = tk.OptionMenu(root, dropdown_boolean_operations, *boolean_operations)
        dropdown_boolean.pack(pady=30)
        
        boolean_operations_btn = tk.Button(root, text="Show bool operations", command=show_selection)
        boolean_operations_btn.pack()
        
        
        def show_popup():
            messagebox.showinfo("Information", "This is a popup box!")

        button = tk.Button(root, text="Click Me!", command=show_popup)
        button.pack(pady=50) 
        
        root.mainloop()

