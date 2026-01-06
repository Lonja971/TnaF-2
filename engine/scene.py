from utils.log import debug_log
from engine.renderer import Renderer
from engine.sprites_manager import SpritesManager
import copy, time

class Scene:
    def __init__(self, app):
        self.app = app
        self.force_redraw = True
        self.prev_frame_data = None
        self.curr_frame_data = None
        self.anim_state = {}

        win_size = app.win.getmaxyx()
        self.sprites_manager = SpritesManager(win_size, self.curr_frame_data)
        self.renderer = Renderer(app.win)

    def on_enter(self):
        self.force_redraw = True
        if self.curr_frame_data is not None:
            self.prev_frame_data = self.curr_frame_data.copy()

    def on_exit(self):
        pass

    def handle_input(self, key):
        pass

    def update(self):
        now = time.time()

        for name, element in list(self.curr_frame_data["sprites"].items()):
            if element.get("type") != "animation":
                continue

            if name not in self.anim_state:
                self.anim_state[name] = {
                    "curr_frame": element["data"].get("curr_frame", 0),
                    "last_update": time.time()
                }

            element["data"] = self.anim_state[name]
            data = element["data"]

            update_in = element.get("update_in", 1)
            frames_num = element.get("frames_num", 1)
            mode = element.get("mode", "hold")  # "loop", "hold", "remove"
            reverse = element.get("reverse", False)

            curr_frame = data["curr_frame"]
            last_update = data["last_update"]

            if now - last_update >= update_in:
                if reverse:
                    next_frame = curr_frame - 1
                    if next_frame < 0:
                        if mode == "loop":
                            next_frame = frames_num - 1
                        elif mode == "hold":
                            next_frame = 0
                        elif mode == "remove":
                            del self.curr_frame_data["sprites"][name]
                            del self.anim_state[name]
                            continue
                else:
                    next_frame = curr_frame + 1
                    if next_frame >= frames_num:
                        if mode == "loop":
                            next_frame = 0
                        elif mode == "hold":
                            next_frame = frames_num - 1
                        elif mode == "remove":
                            del self.curr_frame_data["sprites"][name]
                            del self.anim_state[name]
                            continue

                data["curr_frame"] = next_frame
                data["last_update"] += update_in

        # очищуємо старі анімації, яких більше немає
        current_sprites = set(self.curr_frame_data["sprites"].keys())
        anim_keys = set(self.anim_state.keys())
        for name in anim_keys - current_sprites:
            del self.anim_state[name]

        self.extra_update()

    def update_background(self):
        pass

    def update_frame(self):
        self.prev_frame_data = self.curr_frame_data

    def has_frame_changed(self):
        if self.force_redraw:
            self.force_redraw = False
            self.prev_frame_data = None
            return True

        if self.prev_frame_data is None:
            self.prev_frame_data = copy.deepcopy(self.curr_frame_data)
            return True

        def extract_render_data(frame_data):
            return {
                "room": frame_data.get("room"),
                "sprites": {
                    name: {
                        "type": s["type"],
                        "data": s.get("data", {})
                    }
                    for name, s in frame_data.get("sprites", {}).items()
                }
            }

        prev_render = extract_render_data(self.prev_frame_data)
        curr_render = extract_render_data(self.curr_frame_data)

        if prev_render != curr_render:
            self.prev_frame_data = copy.deepcopy(self.curr_frame_data)
            return True

        return False

    def render(self, win):
        updated_symbols = self.sprites_manager.get_update(self.curr_frame_data)
        self.renderer.render(updated_symbols)

    def extra_update(self):
        pass