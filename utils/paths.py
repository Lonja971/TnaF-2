import os
from appdirs import user_data_dir

APP_NAME = "TNAF2"
APP_AUTHOR = "MrStinger__"

SAVE_DIR = user_data_dir(APP_NAME, APP_AUTHOR)
os.makedirs(SAVE_DIR, exist_ok=True)