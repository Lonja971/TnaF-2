from game.anim.anim import Anim
import time

class NewFred(Anim):
    def __init__(self, intelligence, game_state):
        self.name = "new_fred"
        super().__init__(intelligence, game_state)
