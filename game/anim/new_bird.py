from game.anim.anim import Anim
import time

class NewBird(Anim):
    def __init__(self, intelligence, locations):
        self.name = "new_bird"
        super().__init__(intelligence, locations)