import json
import csv
import os
from PEATA.config import JSON_FOLDER, CSV_FOLDER

"""Haven't tested with modified code yet, might not work fully."""

class FileConverter:
   
     
    def save_json_to_file(data, filename="data.json"):
        #Save JSON data to a file in the 'json' folder
        # V Causes tests to FAIL due to filepath bein
        filepath = os.path.join(JSON_FOLDER, filename)
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"JSON-data lagret i {filepath}") # filepath eller filename?

    def save_json_to_csv(self, data, filename="data.csv"):
        if not data or not isinstance(data, list) or not isinstance(data[0], dict):
            print("Ingen gyldige data å lagre.")
            return
        
        fieldnames = set()
        for item in data:
            fieldnames.update(item.keys())

        #Save CSV file in the 'csv' folder
        filepath = os.path.join(CSV_FOLDER, filename)
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=sorted(fieldnames))
            writer.writeheader()
            for item in data:
                writer.writerow(item) 

        print(f"JSON-data lagret i CSV-fil: {filename}")


    def save_any_json_data(self, data, filename="output", file_format="json"):
        filename = f"{filename}.{file_format}"
        if file_format == "json":
            self.save_json_to_file(data, filename)
        elif file_format == "csv":
            self.save_json_to_csv(data, filename)

