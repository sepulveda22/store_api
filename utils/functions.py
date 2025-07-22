import json
import os
def read_data():
    try:
        with open("config.json", 'r', encoding="utf-8") as file:
            config = json.load(file)
            return config
    except Exception as e:
            print(f"File not found: {e}")
            return None