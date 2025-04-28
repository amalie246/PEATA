import os

BASE_FOLDER = "data"
JSON_FOLDER = os.path.join(BASE_FOLDER, "json")
CSV_FOLDER = os.path.join(BASE_FOLDER, "csv")
EXPORTS_FOLDER = os.path.join(BASE_FOLDER, "exports")

os.makedirs(JSON_FOLDER, exist_ok=True)
os.makedirs(CSV_FOLDER, exist_ok=True)
os.makedirs(EXPORTS_FOLDER, exist_ok=True)