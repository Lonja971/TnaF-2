from game.anim.anim import Anim
import time

class Mangle(Anim):
    def __init__(self, intelligence, game_state):
        self.name = "mangle"
        super().__init__(intelligence, game_state)
