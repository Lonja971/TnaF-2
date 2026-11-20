import time

from engine.scene import Scene
from pynput import keyboard

class CustomOptions(Scene):
    def __init__(self, app, save_state, params):
        super().__init__(app)
        self.save_state = save_state
        self.matrix = [[{"name": "old_fred", "intel": 0}, {"name": "old_bon", "intel": 0}, {"name": "old_bird", "intel": 0}, {"name": "old_foxy", "intel": 0}, {"name": "bb", "intel": 0}],
                       [{"name": "new_fred", "intel": 0}, {"name": "new_bon", "intel": 0}, {"name": "new_bird", "intel": 0}, {"name": "mangle", "intel": 0}],
                       [{"name": "ready"}]]
        self.cursor = [0,0]
        self._intel_input_buffer = ""
        self._last_intel_input_at = 0.0
        self.curr_frame_data = {
            "room": "custom_options",
            "sprites": {
                "custom_icons": {
                    "type": "static"
                },
                "custom_options_grid": {
                    "type": "generated",
                    "data": {
                        "matrix": self.matrix,
                        "cursor": self.cursor
                    }
                },
                "custom_options_ready": {
                    "type": "generated",
                    "data": {
                        "cursor": self.cursor,
                        "ready_position": [2, 0]
                    }
                },
                "return": {
                    "type": "generated",
                    "data": {
                        "text": "'c' or 'esc' to return/nnumbers  to  choose  i ntelligence ( 0 - 20 )"
                    }
                }
            }
        }

        super().on_enter()

    def on_enter(self):
        pass

    def handle_input(self, input):
        if input.was_pressed(keyboard.Key.esc) or input.was_pressed(keyboard.KeyCode.from_char('c')):
            self.app.set_scene("menu")
            return

        previous_cursor = self.cursor[:]
        row, column = self.cursor

        if input.was_pressed(keyboard.Key.left):
            column = max(0, column - 1)
        elif input.was_pressed(keyboard.Key.right):
            column = min(len(self.matrix[row]) - 1, column + 1)
        elif input.was_pressed(keyboard.Key.up):
            row = max(0, row - 1)
            column = min(column, len(self.matrix[row]) - 1)
        elif input.was_pressed(keyboard.Key.down):
            row = min(len(self.matrix) - 1, row + 1)
            column = min(column, len(self.matrix[row]) - 1)

        self.cursor[:] = [row, column]
        if self.cursor != previous_cursor:
            self._intel_input_buffer = ""

        item = self.matrix[row][column]
        if item.get("name") == "ready":
            self._intel_input_buffer = ""
            if (
                input.was_pressed(keyboard.Key.enter)
                or input.was_pressed(keyboard.KeyCode.from_char("x"))
            ):
                anim = {
                    matrix_item["name"]: {
                        "intelligence": matrix_item["intel"]
                    }
                    for matrix_row in self.matrix
                    for matrix_item in matrix_row
                    if matrix_item.get("name") != "ready"
                }
                self.app.set_scene("game", {"night_num": 7, "anim": anim})
            return

        digit = next(
            (
                str(value)
                for value in range(10)
                if input.was_pressed(keyboard.KeyCode.from_char(str(value)))
            ),
            None
        )
        if digit is None:
            return

        now = time.monotonic()
        if now - self._last_intel_input_at > 1.0 or len(self._intel_input_buffer) >= 2:
            self._intel_input_buffer = ""

        self._intel_input_buffer += digit
        intel = min(int(self._intel_input_buffer), 20)
        item["intel"] = intel
        if intel == 20:
            self._intel_input_buffer = "20"
        self._last_intel_input_at = now

    def extra_update(self):
        pass
        #self.timer = self.timer + 1
        #if self.timer >= 300 and "newspaper_uit" not in self.curr_frame_data["sprites"]:
        #    self.curr_frame_data["sprites"]["newspaper_uit"] = self.animation_sprite
        #if self.timer >= 325:
        #    all_completed_events = self.save_state.data["completed_events"]
        #    all_completed_events.append(self.event_name)
        #    update_config_value("save.json", "completed_events", all_completed_events)
#
        #    self.app.set_scene("game", {"night_num": self.night_num})