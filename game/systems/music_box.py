class MusicBox:
    # The original box starts at 2000 and loses 2-6 points every 0.05 seconds.
    # Power is displayed on a 0-100 scale here, so these are the equivalent rates.
    DISCHARGE_PER_SECOND = {
        1: 2.0,
        2: 2.0,
        3: 3.0,
        4: 4.0,
        5: 5.0,
        6: 6.0,
        7: 6.0,
    }

    def __init__(self, night_num):
        self.power = 100
        self.charge_per_second = 15.0
        self.discharge_per_second = self.DISCHARGE_PER_SECOND.get(night_num, 6.0)
        self.starts_at_two_am = night_num == 1

    def update(self, state, dt):
        if self.starts_at_two_am and state.time.time[0] in (12, 1):
            return

        if state.is_winding_music_box:
            self.power = min(100.0, self.power + self.charge_per_second * dt)
            return

        self.power = max(0.0, self.power - self.discharge_per_second * dt)

    def charge(self, amount=5):
        self.power = min(100.0, self.power + amount)
