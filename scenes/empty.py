from engine.scene import Scene

class EmptyScene(Scene):
    def draw(self, stdscr):
        stdscr.clear()
        stdscr.addstr(1, 1, "Empty")

    def handle_input(self, key):
        if key == 27:  # ESC
            self.app.set_scene("menu")
