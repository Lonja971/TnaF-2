from engine.scene import Scene
from utils.save import update_config_value
import time

class Newspaper(Scene):
    def __init__(self, app, save_state, params):
        super().__init__(app)
        self.save_state = save_state
        self.event_name = "1_start"
        self.night_num = params["night_num"]
        self.timer = 0
        self.animation_sprite = {
            "type": "animation",
            "update_in": 0.05,
            "frames_num": 12,
            "mode": "hold",
            "data": {
                "curr_frame": 0,
                "last_update": time.time()
            }
        }
        self.curr_frame_data = {
            "room": "newspaper",
            "sprites": {
                "newspaper": {
                    "type": "static"
                },
                "text": {
                    "type": "generated",
                    "data": {
                        "text": "Grand Re-opening !!!/n /nVintage pizzeria/ngiven new life !/n /nCome be a part of the/nnew face of freddy/nfazbears's pizza !/n /nwhat could go wrong ?/n /n$100.50 a week !/nTo apply call:/n1-555-faz-fazbear"
                    }
                }
            }
        }

        super().on_enter()

    def on_enter(self):
        pass

    def handle_input(self, input):
        pass

    def extra_update(self):
        self.timer = self.timer + 1
        if self.timer >= 300 and "newspaper_uit" not in self.curr_frame_data["sprites"]:
            self.curr_frame_data["sprites"]["newspaper_uit"] = self.animation_sprite
        if self.timer >= 325:
            all_completed_events = self.save_state.data["completed_events"]
            all_completed_events.append(self.event_name)
            update_config_value("save.json", "completed_events", all_completed_events)

            self.app.set_scene("game", {"night_num": self.night_num})