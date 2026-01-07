from utils.log import debug_log

class ButterySystem:
    def __init__(self):
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

        state.buttery -= drain

        if state.buttery < 0:
            state.buttery = 0
            state.light = None
            state.is_camera_light = False
