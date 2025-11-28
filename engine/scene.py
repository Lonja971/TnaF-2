from utils.log import debug_log
import copy

class Scene:
    def __init__(self, app):
        self.app = app
        self.force_redraw = True
        self.prev_frame_data = None
        self.curr_frame_data = None

    def on_enter(self):
        self.force_redraw = True
        if self.curr_frame_data is not None:
            self.prev_frame_data = self.curr_frame_data.copy()

    def on_exit(self):
        pass

    def handle_input(self, key):
        pass

    def update(self):
        pass

    def update_frame(self):
        self.prev_frame_data = self.curr_frame_data

    def has_frame_changed(self):
        if self.force_redraw:
            self.force_redraw = False
            self.prev_frame_data = None
            return True

        if self.prev_frame_data != self.curr_frame_data:
            self.prev_frame_data = copy.deepcopy(self.curr_frame_data)
            return True

        return False

    def draw(self, stdscr):
        pass