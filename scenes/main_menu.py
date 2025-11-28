import curses, time
from engine.scene import Scene
from utils.sprite_loader import load_sprite
from utils.log import debug_log

class MainMenu(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.options = [
            {
                "title": "Почати гру",
                "action": lambda: self.app.set_scene("game")
            },
            {
                "title": "Налаштування",
                "action": lambda: self.app.set_scene("settings")
            },
            {
                "title": "Вийти",
                "action": lambda: exit()
            },
        ]
        self.curr_frame_data = {
            "selected_option": 0,
            "background": {
                "frame_nr": 0,
                "last_update": 0,
                "update_in": 1
            }
        }
        self.options_padding = {"w": 5, "h":2}

        super().on_enter()

    def update(self):
        self.update_background()

    def update_background(self):
        now = time.time()
        if now - self.curr_frame_data["background"]["last_update"] >= self.curr_frame_data["background"]["update_in"]:
            self.curr_frame_data["background"]["frame_nr"] += 1
            self.curr_frame_data["background"]["last_update"] = now

    def handle_input(self, key):
        selected_option = self.curr_frame_data["selected_option"]

        if key == curses.KEY_UP:
            if (selected_option - 1) >= 0:
                selected_option -= 1
        elif key == curses.KEY_DOWN:
            if (selected_option + 1) < len(self.options):
                selected_option += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            option = self.options[selected_option]
            option["action"]()
        elif key == 27:
            exit()

        self.curr_frame_data["selected_option"] = selected_option

    def draw(self, win):
        win.clear()
        h, w = win.getmaxyx()

        self.draw_background(win, h, w)
        self.draw_options(win, h, w)

    def draw_background(self, win, h, w):
        if self.curr_frame_data["background"]["frame_nr"] > 3:
            self.curr_frame_data["background"]["frame_nr"] = 0

        sprite = load_sprite(f"test{self.curr_frame_data["background"]["frame_nr"]}")
        sprite_h = len(sprite)
        sprite_w = max(len(line) for line in sprite)

        start_y = h - sprite_h
        start_x = w - sprite_w

        for i, line in enumerate(sprite):
            try:
                win.addstr(start_y + i, start_x, line[:w-start_x])
            except curses.error:
                pass


    def draw_options(self, win, h, w):
        symb_h = 1
        max_h = h - (len(self.options) * symb_h) - self.options_padding["h"] - 1

        for i, opt in enumerate(self.options):
            y = max_h + symb_h + i

            if i == self.curr_frame_data["selected_option"]:
                win.attron(curses.A_REVERSE)

            win.addstr(y, self.options_padding["w"], opt["title"])

            if i == self.curr_frame_data["selected_option"]:
                win.attroff(curses.A_REVERSE)