import json
import os

class SaveManager:
    FILE_NAME = "save_data.json"
    @staticmethod
    def load_data():
        if not os.path.exists(SaveManager.FILE_NAME): return {"unlocked_levels": 1}
        try:
            with open(SaveManager.FILE_NAME, "r") as f: return json.load(f)
        except: return {"unlocked_levels": 1}
    @staticmethod
    def save_progress(lvl):
        data = SaveManager.load_data()
        if lvl >= data.get("unlocked_levels", 1):
            data["unlocked_levels"] = lvl + 1
            with open(SaveManager.FILE_NAME, "w") as f: json.dump(data, f)