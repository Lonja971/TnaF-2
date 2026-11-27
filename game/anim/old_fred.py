from game.anim.anim import Anim
import time

class OldFred(Anim):
    def __init__(self, intelligence, game_state):
        self.name = "old_fred"
        super().__init__(intelligence, game_state)
