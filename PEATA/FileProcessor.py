#combining fileHandler and fileconverter

import json
import csv
import os
import openpyxl
from openpyxl import Workbook
from pathlib import Path
from config import JSON_FOLDER, CSV_FOLDER, EXPORTS_FOLDER

class FileProcessor: 
    
    def __init__(self):
        self.data = None # Store the DataFrame
        self.file_path = self.get_latest_csv_file() 
    
    @staticmethod
    def save_json_to_file(data, filename="data.json"):
        #Save JSON data to a file in the 'json' folder
        filepath = os.path.join(JSON_FOLDER, filename)
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"JSON-data lagret i {filename}")


    
    @staticmethod
    def save_json_to_csv(data, filename="data.csv"):
        if not data or not isinstance(data, list) or not isinstance(data[0], dict):
            print("Ingen gyldige data å lagre.")
            return
        
        fieldnames = set()
        for item in data:
            fieldnames.update(item.keys())

        #Save CSV file in the 'csv' folder
        filepath = os.path.join(CSV_FOLDER, filename)
        with open(filepath, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=sorted(fieldnames))
            writer.writeheader()
            for item in data:
                writer.writerow(item) 

        print(f"JSON-data lagret i CSV-fil: {filename}")


    @staticmethod
    def save_any_json_data(data, filename="output", file_format="json"):
        filename = f"{filename}.{file_format}"
        if file_format == "json":
            FileProcessor.save_json_to_file(data, filename)
        elif file_format == "csv":
            FileProcessor.save_json_to_csv(data, filename)
            
    
    # No need to manually specify the filename each time
    def get_latest_csv_file(self):
        # Find the most recently modified CSV file in the CSV folder
        csv_files = list(Path(CSV_FOLDER).glob("*.csv"))
        if not csv_files:
            print("No CSV files found.")
            return None
        
        latest_file = max(csv_files, key=os.path.getmtime) 
        print(f"Latest CSV file detected: {latest_file}")
        return latest_file
    
    def open_file(self):
        # Opens the latest CSV file and returns the data as a list
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
       # Closes the file by deleting the stored DataFrame reference.
        if self.data is not None:
            self.data = None # Clear the DataFrame from memory
            print("File data has been cleared from memory.")
        else: 
            print("No file data to close.")
        
     
        
     
    @staticmethod
    def csv_to_excel(csv_file, excel_file):
        csv_data = []
        with open(csv_file) as file_obj:
            reader = csv.reader(file_obj)
            for row in reader: 
                csv_data.append(row)
                
        #creating excel
        workbook = openpyxl.Workbook()
        sheet = workbook.active
                
                
        #adding rows from csv to excel
        for row in csv_data: 
            sheet.append(row)
        workbook.save(excel_file)
   
        
   
    #chose to remove panda because we dont have big data sets       
    def export_as_excel(self):
        if self.data is None:
            print("No data available to export.")
            return
        try:
            wb = Workbook()
            ws = wb.active
            
            
            for row in self.data:
                ws.append(list(row.values()))
            
            output_excel = Path(EXPORTS_FOLDER) / (self.file_path.stem + ".xlsx")
            wb.save(output_excel)
            print("Csv file exported to excel successfully")
            
        except Exception as e: 
            print(f"Error occured while exporting file: {e}")


            
            
            
if __name__ == "__main__":
    file_processor = FileProcessor()
    data = file_processor.open_file()
    
    if data is not None:
        file_processor.export_as_excel()
        file_processor.close_file()
            
            
            
# """ Example Usage """            
# file_handler = FileHandler()  # Instantiate the class
# data = file_handler.open_file()

# if data is not None: 

# """ Export as PDF and Excel"""
# file_handler.export_as_pdf()
# file_handler.export_as_excel()


# """ Close file """
# file_handler.close_file()
