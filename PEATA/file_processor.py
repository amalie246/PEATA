import json
import csv
import os
import openpyxl
import pandas as pd
from openpyxl import Workbook
from pathlib import Path
from config import JSON_FOLDER, CSV_FOLDER, EXPORTS_FOLDER

class FileProcessor: 
    

    def export_as_excel(self, filename, data):
        self.add_url(filename, data)
         
        if filename is None:
             raise ValueError("Needs a filename")
            
        if isinstance(data, dict):
            data = [data]
        
        try:
            dataframe = pd.DataFrame(data)
            filepath = Path(EXPORTS_FOLDER) / f"{filename}.xlsx"
            dataframe.to_excel(filepath, index=False)
            
            print("Saved as excel")
            return 0
        
        except Exception as e:
            print(f"Error while saving xlsx file: {e}")
            return 1
        
        
    def export_data_as_csv(self, filename, data):
        self.add_url(filename, data)
        if filename is None:
            raise ValueError("Needs a filename")
        if isinstance(data, dict):
            data = [data]
        filename = filename.rsplit(".", 1)[0]
        try:
            csv_filepath = Path(CSV_FOLDER) / f"{filename}.csv"
            with open(csv_filepath, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
                print(f"CSV file saved: {csv_filepath}")
                return 0
        except Exception as e:
            print(f"Error while saving CSV file: {e}")
            return 1

            

    def add_url(self, filename, data):
        if "VIDEO" in filename:
            for item in data:
                video_id = item.get("id")
                username = item.get("username")
                if video_id and username:
                    url = f"https://www.tiktok.com/@{username}/video/{video_id}"
                    item["url"] = url
                else:
                    item["url"] = "N/A"  
            