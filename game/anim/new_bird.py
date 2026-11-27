from game.anim.anim import Anim
import time

class NewBird(Anim):
    def __init__(self, intelligence, game_state):
        self.name = "new_bird"
        super().__init__(intelligence, game_state)
