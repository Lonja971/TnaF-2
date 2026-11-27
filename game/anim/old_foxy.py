from game.anim.anim import Anim
import random
import time

class OldFoxy(Anim):
    def __init__(self, intelligence, game_state):
        self.name = "old_foxy"
        self.pressure = 0.0
        self.flash_time = 0.0
        self.stun_until = 0.0
        self.flash_required = max(1.0, 1.67 * min(game_state.night_num, 6))
        super().__init__(intelligence, game_state)

    def try_move(self):
        # Foxy's hallway movement opportunity uses his own rising pressure value.
        return random.randint(21, 25) - self.pressure <= min(self.intelligence, 17)

    def update(self, dt):
        if not self.is_active or self.pos == 20:
            return

        if self.game_state.light == "centre":
            self.pressure = 0.0

        if self.pos == 13:
            if self.game_state.light == "centre":
                self.flash_time += dt
                if self.flash_time >= self.flash_required:
                    self.change_pos(self.reset_pos)
                    self.flash_time = 0.0
                    self.stun_until = time.monotonic() + random.uniform(500, 999) / 60
                return

        office_is_occupied = bool(self.locations.get(15, []))
        if self.game_state.light != "centre" and not office_is_occupied:
            self.pressure += dt * (2.0 if self.game_state.is_mask else 1.0)

        if time.monotonic() < self.stun_until:
            return

        if self.pos == 15:
            # The mask does not fool Foxy; only hallway light can repel him.
            if self.game_state.is_camera_open or self.game_state.is_tablet_opening_anim:
                return
            self.office_attack_time += dt
            if self.office_attack_time >= 0.75:
                self.is_attacking = True
                self.change_pos(20)
            return

        if self.next_move_time is None:
            self.schedule_next_move()
            return
        if time.monotonic() >= self.next_move_time:
            if self.try_move():
                self.move()
            else:
                self.schedule_next_move()
