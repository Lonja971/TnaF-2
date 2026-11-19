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
        self.curr_frame_data = {
            "room": "newspaper",
            "sprites": {
                "newspaper_in": {
                    "type": "animation",
                    "update_in": 0.5,
                    "frames_num": 4,
                    "mode": "hold",
                    "data": {
                        "curr_frame": 0,
                        "last_update": time.time()
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
        if self.timer >= 50:
            all_completed_events = self.save_state.data["completed_events"]
            all_completed_events.append(self.event_name)
            update_config_value("save.json", "completed_events", all_completed_events)

            self.app.set_scene("game", {"night_num": self.night_num})