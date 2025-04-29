import tkinter as tk
import tkinter.ttk as ttk

class VideoQueryWidget(tk.Frame):
    
    def __init__(self, parent, on_submit):
        super().__init__(parent, bg="#3A3A3A")
        self.on_submit = on_submit
        self.rows = []
        self.containers = []

        self.bool_op = ["AND", "OR", "NOT"]
        self.video_fields = [
            "username", "keyword", "create_date", "region_code", "video_id",
            "hashtag_name", "music_id", "effect_id", "video_length"
        ]

        self.build_ui()
    
    def build_ui(self):
        tk.Label(self, text="Enter parameters for video queries", font=("Helvetica", 10, "bold"), fg="white", bg="#3A3A3A").pack(pady=10)

        tk.Label(self, text="Start date (YYYYMMDD)", font=("Helvetica", 8, "bold"), fg="white", bg="#3A3A3A").pack()
        self.startdate_var = tk.StringVar()
        tk.Entry(self, textvariable=self.startdate_var, bg="lightgrey", fg="black").pack(pady=5)

        tk.Label(self, text="End date (≤30 days later)", font=("Helvetica", 8, "bold"), fg="white", bg="#3A3A3A").pack()
        self.enddate_var = tk.StringVar()
        tk.Entry(self, textvariable=self.enddate_var, bg="lightgrey", fg="black").pack(pady=5)

        self.add_dropdown_row("username", "")
        self.add_dropdown_row("keyword", "")

        tk.Button(self, text="Add row", command=self.add_dropdown_row).pack(pady=5, side="bottom")
        tk.Button(self, text="Submit", command=self.submit).pack(pady=5, side="bottom")
        
    
    def add_dropdown_row(self, default_field=None, default_value=""):
        container = tk.Frame(self, bg="#3A3A3A")
        container.pack(pady=5)
        self.containers.append(container)

        bool_var = tk.StringVar(value=self.bool_op[0])
        field_var = tk.StringVar(value=default_field or self.video_fields[0])
        value_var = tk.StringVar(value=default_value)

        tk.OptionMenu(container, bool_var, *self.bool_op).pack(side="left")
        tk.OptionMenu(container, field_var, *self.video_fields).pack(side="left")
        tk.Entry(container, textvariable=value_var).pack(side="left")

        tk.Button(container, text="-", command=lambda: self.remove_row(container)).pack(side="left")

        self.rows.append((bool_var, field_var, value_var))

    def remove_row(self, container):
        idx = self.containers.index(container)
        container.destroy()
        self.containers.pop(idx)
        self.rows.pop(idx)

    def submit(self):
        start = self.startdate_var.get()
        end = self.enddate_var.get()
        conditions = [(b.get(), f.get(), v.get()) for b, f, v in self.rows]
        self.on_submit(conditions, start, end)