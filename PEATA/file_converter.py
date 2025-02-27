import json
import csv

def save_json_to_file(data, filename="data.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"JSON-data lagret i {filename}")

def save_json_to_csv(data, filename="data.csv"):
    if not data or not isinstance(data, list) or not isinstance(data[0], dict):
        print("Ingen gyldige data å lagre.")
        return
    
    fieldnames = set()
    for item in data:
        fieldnames.update(item.keys())

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=sorted(fieldnames))
        writer.writeheader()
        for item in data:
            writer.writerow(item) 

    print(f"JSON-data lagret i CSV-fil: {filename}")


def save_any_json_data(data, filename="output", file_format="json"):
    filename = f"{filename}.{file_format}"
    if file_format == "json":
        save_json_to_file(data, filename)
    elif file_format == "csv":
        save_json_to_csv(data, filename)
