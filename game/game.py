from .state import GameState
from .scene_frames import GameSceneFrames
from utils.log import debug_log

class Game:
    def __init__(self, night_num, anim_intelligence = None):
        self.night = night_num
        self.state = GameState(night_num, anim_intelligence)
        self.scene_frames = GameSceneFrames(self.state, self.night)

    def apply_night_ai_changes(self):
        schedule = self.state.ai_schedule
        if not schedule:
            return

        hour = self.state.time.time[0]
        for change_hour, changes in schedule.items():
            if hour != change_hour or change_hour in self.state.applied_ai_changes:
                continue
            for name, intelligence in changes.items():
                self.state.animatronics[name].set_intelligence(intelligence)
            self.state.applied_ai_changes.add(change_hour)

    def update_states(self, dt):
        if self.state.time.is_end_night():
            if not self.state.is_night_progress_saved:
                self.state.save_completed_night()

            self.state.state = "end"

        if self.state.state == "end": return

        self.apply_night_ai_changes()

        if self.state.state == "screamer_anima":
            return

        if self.state.pending_screamer_name is not None:
            self.state.update_pending_screamer()
            return

        # Apply winding before Puppet checks whether it should keep emerging or retreat.
        self.state.music_box.update(self.state, dt)

        for name, anim_class in self.state.animatronics.items():
            anim_class.update(dt)
            if anim_class.pos == 20:
                self.state.start_screamer(name)
                return

        self.state.buttery.update(self.state, dt)
        self.state.time.update(self.state)

    def update_scene_frames(self, curr_scene_frames, anim_state):
        processed_frames = self.scene_frames.process_scene_frames(curr_scene_frames, anim_state)

        return processed_frames
