import time

from game.anim.anim import Anim

class BB(Anim):
    def __init__(self, intelligence, game_state):
        self.name = "bb"
        super().__init__(intelligence, game_state)

    def enter_office(self):
        self.change_pos(15)
        self.game_state.buttery.power = 0
        self.game_state.light = None
        self.game_state.is_camera_light = False

    def update(self, dt):
        if not self.is_active or self.pos == 15 or self.pos == 20:
            return

        if self.pos == 16:
            if self.game_state.is_mask:
                if self.update_vent(dt):
                    return
            else:
                self.mask_hold_time = 0.0

        if self.next_move_time is None:
            self.schedule_next_move()
            return
        if time.monotonic() >= self.next_move_time:
            if self.try_move():
                if self.pos == 16 and self.can_move_to(15):
                    self.enter_office()
                else:
                    self.move()
            else:
                self.schedule_next_move()
