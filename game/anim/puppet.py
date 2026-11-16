from game.anim.anim import Anim
import time

class Puppet(Anim):
    def __init__(self, intelligence, locations):
        self.name = "puppet"
        super().__init__(intelligence, locations)
