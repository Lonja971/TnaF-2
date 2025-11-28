from engine.scene import Scene
from utils.log import debug_log
import curses
from utils.sprite_loader import load_sprite

class GameScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.curr_frame_data = {
            "side": "l"
        }

    def draw(self, win):
        sprite = load_sprite(f"office{self.curr_frame_data['side']}")

        for i, line in enumerate(sprite):
            try:
                win.addstr(0 + i, 0, line)
            except curses.error:
                pass

    def handle_input(self, key):
        if key == 27:  # ESC
            self.app.set_scene("menu")
        elif key in [ord('a'), ord('A')]:
            self.curr_frame_data["side"] = "l"
        elif key in [ord('d'), ord('D')]:
            self.curr_frame_data["side"] = "r"