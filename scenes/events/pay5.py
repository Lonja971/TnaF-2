from engine.scene import Scene
from utils.save import update_config_value
import time

class PayCheck5(Scene):
    def __init__(self, app, save_state, params):
        super().__init__(app)
        self.save_state = save_state
        self.event_name = "5_end"
        self.night_num = params["night_num"]
        self.timer = 0
        self.animation_sprite = {
            "type": "animation",
            "update_in": 0.02,
            "frames_num": 11,
            "mode": "hold",
            "data": {
                "curr_frame": 0,
                "last_update": time.time()
            }
        }
        self.curr_frame_data = {
            "room": "paycheck5",
            "sprites": {
                "paycheck5": {
                    "type": "static"
                },
                "text": {
                    "type": "generated",
                    "data": {
                        "text": "Jeremy Fittgerald - $ 100.50"
                    }
                },
                "theend": {
                    "type": "generated",
                    "data": {
                        "text": "the end"
                    }
                },
            }
        }

        super().on_enter()

    def on_enter(self):
        pass

    def handle_input(self, input):
        pass

    def extra_update(self):
        self.timer = self.timer + 1
        if self.timer >= 300 and "paycheck5_uit" not in self.curr_frame_data["sprites"]:
            self.curr_frame_data["sprites"]["paycheck5_uit"] = self.animation_sprite
        if self.timer >= 325:
            all_completed_events = self.save_state.data["completed_events"]
            all_completed_events.append(self.event_name)
            update_config_value("save.json", "completed_events", all_completed_events)

            self.app.set_scene("menu")