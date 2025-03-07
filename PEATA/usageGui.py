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
        
        def show_selection():
            label1.config(text=clickedBool.get())
            label2.config(text=clickedEq.get())
            
        dropdown_frame = tk.Frame(root)
        dropdown_frame.pack(pady=20)
        
        clickedBool = tk.StringVar()
        clickedBool.set( "and" )
        clickedEq = tk.StringVar()
        clickedEq.set("EQ")
        
        bool_drop = tk.OptionMenu(dropdown_frame, clickedBool, *boolean_operations)
        bool_drop.grid(row=0, column=0, padx=10)
        eq_drop = tk.OptionMenu(dropdown_frame, clickedEq, *eq_operations)
        eq_drop.grid(row=0, column=2, padx=10)
        
        button = tk.Button(dropdown_frame, text="Submit", command=show_selection)
        button.grid(row=3, column=1, pady=10)
        label1 = tk.Label(dropdown_frame, text=" ")
        label1.grid(row=4, column=0, padx=10)
        label2 = tk.Label(dropdown_frame, text= " ")
        label2.grid(row=4, column=2, padx=10)
        
        
        def show_popup():
            messagebox.showinfo("Information", "This is a popup box!")

        button = tk.Button(root, text="Click Me!", command=show_popup)
        button.pack(pady=50) 
        
        root.mainloop()

