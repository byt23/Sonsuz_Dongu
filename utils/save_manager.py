import json
import os

SAVE_FILE = "save_data.json"

class SaveManager:
    @staticmethod
    def load_data():
        """Kayıt dosyasını okur. Yoksa varsayılan oluşturur."""
        if not os.path.exists(SAVE_FILE):
            default_data = {"unlocked_levels": 1}
            SaveManager.save_data(default_data)
            return default_data
        
        try:
            with open(SAVE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"unlocked_levels": 1}

    @staticmethod
    def save_progress(level_completed):
        """Level tamamlandığında bir sonraki leveli açar."""
        data = SaveManager.load_data()
        current_unlocked = data.get("unlocked_levels", 1)
        
        # Eğer tamamlanan level son açılandan büyükse veya eşitse, bir sonrakini aç
        # Örneğin Level 1 bitti, Level 2 açılsın.
        next_level = level_completed + 1
        
        if next_level > current_unlocked:
            data["unlocked_levels"] = next_level
            SaveManager.save_data(data)

    @staticmethod
    def save_data(data):
        with open(SAVE_FILE, 'w') as f:
            json.dump(data, f)