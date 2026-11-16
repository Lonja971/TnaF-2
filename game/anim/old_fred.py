from game.anim.anim import Anim
import time

class OldFred(Anim):
    def __init__(self, intelligence, locations):
        self.name = "old_fred"
        super().__init__(intelligence, locations)
