from utils.log import debug_log

class ButterySystem:
    def __init__(self):
        self.power = 100
        self.CENTER_LIGHT = 0.15
        self.SIDE_LIGTH = 0.1
        self.CAMERA_LIGTH = 0.15

    def update(self, state, dt: float):
        drain = 0
        if state.light == "center":
            drain += self.CENTER_LIGHT
        elif state.light == "left" or state.light == "right":
            drain += self.SIDE_LIGTH
        
        if state.is_camera_light:
            drain += self.CAMERA_LIGTH

        self.power -= drain

        if self.power < 0:
            self.power = 0
            state.light = None
            state.is_camera_light = False
