from game.anim.anim import Anim
import time

class OldFoxy(Anim):
    def __init__(self, intelligence, locations):
        self.name = "old_foxy"
        super().__init__(intelligence, locations)
