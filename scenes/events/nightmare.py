from engine.scene import Scene
from utils.save import update_config_value
from pynput import keyboard
from config.sprite_registry import SPRITES
from config.rooms import ROOMS
import time

SIDES = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

class Nightmare(Scene):
    def __init__(self, app, save_state, params):
        super().__init__(app)
        self.save_state = save_state
        self.room = ROOMS["nightmare"]
        self.night_num = params["night_num"]
        if self.night_num == 0:
            self.event_name =f"first_nightmare"
        else:
            self.event_name =f"{self.night_num}_start"
        self.curr_position_index = 5
        self.is_black = False
        self.timer = 0
        self.curr_frame_data = {
            "room": "nightmare",
            "sprites": {
                "nightmare_mask": {
                    "type": "static"
                }
            }
        }
        if self.night_num == 4:
            self.curr_frame_data["sprites"]["nightmare_poppet"] = {"type": "static"}
        self.add_location()
        self.check_if_bon_bird()

        super().on_enter()

    def on_enter(self):
        pass

    def handle_input(self, input):
        if input.was_pressed(keyboard.Key.left):
            if self.curr_position_index - 1 >= 0:
                self.delete_location()
                self.curr_position_index = self.curr_position_index - 1
                self.add_location()
                self.check_if_bon_bird()

        if input.was_pressed(keyboard.Key.right):
            if self.curr_position_index + 1 < len(SIDES):
                self.delete_location()
                self.curr_position_index = self.curr_position_index + 1
                self.add_location()
                self.check_if_bon_bird()


    def extra_update(self):
        self.timer = self.timer + 1
        if self.timer >= 550 and not self.is_black:
            self.curr_frame_data["sprites"]["background_black"] = {"type": "generated"}
            self.curr_frame_data["sprites"]["its_me"] = {"type": "generated", "data": { "text": "Its me" }}
            self.is_black = True
        elif self.timer == 540:
            self.curr_frame_data["sprites"]["glitch"] = {
                "type": "animation",
                "update_in": SPRITES["glitch_white"]["update_in"],
                "frames_num": 6,
                "mode": "hold",
                "data": {
                    "curr_frame": 0,
                    "last_update": time.time()
                }
            }

        elif self.timer >= 610:
            all_completed_events = self.save_state.data["completed_events"]
            all_completed_events.append(self.event_name)
            update_config_value("save.json", "completed_events", all_completed_events)
            self.app.set_scene("menu")

    def delete_location(self):
        sprites = self.curr_frame_data["sprites"]
        side = SIDES[self.curr_position_index]

        night_nr = self.night_num
        if night_nr == 4:
            night_nr = 0

        sprites.pop(f"nightmare_location_{side}", None)
        sprites.pop(f"nightmare_bon_{night_nr}_{side}", None)
        sprites.pop(f"nightmare_bird_{night_nr}_{side}", None)

        if self.night_num == 3:
            sprites.pop(f"nightmare_golden_{side}", None)


    def add_location(self):
        side = SIDES[self.curr_position_index]
        self.curr_frame_data["sprites"][f"nightmare_location_{side}"] = {"type": "static"}

    def check_if_bon_bird(self):
        sprites = self.curr_frame_data["sprites"]
        side = SIDES[self.curr_position_index]
        night_nr = self.night_num
        if night_nr == 4:
            night_nr = 0

        for character in ("bon", "bird"):
            sprite_name = f"nightmare_{character}_{night_nr}_{side}"
            if sprite_name in self.room["sprites"]:
                sprites[sprite_name] = {"type": "static"}
                break

        if self.night_num == 3:
            sprite_name = f"nightmare_golden_{side}"
            if sprite_name in self.room["sprites"]:
                sprites[sprite_name] = {"type": "static"}