import tkinter as tk
import tkinter.ttk as ttk

class UiConfig:
    def create_button(self, text, command, frame):
        button = tk.Button(frame, command=command, text=text,
                           fg="white", bg="#232323",
                           font=("Helvetica", 10, "bold"),
                           width=30, height=2)
        button.pack(padx=10, pady=10)

        return button
