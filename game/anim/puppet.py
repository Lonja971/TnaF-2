from game.anim.anim import Anim

class Puppet(Anim):
    def __init__(self, intelligence, game_state):
        self.name = "puppet"
        self.is_released = False
        self.escape_progress = 0.0
        self.has_left_box = False
        super().__init__(intelligence, game_state)
        self.phase = "boxed"

    def escape_duration(self):
        # Higher Puppet AI means it gets out of the box sooner.
        return max(5.0, 15.0 - 0.5 * self.intelligence)

    def schedule_next_move(self, delay=None):
        if delay is None:
            # At AI 20 Puppet advances every second instead of waiting five seconds.
            delay = max(1.0, self.MOVE_INTERVAL - 0.2 * self.intelligence)
        super().schedule_next_move(delay)

    def try_move(self):
        # Once out of the box, Puppet always advances when its move timer expires.
        return self.has_left_box

    def phase_for_position(self, position):
        return {
            11: self.phase if self.is_released else "boxed",
            20: "attack",
        }.get(position, "moving")

    def update(self, dt):
        if self.pos == 20:
            return

        if self.has_left_box:
            # Once fully out, Puppet follows the configured path and cannot be stopped.
            super().update(dt)
            return

        power = self.game_state.music_box.power
        if power <= 0:
            self.is_released = True
            self.escape_progress = min(
                1.0,
                self.escape_progress + dt / self.escape_duration(),
            )
        elif self.is_released:
            self.escape_progress = max(
                0.0,
                self.escape_progress - dt / self.escape_duration(),
            )

        if not self.is_released:
            self.phase = "boxed"
            return

        if self.escape_progress == 0.0:
            self.is_released = False
            self.phase = "boxed"
            return

        if self.escape_progress < 0.33:
            self.phase = "waking"
        elif self.escape_progress < 0.75:
            self.phase = "emerging"
        else:
            self.phase = "aggressive"

        if self.escape_progress >= 1.0:
            self.has_left_box = True
            self.phase = "aggressive"
            self.activate()
            # The first configured edge is the actual exit from the box; take it now.
            self.move()
