import curses
from scenes.main_menu import MainMenu
from scenes.events.newspaper import Newspaper
from scenes.events.nightmare import Nightmare
from scenes.events.pay5 import PayCheck5
from scenes.events.pay6 import PayCheck6
from scenes.events.pay7 import PayCheck7
from scenes.custom_options import CustomOptions
from scenes.game import GameScene
from scenes.settings import SettingsScene
from utils.log import debug_log
from engine.input_manager import InputManager
from engine.save_state import SaveState
import time

class ScenesManager:
    def __init__(self, win):
        self.win = win
        self.save_state = SaveState()
        self.scenes = {
            "menu": MainMenu,
            "game": GameScene,
            "settings": SettingsScene,
            "newspaper": Newspaper,
            "nightmare": Nightmare,
            "pay5": PayCheck5,
            "pay7": PayCheck7,
            "pay6": PayCheck6,
            "custom_options": CustomOptions
        }
        self.current_scene = None

    def set_scene(self, name, params={}):
        if self.current_scene:
            self.current_scene.on_exit()

        self.current_scene = self.scenes[name](self, self.save_state, params)
        self.current_scene.on_enter()

    def run(self):
        self.win.nodelay(True)
        curses.curs_set(0)

        self.input = InputManager()
        self.input.start()

        while True:
            self.current_scene.update()
            self.current_scene.handle_input(self.input)
            self.input.end_frame()

            if self.current_scene.has_frame_changed():
                self.current_scene.render(self.win)
                self.win.refresh()

            time.sleep(0.0005)
            curses.napms(16)
