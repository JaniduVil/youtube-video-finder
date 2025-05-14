import json
from datetime import datetime
from typing import List, Dict

class JSONStorage:
    def __init__(self, file_path: str = "src/data/videos.json"):
        self.file_path = file_path

    def save(self, data: List[Dict], query: str):
        """Append new data to JSON file with a timestamp."""
        try:
            existing_data = []
            try:
                with open(self.file_path, "r") as f:
                    existing_data = json.load(f)
            except FileNotFoundError:
                pass

            new_entry = {
                "query": query,
                "timestamp": str(datetime.now()),
                "videos": data
            }
            existing_data.append(new_entry)

            with open(self.file_path, "w") as f:
                json.dump(existing_data, f, indent=2)
        except Exception as e:
            raise Exception(f"Failed to save data: {e}")