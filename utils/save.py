import json, os
from utils.paths import SAVE_DIR
    
def load_config(filename):
    path = os.path.join(SAVE_DIR, filename)
    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(filename, data):
    path = os.path.join(SAVE_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def update_config_value(filename, key, value):
    data = load_config(filename) or {}
    data[key] = value
    save_config(filename, data)

def update_config_path(filename, path, value):
    """
    path = ["progress", "night"]
    """
    data = load_config(filename) or {}

    ref = data
    for key in path[:-1]:
        ref = ref.setdefault(key, {})

    ref[path[-1]] = value
    save_config(filename, data)