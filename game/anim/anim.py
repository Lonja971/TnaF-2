import random
import time

from config.anim import ANIMATRONICS
from utils.log import debug_log


class Anim:
    """Shared movement and office-defense behavior for FNaF 2 animatronics."""

    MOVE_INTERVAL = 5.0
    MASK_REPEL_TIME = 5.0
    VENT_POSITIONS = {5, 6, 16, 17}

    def __init__(self, intelligence, game_state):
        self.game_state = game_state
        self.locations = game_state.locations
        anim_data = ANIMATRONICS[self.name]
        self.def_pos = anim_data["default_position"]
        self.reset_pos = anim_data.get("reset_position", self.def_pos)
        self.path_graph = anim_data["path_graph"]
        self.pos = self.def_pos
        self.intelligence = self._clamp_intelligence(intelligence)
        self.is_active = False
        self.is_attacking = False
        self.next_move_time = None
        self.office_attack_time = 0.0
        self.mask_hold_time = 0.0
        self.phase = "idle"

        self.locations.setdefault(self.pos, []).append(self.name)

    @staticmethod
    def _clamp_intelligence(intelligence):
        return max(0, min(20, int(intelligence or 0)))

    def set_intelligence(self, intelligence):
        was_inactive = self.intelligence <= 0
        self.intelligence = self._clamp_intelligence(intelligence)
        if was_inactive and self.intelligence > 0:
            self.activate()

    def activate(self):
        self.is_active = True
        if self.next_move_time is None:
            self.schedule_next_move()

    def schedule_next_move(self, delay=None):
        if delay is None:
            delay = self.MOVE_INTERVAL
        self.next_move_time = time.monotonic() + delay

    def try_move(self):
        return random.randint(1, 20) <= self.intelligence

    def can_move_to(self, new_pos):
        occupants = self.locations.get(new_pos, [])
        others = [name for name in occupants if name != self.name]

        if new_pos in self.VENT_POSITIONS and others:
            return False

        if new_pos == 1 and self.name == "old_bon" and "new_bird" in others:
            return False
        if new_pos == 1 and self.name == "new_bird" and "old_bon" in others:
            return False
        if new_pos == 4 and self.name == "old_bird" and "new_bird" in others:
            return False
        if new_pos == 4 and self.name == "new_bird" and "old_bird" in others:
            return False

        if new_pos == 15:
            attackers = [name for name in others if name != "bb"]
            if attackers:
                return False
            if self.name != "bb" and self.pos in {16, 17} and not self.game_state.is_camera_open:
                return False

        return True

    def move(self):
        possible_positions = self.path_graph.get(self.pos, [])
        if not possible_positions:
            self.change_pos(self.reset_pos)
            return

        possible_positions = list(possible_positions)
        random.shuffle(possible_positions)
        for new_pos in possible_positions:
            if self.can_move_to(new_pos):
                self.change_pos(new_pos)
                return
        self.schedule_next_move()

    def change_pos(self, new_pos):
        old_pos = self.pos
        old_occupants = self.locations.get(old_pos, [])
        if self.name in old_occupants:
            old_occupants.remove(self.name)

        self.pos = new_pos
        self.locations.setdefault(new_pos, []).append(self.name)
        self.office_attack_time = 0.0
        self.mask_hold_time = 0.0
        self.is_attacking = False
        self.phase = self.phase_for_position(new_pos)
        self.schedule_next_move()
        debug_log(f"{self.name} moved from {old_pos} to {new_pos}")

    def phase_for_position(self, position):
        return "office" if position == 15 else "moving"

    def return_after_mask(self):
        target = self.reset_pos
        if not self.can_move_to(target):
            target = self.def_pos
        if not self.can_move_to(target):
            # Stay in the current non-office room until its reset spot is free.
            self.schedule_next_move()
            return
        self.change_pos(target)

    def office_attack_window(self):
        # The harder the AI, the shorter the guard's reaction window.
        return max(0.75, 1.75 - 0.05 * (self.intelligence - 1))

    def update_office(self, dt):
        if self.game_state.is_mask:
            self.mask_hold_time += dt
            if self.mask_hold_time >= self.MASK_REPEL_TIME:
                self.return_after_mask()
            return

        self.mask_hold_time = 0.0
        if self.game_state.is_camera_open or self.game_state.is_tablet_opening_anim:
            return

        self.office_attack_time += dt
        if self.office_attack_time >= self.office_attack_window():
            self.is_attacking = True
            self.change_pos(20)

    def update_vent(self, dt):
        if not self.game_state.is_mask:
            self.mask_hold_time = 0.0
            return False

        self.mask_hold_time += dt
        if self.mask_hold_time >= self.MASK_REPEL_TIME:
            self.return_after_mask()
        return True

    def update(self, dt):
        if not self.is_active:
            return
        if self.pos == 20:
            return
        if self.pos == 15:
            self.update_office(dt)
            return
        if self.pos in {16, 17} and self.update_vent(dt):
            return

        if self.next_move_time is None:
            self.schedule_next_move()
            return
        if time.monotonic() >= self.next_move_time:
            if self.try_move():
                self.move()
            else:
                self.schedule_next_move()
