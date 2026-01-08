from utils.save import load_config

class SaveState:
    def __init__(self):
        self.data = load_config("save.json")

    def update(self):
        self.data = load_config("save.json")