from config.rooms import ROOMS
from config.sprite_registry import SPRITES
from utils.log import debug_log
import time

class GameSceneFrames:
    def __init__(self, state, night):
        self.state = state
        self.night = night
        self.last_scene = None

    def office_frames(self, curr_scene_frames, anim_state):
        fan_name = ROOMS[f"game_office_{"l" if self.state.office_pos == "l" else "r"}"]["sprites"]["office_fan_anima"]["name"]
        mask_name_on = "mask_anima_on"
        mask_name_off = "mask_anima_off"

        frames = {
            "room": "game_office_l" if self.state.office_pos == "l" else "game_office_r",
            "sprites": {
                "game_buttery": {
                    "type": "generated",
                    "data": {
                        "value": self.state.get_buttery_level()
                    }
                },
                "game_timeblock": {
                    "type": "generated",
                    "data": {
                        "time": self.state.time.time.copy()
                    }
                },
                "game_nightnumber": {
                    "type": "generated",
                    "data": {
                        "number": self.night
                    }
                },
                "office_fan_anima": {
                    "type": "animation",
                    "update_in": SPRITES[fan_name]["update_in"],
                    "frames_num": len(SPRITES[fan_name]["frames"]),
                    "mode": SPRITES[fan_name]["mode"],
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
                    "last_update": anim_state.get("game_mask_off", {}).get("last_update", time.time())
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
                        "last_update": anim_state.get("game_mask_on", {}).get("last_update", time.time()),
                    }
                }

        if self.state.is_tablet_opening_anim:
            if self.state.tablet_anim_dir == "open":
                frames["sprites"]["game_tablet_on"] = {
                    "type": "animation",
                    "update_in": SPRITES["tablet_anima_on"]["update_in"],
                    "frames_num": len(SPRITES["tablet_anima_on"]["frames"]),
                    "mode": SPRITES["tablet_anima_on"]["mode"],
                    "data": {
                        "curr_frame": anim_state.get("curr_frame", {}).get("curr_frame", 0),
                        "last_update": anim_state.get("last_update", {}).get("last_update", time.time())
                    }
                }
            else:
                frames["sprites"]["game_tablet_off"] = {
                    "type": "animation",
                    "update_in": SPRITES["tablet_anima_off"]["update_in"],
                    "frames_num": len(SPRITES["tablet_anima_off"]["frames"]),
                    "mode": SPRITES["tablet_anima_off"]["mode"],
                    "data": {
                        "curr_frame": anim_state.get("curr_frame", {}).get("curr_frame", 0),
                        "last_update": anim_state.get("last_update", {}).get("last_update", time.time())
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

        if self.state.office_pos == "l":
            if self.state.light == "left" and "left_light" not in curr_sprites_frames:
                frames_data["update"]["left_light"] = {
                    "type": "static"
                }
            elif self.state.light != "left" and "left_light" in curr_sprites_frames:
                frames_data["delete"].append("left_light")

        if self.state.office_pos == "r":
            if self.state.light == "right" and "right_light" not in curr_sprites_frames:
                frames_data["update"]["right_light"] = {
                    "type": "static"
                }
            elif self.state.light != "right" and "right_light" in curr_sprites_frames:
                frames_data["delete"].append("right_light")

        if curr_sprites_frames["game_buttery"]["data"]["value"] != int(self.state.get_buttery_level()):
            frames_data["update"]["game_buttery"] = {
                "type": "generated",
                    "data": {
                        "value": int(self.state.get_buttery_level())
                    }
            }

        if curr_sprites_frames["game_timeblock"]["data"]["time"] != self.state.time:
            frames_data["update"]["game_timeblock"] = {
                "type": "generated",
                    "data": {
                        "time": self.state.time.time.copy()
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

        if "game_mask_off" in curr_sprites_frames and curr_sprites_frames["game_mask_off"]["data"]["curr_frame"] == curr_sprites_frames["game_mask_off"]["frames_num"] - 1:
            frames_data["delete"].append("game_mask_off")
            self.state.is_removing_mask = False

        if self.state.is_tablet_opening_anim and self.state.tablet_anim_dir == "open" and "game_tablet_on" not in curr_sprites_frames:
            frames_data["update"]["game_tablet_on"] = {
                "type": "animation",
                "update_in": SPRITES["tablet_anima_on"]["update_in"],
                "frames_num": len(SPRITES["tablet_anima_on"]["frames"]),
                "mode": SPRITES["tablet_anima_on"]["mode"],
                "data": {
                    "curr_frame": 0,
                    "last_update": time.time()
                }
            }

        if self.state.is_tablet_opening_anim and self.state.tablet_anim_dir == "close" and "game_tablet_off" not in curr_sprites_frames:
            frames_data["update"]["game_tablet_off"] = {
                "type": "animation",
                "update_in": SPRITES["tablet_anima_off"]["update_in"],
                "frames_num": len(SPRITES["tablet_anima_off"]["frames"]),
                "mode": SPRITES["tablet_anima_off"]["mode"],
                "data": {
                    "curr_frame": 0,
                    "last_update": time.time()
                }
            }

        if "game_tablet_on" in curr_sprites_frames and curr_sprites_frames["game_tablet_on"]["data"]["curr_frame"] == curr_sprites_frames["game_tablet_on"]["frames_num"] - 1:
            self.state.set_camera()

        if "game_tablet_off" in curr_sprites_frames and curr_sprites_frames["game_tablet_off"]["data"]["curr_frame"] == curr_sprites_frames["game_tablet_off"]["frames_num"] - 1:
            self.state.is_tablet_opening_anim = False
            frames_data["delete"].append("game_tablet_off")

        return frames_data
    
    def camera_frames(self, curr_scene_frames):
        active_cam_name = f"cam_{self.state.active_camera_num}"

        frames = {
            "room": "camera",
            "sprites": {
                "game_buttery": {
                    "type": "generated",
                    "data": {
                        "value": self.state.get_buttery_level()
                    }
                },
                "game_timeblock": {
                    "type": "generated",
                    "data": {
                        "time": self.state.time.time.copy()
                    }
                },
                "game_nightnumber": {
                    "type": "generated",
                    "data": {
                        "number": self.night
                    }
                },
                "camera_map": {
                    "type": "generated",
                    "data": {
                        "active_cam": self.state.active_camera_num
                    }
                }
            }
        }

        if self.state.active_camera_num == 11:
            frames["music_box_power"] = {
                "type": "generated",
                "data": {
                    "power": int(self.state.music_box.power)
                }
            }

        if active_cam_name not in ROOMS[curr_scene_frames["room"]]["sprites"]:
            frames["camera_not_found"] = {
                "type": "animation",
                "update_in": SPRITES["camera_not_found"]["update_in"],
                "frames_num": len(SPRITES["camera_not_found"]["frames"]),
                "mode": SPRITES["camera_not_found"]["mode"],
                "data": {
                    "curr_frame": 0,
                    "last_update": time.time()
                }
            }
        else:
            if self.state.is_camera_light:
                if f"{active_cam_name}_l" not in ROOMS[curr_scene_frames["room"]]["sprites"]:
                    frames["camera_not_found"] = {
                        "type": "animation",
                        "update_in": SPRITES["camera_not_found"]["update_in"],
                        "frames_num": len(SPRITES["camera_not_found"]["frames"]),
                        "mode": SPRITES["camera_not_found"]["mode"],
                        "data": {
                            "curr_frame": 0,
                            "last_update": time.time()
                        }
                    }
                else:
                    frames[f"{active_cam_name}_l"] = {
                        "type": "static"
                    }
            else:
                frames[active_cam_name] = {
                    "type": "static"
                }


        self.state.is_tablet_opening_anim = False

        return frames
    
    def update_camera_frames(self, curr_scene_frames):
        active_cam_name = f"cam_{self.state.active_camera_num}"
        allowed = {active_cam_name, f"{active_cam_name}_l"}
        curr_sprites_frames = curr_scene_frames["sprites"]
        frames_data = {
            "update": {},
            "delete": []
        }

        if self.state.active_camera_num == 11:
            if "music_box_power" not in curr_sprites_frames:
                frames_data["update"]["music_box_power"] = {
                    "type": "generated",
                    "data": {
                        "power": int(self.state.music_box.power)
                    }
                }
            elif curr_sprites_frames["music_box_power"]["data"]["power"] != int(self.state.music_box.power):
                frames_data["update"]["music_box_power"] = {
                    "type": "generated",
                    "data": {
                        "power": int(self.state.music_box.power)
                    }
                }
        else:
            if "music_box_power" in curr_sprites_frames:
                frames_data["delete"].append("music_box_power")

        if curr_sprites_frames["camera_map"]["data"]["active_cam"] != self.state.active_camera_num:
            frames_data["update"]["camera_map"] = {
                "type": "generated",
                    "data": {
                        "active_cam": self.state.active_camera_num
                    }
            }

        if curr_sprites_frames["game_buttery"]["data"]["value"] != int(self.state.get_buttery_level()):
            frames_data["update"]["game_buttery"] = {
                "type": "generated",
                    "data": {
                        "value": int(self.state.get_buttery_level())
                    }
            }

        if curr_sprites_frames["game_timeblock"]["data"]["time"] != self.state.time:
            frames_data["update"]["game_timeblock"] = {
                "type": "generated",
                    "data": {
                        "time": self.state.time.time.copy()
                    }
            }

        if active_cam_name not in ROOMS[curr_scene_frames["room"]]["sprites"]:
            for sprite_name in list(curr_sprites_frames.keys()):
                if sprite_name.startswith("cam_"):
                    frames_data["delete"].append(sprite_name)
            frames_data["update"]["camera_not_found"] = {
                "type": "animation",
                "update_in": SPRITES["camera_not_found"]["update_in"],
                "frames_num": len(SPRITES["camera_not_found"]["frames"]),
                "mode": SPRITES["camera_not_found"]["mode"],
                "data": {
                    "curr_frame": 0,
                    "last_update": time.time()
                }
            }
        else:
            if "camera_not_found" in curr_sprites_frames:
                frames_data["delete"].append("camera_not_found")

            for sprite_name in curr_sprites_frames:
                if sprite_name.startswith("cam_") and sprite_name not in allowed:
                    frames_data["delete"].append(sprite_name)

            if self.state.is_camera_light and f"{active_cam_name}_l" not in curr_sprites_frames:
                if active_cam_name in curr_sprites_frames:
                    frames_data["delete"].append(active_cam_name)

                if f"{active_cam_name}_l" not in ROOMS[curr_scene_frames["room"]]["sprites"]:
                    frames_data["update"]["camera_not_found"] = {
                        "type": "animation",
                        "update_in": SPRITES["camera_not_found"]["update_in"],
                        "frames_num": len(SPRITES["camera_not_found"]["frames"]),
                        "mode": SPRITES["camera_not_found"]["mode"],
                        "data": {
                            "curr_frame": 0,
                            "last_update": time.time()
                        }
                    }
                else:
                    frames_data["update"][f"{active_cam_name}_l"] = {
                        "type": "static"
                    }

            if not self.state.is_camera_light and active_cam_name not in curr_sprites_frames:
                if f"{active_cam_name}_l" in curr_sprites_frames:
                    frames_data["delete"].append(f"{active_cam_name}_l")

                frames_data["update"][active_cam_name] = {
                    "type": "static"
                }

            for name, anim_class in self.state.animatronics.items():
                if anim_class.pos == self.state.active_camera_num:
                    frames_data["update"][f"{active_cam_name}_{name}{"_l" if self.state.is_camera_light else ""}"] = {
                        "type": "static"
                    }
                else:
                    if f"{active_cam_name}_{name}{"_l" if self.state.is_camera_light else ""}" in curr_sprites_frames:
                        frames_data["delete"].append(f"{active_cam_name}_{name}{"_l" if self.state.is_camera_light else ""}")

        return frames_data

    def process_scene_frames(self, curr_scene_frames, anim_state):
        if self.last_scene == None: self.last_scene = curr_scene_frames["room"]

        frames_data = {
            "rewrite": False,
            "update": {},
            "delete": []
        }

        if self.state.is_camera_open == False:
            if self.last_scene != f"game_office_{self.state.office_pos}":
                frames_data["rewrite"] = True
                frames_data["update"] = self.office_frames(curr_scene_frames, anim_state)

            else:
                updated_frames = self.update_office_frames(curr_scene_frames, anim_state)
                frames_data["update"] = updated_frames["update"]
                frames_data["delete"] = updated_frames["delete"]

            self.last_scene = "game_office_l" if self.state.office_pos == "l" else "game_office_r"
        else:
            if self.last_scene != "camera":
                frames_data["rewrite"] = True
                frames_data["update"] = self.camera_frames(curr_scene_frames)
            else:
                updated_frames = self.update_camera_frames(curr_scene_frames)
                frames_data["update"] = updated_frames["update"]
                frames_data["delete"] = updated_frames["delete"]

            self.last_scene = "camera"

        return frames_data