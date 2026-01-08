import os
import shutil
from utils.paths import SAVE_DIR

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(PROJECT_ROOT, "config")

def ensure_config(filename):
    """
    Якщо файлу нема в AppData — копіює з project/config/*.template.json
    """
    target_path = os.path.join(SAVE_DIR, filename)
    template_path = os.path.join(
        TEMPLATE_DIR,
        filename.replace(".json", ".template.json")
    )

    if os.path.exists(target_path):
        return

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found: {template_path}")

    shutil.copy(template_path, target_path)