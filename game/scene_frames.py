from config.rooms import ROOMS
from config.sprite_registry import SPRITES
from utils.log import debug_log
import time

class GameSceneFrames:
    def __init__(self, state, night):
        self.state = state
        self.night = night

    def office_frames(self, curr_scene_frames, anim_state):
        vent_name = ROOMS[curr_scene_frames["room"]]["sprites"]["office_vent_anima"]["name"]
        mask_name_on = "mask_anima_on"
        mask_name_off = "mask_anima_off"

        frames = {
            "room": "game_office_l" if self.state.office_pos == "l" else "game_office_r",
            "sprites": {
                "game_buttery": {
                    "type": "generated",
                    "data": {
                        "value": self.state.buttery
                    }
                },
                "game_timeblock": {
                    "type": "generated",
                    "data": {
                        "time": self.state.time.copy()
                    }
                },
                "game_nightnumber": {
                    "type": "generated",
                    "data": {
                        "number": self.night
                    }
                },
                "office_vent_anima": {
                    "type": "animation",
                    "update_in": SPRITES[vent_name]["update_in"],
                    "frames_num": len(SPRITES[vent_name]["frames"]),
                    "mode": SPRITES[vent_name]["mode"],
                    "data": {
                        "curr_frame": 0,
                        "last_update": time.time()
                    }
                }
            }
        }

        if self.state.light != "center":
            frames["sprites"]["center_light"] = {
                "type": "static"
            }

        if self.state.is_removing_mask:
            frames["sprites"]["game_mask_off"] = {
                "type": "animation",
                "update_in": SPRITES[mask_name_off]["update_in"],
                "frames_num": len(SPRITES[mask_name_off]["frames"]),
                "mode": SPRITES[mask_name_off]["mode"],
                "data": {
                    "curr_frame": anim_state.get("game_mask_off", {}).get("curr_frame", 0),
                    "last_update": anim_state.get("game_mask_off", {}).get("last_update", 0)
                }
            }
        else:
            if self.state.is_mask == True:
                frames["sprites"]["game_mask_on"] = {
                    "type": "animation",
                    "update_in": SPRITES[mask_name_on]["update_in"],
                    "frames_num": len(SPRITES[mask_name_on]["frames"]),
                    "mode": SPRITES[mask_name_on]["mode"],
                    "data": {
                        "curr_frame": anim_state.get("game_mask_on", {}).get("curr_frame", 0),
                        "last_update": anim_state.get("game_mask_on", {}).get("last_update", 0),
                    }
                }

        if self.state.office_pos == "l":
            if self.state.light == "left":
                frames["sprites"]["left_light"] = {
                    "type": "static"
                }

        if self.state.office_pos == "r":
            if self.state.light == "right":
                frames["sprites"]["right_light"] = {
                    "type": "static"
                }

        return frames
    
    def update_office_frames(self, curr_scene_frames, anim_state):
        mask_name_on = "mask_anima_on"
        mask_name_off = "mask_anima_off"
        frames_data = {
            "update": {},
            "delete": []
        }
        curr_sprites_frames = curr_scene_frames["sprites"]

        if self.state.light == "center" and "center_light" in curr_sprites_frames:
            frames_data["delete"].append("center_light")

        if not self.state.light == "center" and "center_light" not in curr_sprites_frames:
            frames_data["update"]["center_light"] = {
                "type": "static"
            }

        if curr_sprites_frames["game_buttery"]["data"]["value"] != int(self.state.buttery):
            frames_data["update"]["game_buttery"] = {
                "type": "generated",
                    "data": {
                        "value": int(self.state.buttery)
                    }
            }

        if curr_sprites_frames["game_timeblock"]["data"]["time"] != self.state.time:
            frames_data["update"]["game_timeblock"] = {
                "type": "generated",
                    "data": {
                        "time": self.state.time.copy()
                    }
            }

        if self.state.is_mask and "game_mask_on" not in curr_sprites_frames:
            frames_data["update"]["game_mask_on"] = {
                "type": "animation",
                "update_in": SPRITES[mask_name_on]["update_in"],
                "frames_num": len(SPRITES[mask_name_on]["frames"]),
                "mode": SPRITES[mask_name_on]["mode"],
                "data": {
                    "curr_frame": 0,
                    "last_update": time.time()
                }
            }

        if not self.state.is_mask and "game_mask_on" in curr_sprites_frames:
            frames_data["delete"].append("game_mask_on")
            frames_data["update"]["game_mask_off"] = {
                "type": "animation",
                "update_in": SPRITES[mask_name_off]["update_in"],
                "frames_num": len(SPRITES[mask_name_off]["frames"]),
                "mode": SPRITES[mask_name_off]["mode"],
                "revers": SPRITES[mask_name_off].get("revers", False),
                "data": {
                    "curr_frame": 0,
                    "last_update": time.time()
                }
            }
            self.state.is_removing_mask = True
        debug_log(curr_sprites_frames)
        if "game_mask_off" in curr_sprites_frames and curr_sprites_frames["game_mask_off"]["data"]["curr_frame"] == curr_sprites_frames["game_mask_off"]["frames_num"] - 1:
            frames_data["delete"].append("game_mask_off")
            self.state.is_removing_mask = False

        if self.state.office_pos == "l":
            if self.state.light == "left" and "left_light" not in curr_sprites_frames:
                frames_data["update"]["left_light"] = {
                    "type": "static"
                }

        return frames_data



    def process_scene_frames(self, curr_scene_frames, anim_state):
        frames_data = {
            "rewrite": False,
            "update": {},
            "delete": []
        }

        if self.state.camera == None:
            if curr_scene_frames["room"] != f"game_office_{self.state.office_pos}":
                frames_data["rewrite"] = True
                frames_data["update"] = self.office_frames(curr_scene_frames, anim_state)

            else:
                updated_frames = self.update_office_frames(curr_scene_frames, anim_state)
                frames_data["update"] = updated_frames["update"]
                frames_data["delete"] = updated_frames["delete"]

        return frames_data