from utils.log import debug_log

class MusicBox:
    def __init__(self, discharge_per_tick):
        self.power = 100
        self.charge_per_tick = 5
        self.discharge_per_tick = discharge_per_tick

    def update(self, state):
        if self.power == 0: return

        self.power -= self.discharge_per_tick

    def charge(self):
        new_level = self.power + self.charge_per_tick
        if new_level > 100: new_level = 100
        self.power = new_level
