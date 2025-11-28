import json
import os

class ConfigManager:
    def __init__(self, file_path="config.json"):
        self.file_path = file_path
        self.config = self.load()

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        else:
            default_data = {
                "terminal_min_width": 200,
                "terminal_min_height": 50,
                "volume": 80,
                "controls": {
                    "up": "KEY_UP",
                    "down": "KEY_DOWN",
                    "left": "KEY_LEFT",
                    "right": "KEY_RIGHT",
                    "action": "ENTER"
                }
            }
            self.save(default_data)
            return default_data

    def save(self, data=None):
        if not data:
            data = self.config

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @property
    def terminal_min_width(self):
        return self.config.get("terminal_min_width", 200)

    @property
    def terminal_min_height(self):
        return self.config.get("terminal_min_height", 50)