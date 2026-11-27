from game.anim.anim import Anim
import time

class OldBon(Anim):
    def __init__(self, intelligence, game_state):
        self.name = "old_bon"
        super().__init__(intelligence, game_state)
