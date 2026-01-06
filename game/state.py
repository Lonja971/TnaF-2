from utils.log import debug_log

class GameState:
    def __init__(self):
        self.hour = 12
        self.buttery = 100
        self.time = [12, 0]
        self.miliseconds = 0

        self.office_pos = "l"
        self.camera = None
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
        debug_log(self.is_removing_mask)
        if self.is_removing_mask: return
        debug_log("Тут")

        self.is_mask = not self.is_mask
        if self.is_mask and self.light:
            self.light = None