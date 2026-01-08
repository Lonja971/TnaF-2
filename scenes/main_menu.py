import curses, time, random, sys
from engine.scene import Scene
from utils.log import debug_log
from pynput import keyboard
from scenes.helpers import new_game

class MainMenu(Scene):
    def __init__(self, app, save_state, params):
        super().__init__(app)
        self.save_state = save_state
        self.options_action = [
            lambda: self.app.set_scene("game", {"night_num": self.save_state.data["curr_night"]}),
            lambda: new_game(self.app, self.save_state.update),
            lambda: self.app.set_scene("settings"),
            lambda: sys.exit()
        ]
        self.bg_anim_data = {
            "chica": {
                "old": "menu_anim_old_chica",
                "toy": "menu_anim_toy_chica",
                "toy_interval": [3, 15],
                "old_interval": 3
            },
            "bonnie": {
                "old": "menu_anim_old_bonnie",
                "toy": "menu_anim_toy_bonnie",
                "toy_interval": [3, 15],
                "old_interval": 3
            },
            "freddy": {
                "old": "menu_anim_old_freddy",
                "toy": "menu_anim_toy_freddy",
                "toy_interval": [3, 15],
                "old_interval": 3
            },
        }

        self.curr_frame_data = {
            "room": "main_menu",
            "sprites": {
                "main_menu_options": {
                    "type": "generated",
                    "data": {
                        "selected": 0,
                        "options": [f"Night {self.save_state.data["curr_night"]}", "New game", "Settings", "Quit"]
                    }
                },
                "menu_logo_text": {
                    "type": "static"
                },
                "menu_anim_toy_freddy": {
                    "type": "static"
                },
                "menu_anim_toy_bonnie": {
                    "type": "static"
                },
                "menu_anim_toy_chica": {
                    "type": "static"
                }
            }
        }

        super().on_enter()

    def handle_input(self, input):
        menu_element = self.curr_frame_data["sprites"]["main_menu_options"]
        data = menu_element["data"]

        selected_option = data["selected"]
        options = data["options"]

        if input.was_pressed(keyboard.Key.up):
            if selected_option > 0:
                selected_option -= 1

        if input.was_pressed(keyboard.Key.down):
            if selected_option < len(options) - 1:
                selected_option += 1

        if input.is_held(keyboard.Key.esc):
            exit()

        if input.is_held(keyboard.Key.enter):
            action = self.options_action[selected_option]
            action()

        data["selected"] = selected_option

    def extra_update(self):
        now = time.time()

        for name, el in self.bg_anim_data.items():
            toy = el["toy"]
            old = el["old"]

            if "timer" not in el:
                el["timer"] = now + random.uniform(el["toy_interval"][0], el["toy_interval"][1])

            if now >= el["timer"]:
                sprites = self.curr_frame_data["sprites"]

                if toy in sprites:
                    sprites.pop(toy)
                    sprites[old] = {"type": "static"}
                    el["timer"] = now + el["old_interval"]
                elif old in sprites:
                    sprites.pop(old)
                    sprites[toy] = {"type": "static"}
                    el["timer"] = now + random.uniform(el["toy_interval"][0], el["toy_interval"][1])
