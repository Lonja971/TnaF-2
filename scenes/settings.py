from engine.scene import Scene

class SettingsScene(Scene):
    def draw(self, stdscr):
        stdscr.clear()
        stdscr.addstr(1, 1, "Тут будуть налаштування")
        stdscr.addstr(3, 1, "Натисніть Backspace щоб повернутися в меню")

    def handle_input(self, key):
        if key == 8:
            self.app.set_scene("menu")
