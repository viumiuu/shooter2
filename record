import json
import os

RECORD_FILE = "record.json"

def load_record():
    if os.path.exists(RECORD_FILE):
        with open(RECORD_FILE, "r") as file:
            try:
                data = json.load(file)
                return data.get("record", 0)
            except:
                return 0
    return 0

def save_record(new_record):
    with open(RECORD_FILE, "w") as file:
        json.dump({"record": new_record}, file)
