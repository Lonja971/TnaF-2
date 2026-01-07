from utils.log import debug_log

class GameState:
    def __init__(self):
        self.hour = 12
        self.buttery = 100
        self.time = [12, 0]
        self.miliseconds = 0

        self.office_pos = "l"
        self.is_camera_open = False
        self.is_camera_light = False
        self.is_tablet_opening_anim = False
        self.tablet_anim_dir = "open"
        self.active_camera_num = 9
        self.cameras = {
            1: "First",
            2: "Second",
            3: "d",
            4: "d",
            5: "d",
            6: "d",
            7: "d",
            8: "d",
            9: "d",
            10: "d",
            11: "d",
            12: "d",
        }

        self.is_mask = False
        self.is_removing_mask = False
        self.light = None

        self.visible_sprites = {}

    def build_render_data(self):
        return {
            "sprites": self.visible_sprites,
            "full_reset": False
        }
    
    def set_office_pos(self, pos):
        if self.is_tablet_opening_anim: return
        if self.is_camera_open: return
        
        self.office_pos = pos.lower()

    def set_light(self, side, is_on=True):
        if self.buttery <= 0: return
        if self.is_mask: return

        if self.light != side and is_on:
            self.light = side
            return
        
        if self.light == side and not is_on:
            self.light = None

    def set_mask(self):
        if self.is_removing_mask: return
        if self.is_camera_open or self.is_tablet_opening_anim: return

        self.is_mask = not self.is_mask
        if self.is_mask and self.light:
            self.light = None

    def set_camera(self):
        if self.is_mask or self.is_removing_mask: return

        self.is_camera_open = not self.is_camera_open

        if not self.is_camera_open and self.is_camera_light:
            self.is_camera_light = False

        if self.is_camera_open and self.light:
            self.light = None

    def start_opening_tablet(self):
        if self.is_mask or self.is_removing_mask: return

        self.is_tablet_opening_anim = not self.is_tablet_opening_anim
        if self.is_camera_open:
            self.tablet_anim_dir = "close"
        else:
            self.tablet_anim_dir = "open"

        if self.is_tablet_opening_anim and self.light:
            self.light = None

        if self.is_camera_open:
            self.is_camera_open = False

    def set_camera_light(self, is_on=True):
        if self.buttery <= 0: return

        if self.is_camera_open or self.is_tablet_opening_anim:
            self.is_camera_light = is_on

    def change_active_camera(self, cam="next"):
        if not self.is_camera_open: return

        if cam == "prev":
            if self.active_camera_num - 1 >= 1:
                self.active_camera_num -= 1
            else:
                self.active_camera_num = 12
        elif cam == "next":
            if self.active_camera_num + 1 <= 12:
                self.active_camera_num += 1
            else:
                self.active_camera_num = 1
            
        elif isinstance(cam, int):
            pass
