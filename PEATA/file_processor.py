import json
import csv
import os
import openpyxl
import pandas as pd
from openpyxl import Workbook
from pathlib import Path
from config import JSON_FOLDER, CSV_FOLDER, EXPORTS_FOLDER

class FileProcessor: 
    
    def __init__(self):
        self.data = None 
        self.file_path = self.get_latest_csv_file() 
    
    @staticmethod
    def save_json_to_file(data, filename="data.json"):
        try:
            with open(Path(JSON_FOLDER) / filename, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
                print(f"JSON-data lagret i {filename}")
        except Exception as e:
            print(f"Error while saving JSON file: {e}")


    
    @staticmethod
    def save_json_to_csv(data, filename="data.csv"):
        if not data or not isinstance(data, list) or not isinstance(data[0], dict):
            print("No valid data to save")
            return
        
        try: 
            filepath = Path(CSV_FOLDER) / filename
            with open(filepath, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writerows(data)

            print(f"JSON-data lagret i CSV-fil: {filename}")
        except Exception as e:
            print(f"Error while saving CSV file: {e}")


    @staticmethod
    def save_any_json_data(data, filename="output", file_format="json"):
        try:
           if file_format == "json":
               FileProcessor.save_json_to_file(data, f"{filename}.json")
               
           elif file_format == "csv":      
               FileProcessor.save_json_to_csv(data, f"{filename}.csv")
               
           else:
               print("Invalid file format.")
        except Exception as e:
           print(f"Error while saving data: {e}")
            
    
    def get_latest_csv_file(self):
        csv_files = list(Path(CSV_FOLDER).glob("*.csv"))
        if not csv_files:
            print("No CSV files found.")
            return None
        
        latest_file = max(csv_files, key=os.path.getmtime) 
        return latest_file
    
    def open_file(self):
        if not self.file_path:
            print("No CSV file to open.")
            return None
        try:
            with open(self.file_path, mode= 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.data = [row for row in reader]
                print(f"{self.file_path} opened")
                return self.data
        except FileNotFoundError:
                print("Could not find the file")
                return self.data
        except Exception as e: 
            print("Error while opening file")
            
        
        
    def close_file(self):
        if self.data is not None:
            self.data = None
            print("File data has been cleared from memory.")
        else: 
            print("No file data to close.")
        
     

   
    #chose to remove panda because we dont have big data sets       
    def export_as_excel(self):
        if self.data is None:
            print("No data available to export.")
            return
        try:
            wb = Workbook()
            ws = wb.active
            ws.append(list(self.data[0].keys()))
            
            for row in self.data:
                ws.append(list(row.values()))
            
            output_excel = Path(EXPORTS_FOLDER) / (self.file_path.stem + ".xlsx")
            wb.save(output_excel)
            print("Csv file exported to excel successfully")
            
        except Exception as e: 
            print(f"Error occured while exporting file: {e}")


    def export_data(self, filename, data):
        if filename is None:
            raise ValueError("Needs a filename")
            return
        
        if isinstance(data, dict):
            data = [data]
        #removes .csv or .json if that is in the filename
        filename = filename.rsplit(".", 1)[0] 
        #save data as csv
        try: 
            csv_filepath = Path(CSV_FOLDER) / f"{filename}.csv"
            with open(csv_filepath, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

            print(f"JSON-data saved in CSV-file: {filename}")
            
            excel_filepath = Path(EXPORTS_FOLDER) / f"{filename}.xlsx"
            df = pd.read_csv(csv_filepath)
            df.to_excel(excel_filepath, index=False, engine='openpyxl')
            
            print(f"Excel data saved: {excel_filepath}")
            return 0
        except Exception as e:
            print(f"Error while saving CSV file: {e}")
            return 1
        
        
            
#if __name__ == "__main__":
    #file_processor = FileProcessor()
    #data = file_processor.open_file()
    
    #if data is not None:
     #   file_processor.export_as_excel()
      #  file_processor.close_file()
            
            
            
# """ Example Usage """            
# file_handler = FileHandler()  # Instantiate the class
# data = file_handler.open_file()

# if data is not None: 

# """ Export as PDF and Excel"""
# file_handler.export_as_pdf()
# file_handler.export_as_excel()


# """ Close file """
# file_handler.close_file()
