from game.anim.anim import Anim
import time

class NewFred(Anim):
    def __init__(self, intelligence, locations):
        self.name = "new_fred"
        super().__init__(intelligence, locations)
