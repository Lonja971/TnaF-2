from .state import GameState
from .scene_frames import GameSceneFrames
from utils.log import debug_log

class Game:
    def __init__(self, night_num):
        self.night = night_num
        self.state = GameState(night_num)
        self.scene_frames = GameSceneFrames(self.state, self.night)

    def update_states(self, dt):
        for name, anim_class in self.state.animatronics.items():
            if anim_class.intelligence > 0:
                anim_class.update()

        self.state.buttery.update(self.state, dt)
        self.state.music_box.update(self.state)
        self.state.time.update(self.state)

    def update_scene_frames(self, curr_scene_frames, anim_state):
        processed_frames = self.scene_frames.process_scene_frames(curr_scene_frames, anim_state)

        return processed_frames