from game.anim.anim import Anim
import time

class BB(Anim):
    def __init__(self, intelligence, locations):
        self.name = "bb"
        super().__init__(intelligence, locations)
