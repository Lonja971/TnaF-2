from game.anim.anim import Anim
import time

class Mangle(Anim):
    def __init__(self, intelligence, locations):
        self.name = "mangle"
        super().__init__(intelligence, locations)
