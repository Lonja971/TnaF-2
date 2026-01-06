from utils.log import debug_log

class ButterySystem:
    CENTER_LIGHT = 0.15
    SIDE_LIGTH = 0.1

    def __init__(self):
        self._accum = 0.0

    def update(self, state, dt: float):
        drain = 0
        if state.light == "center":
            drain += self.CENTER_LIGHT
        elif state.light == "left" or state.light == "right":
            drain += self.SIDE_LIGTH

        state.buttery -= drain

        if state.buttery < 0:
            state.buttery = 0
            state.light = None
