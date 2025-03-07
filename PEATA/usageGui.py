import tkinter as tk
from tkinter import messagebox
import requests

class Gui:
    def __init__(self, cs, ci, ck):
        self.client_secret = cs
        self.client_id = ci
        self.client_key = ck
    
    def page(self):
        #LT/LTE/GT/GTE must be used for date i think
        #And i think IN is in a gange of some sort
        boolean_operations = ["and", "or", "not"]
        eq_operations = ["EQ", "IN", "LT", "LTE", "GT", "GTE"]
        video_fields = []
        user_info_fields = []
        comment_fields = []
        
        root = tk.Tk()
        root.title("Test Box")
        root.geometry("500x500")
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

