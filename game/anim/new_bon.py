from game.anim.anim import Anim
import time
from utils.log import debug_log

class NewBon(Anim):
    def __init__(self, intelligence, game_state):
        self.name = "new_bon"
        super().__init__(intelligence, game_state)
