from game.anim.anim import Anim
import time

class Puppet(Anim):
    def __init__(self, intelligence):
        self.name = "puppet"
        super().__init__(intelligence)

    def update(self):
        if self.next_move_time == None:
            self.schedule_next_move()
            return
        
        if time.time() >= self.next_move_time:
            self.try_move()
            self.schedule_next_move()