import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk

class UiHelper:
    
    def create_button_with_image(self, text, command, frame):
        btn_image = Image.open("images/GenBtn.png")
        btn_image = btn_image.crop(btn_image.getbbox())
        gen_btn_img = ImageTk.PhotoImage(btn_image)
        
        button = tk.Button(frame, image=gen_btn_img, command=command)
        button.image = gen_btn_img
        button.pack(padx=10)
        
        text_label = tk.Label(frame, text=text, background="#323232", font=("Arial", 10, "bold"), fg="white")
        text_label.place(relx=0.5, rely=0.5, anchor="center")
        
        return button
    
    def update_ui(self, data, label):
        label.config(state=tk.NORMAL)
        label.delete(1.0, tk.END)
        
        if "error" in data:
            message = "Error occured during fetching:"
            label.insert(tk.END, f"{message}\n{data}")
            return
        
        elif isinstance(data, list):
            label.insert(tk.END, f"{data}")
            return
        
        else:
            message = "No data was found with your parameters"
            label.insert(tk.END, f"{message}")
        label.config(state=tk.DISABLED)