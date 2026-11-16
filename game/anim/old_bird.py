from game.anim.anim import Anim
import time

class OldBird(Anim):
    def __init__(self, intelligence, locations):
        self.name = "old_bird"
        super().__init__(intelligence, locations)
