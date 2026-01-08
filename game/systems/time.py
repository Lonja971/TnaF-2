class TimeSystem:
    MS_TICK = 6
    
    def __init__(self):
        self.hour = 12
        self.time = [12, 0]
        self.miliseconds = 0

    def update(self, state):
        ms_total = self.MS_TICK + self.miliseconds

        if ms_total >= 60:
            self.miliseconds = ms_total - 60
            self.time[1] += ms_total // 60

            if self.time[1] >= 60:
                self.time[1] = 60 - self.time[1]
                self.time[0] += 1

                if self.time[0] == 13:
                    self.time[0] = 1
        else:
            self.miliseconds += self.MS_TICK