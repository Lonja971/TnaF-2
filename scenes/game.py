from engine.scene import Scene
from utils.log import debug_log
from game.game import Game
import time
from pynput import keyboard
from scenes.helpers import check_night_end_events
from config.sprite_registry import SPRITES

CAMERA_KEYBINDS = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "0": 10,
    "-": 11,
    "=": 12,
}

class GameScene(Scene):
    def __init__(self, app, save_state, params, anim_intelligence = None):
        super().__init__(app)
        debug_log(params)
        self.game = Game(
            params["night_num"],
            params.get("anim", anim_intelligence)
        )
        self.save_state = save_state
        self.tick_rate = 0.10
        self._last_tick = time.time()
        self.paused = False
        self.light_pushed = False
        self.is_preview_ended = False
        self.preview_time = 0
        self.start_frames = {
            "room": "game_office_l",
            "sprites": {
                "game_buttery": {
                    "type": "generated",
                    "data": {
                        "value": self.game.state.get_buttery_level()
                    }
                },
                "game_timeblock": {
                    "type": "generated",
                    "data": {
                        "time": self.game.state.time.time.copy()
                    }
                },
                "game_nightnumber": {
                    "type": "generated",
                    "data": {
                        "number": self.game.night
                    }
                },
                "office_fan_anima": {
                    "type": "animation",
                    "update_in": SPRITES["office_fan_anima"]["update_in"],
                    "frames_num": 4,
                    "mode": "loop",
                    "data": {
                        "curr_frame": 0,
                        "last_update": time.time()
                    }
                },
            }
        }
        self.curr_frame_data = {
            "room": "game_start_night",
            "sprites": {
                "glitch": {
                    "type": "animation",
                    "update_in": SPRITES["glitch_white"]["update_in"],
                    "frames_num": 6,
                    "mode": "hold",
                    "data": {
                        "curr_frame": 0,
                        "last_update": time.time()
                    }
                },
                "time": {
                    "type": "generated",
                    "data": {
                        "text": "12:00 AM"
                    }
                },
                "night": {
                    "type": "generated",
                    "data": {
                        "text": f"{params["night_num"]} st Night"
                    }
                },
            }
        }

    def extra_update(self):
        if not self.is_preview_ended:
            self.preview_time = self.preview_time + 1
            if self.preview_time == 87:
                self.curr_frame_data["sprites"]["glitch"]["data"]["curr_frame"] = 0
            elif self.preview_time >= 100:
                self.is_preview_ended = True
                self.curr_frame_data = self.start_frames

            return
        
        now = time.time()

        if self.paused: return

        if self.game.state.is_6am_anim_finished:
            check_night_end_events(self.app, self.game.night, self.save_state)

        if now - self._last_tick >= self.tick_rate:
            dt = now - self._last_tick
            self._last_tick = now

            self.game.update_states(dt)
            self.process_scene_frames()

    def process_scene_frames(self):
        processed_frames = self.game.update_scene_frames(self.curr_frame_data, self.anim_state)

        if processed_frames["rewrite"] == True:
            self.curr_frame_data = processed_frames["update"]
            return
        
        if processed_frames["delete"]:
            for key in processed_frames["delete"]:
                self.curr_frame_data["sprites"].pop(key, None)

        if processed_frames["update"]:
            for key, sprite in processed_frames["update"].items():
                self.curr_frame_data["sprites"][key] = sprite

    def handle_input(self, input):
        if not self.is_preview_ended: return

        self.game.state.is_winding_music_box = (
            self.game.state.is_camera_open
            and self.game.state.active_camera_num == 11
            and input.is_held(keyboard.KeyCode.from_char('x'))
        )

        if self.game.state.state == "end" and not self.game.state.time.is_end_night():
            if (input.was_pressed(keyboard.Key.enter)
                or input.was_pressed(keyboard.KeyCode.from_char('\n'))
                or input.was_pressed(keyboard.KeyCode.from_char('z'))
                or input.was_pressed(keyboard.KeyCode.from_char('x'))
            ):
                self.app.set_scene("menu")

        if input.is_held(keyboard.Key.esc):
            self.app.set_scene("menu")

        if input.was_pressed(keyboard.Key.left):
            if self.game.state.is_camera_open:
                self.game.state.change_active_camera("prev")
            else:
                self.game.state.set_office_pos("l")

        if input.was_pressed(keyboard.Key.right):
            if self.game.state.is_camera_open:
                self.game.state.change_active_camera()
            else:
                self.game.state.set_office_pos("r")

        # Mask / Camera
        if input.was_pressed(keyboard.Key.down):
            if self.game.state.is_camera_open:
                self.game.state.start_opening_tablet()
            else:
                self.game.state.set_mask()

        if input.was_pressed(keyboard.Key.up):
            if self.game.state.is_mask:
                self.game.state.set_mask()
            else:
                self.game.state.start_opening_tablet()

        # Light
        if input.was_pressed(keyboard.KeyCode.from_char('x')):
            if self.game.state.is_camera_open or self.game.state.is_tablet_opening_anim:
                if self.game.state.active_camera_num == 11:
                    pass
                else:
                    self.game.state.set_camera_light()
            else:
                self.game.state.set_light("centre")

        if input.was_released(keyboard.KeyCode.from_char('x')):
            if self.game.state.is_camera_open:
                self.game.state.set_camera_light(False)
            else:
                self.game.state.set_light("centre", False)

        if input.was_pressed(keyboard.KeyCode.from_char('z')):
            if self.game.state.is_camera_open or self.game.state.is_tablet_opening_anim:
                if self.game.state.active_camera_num == 11:
                    pass
            else:
                self.game.state.set_light("left")

        if input.was_released(keyboard.KeyCode.from_char('z')):
            self.game.state.set_light("left", False)

        if input.was_pressed(keyboard.KeyCode.from_char('c')):
            self.game.state.set_light("right")

        if input.was_released(keyboard.KeyCode.from_char('c')):
            self.game.state.set_light("right", False)

        if self.game.state.is_camera_open:
            for key_char, cam_num in CAMERA_KEYBINDS.items():
                if input.was_pressed(keyboard.KeyCode.from_char(key_char)):
                    self.game.state.change_active_camera(cam_num)
                    break
