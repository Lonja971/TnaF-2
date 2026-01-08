from game.anim.anim import Anim
import time

class OldBon(Anim):
    def __init__(self, intelligence):
        self.name = "old_bon"
        super().__init__(intelligence)

    def update(self):
        if self.next_move_time == None:
            self.schedule_next_move()
            return
        
        if time.time() >= self.next_move_time:
            self.try_move()
            self.schedule_next_move()