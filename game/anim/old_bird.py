from game.anim.anim import Anim
import time

class OldBird(Anim):
    def __init__(self, intelligence, game_state):
        self.name = "old_bird"
        super().__init__(intelligence, game_state)
