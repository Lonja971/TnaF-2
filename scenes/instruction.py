import time

from engine.scene import Scene
from pynput import keyboard

class Instruction(Scene):
    def __init__(self, app, save_state, params):
        super().__init__(app)
        self.curr_frame_data = {
            "room": "instruction",
            "sprites": {
                "return": {
                    "type": "generated",
                    "data": {
                        "text": "'c' or 'esc' to return"
                    }
                },
                "inst": {
                    "type": "generated",
                    "data": {
                        "text":
"""
                                                                                           open  tablet
for  light  use:                               turn  left                      ↑                      turn  right
z  /  x  /  c                                                      <                                                   >
                                                                                                     ↓                 
load  the  music  box:                                                put  on  a  mask
x
"""
                    }
                }
            }
        }

        super().on_enter()

    def on_enter(self):
        pass

    def handle_input(self, input):
        if input.was_pressed(keyboard.Key.esc) or input.was_pressed(keyboard.KeyCode.from_char('c')):
            self.app.set_scene("menu")
            return

        if input.was_pressed(keyboard.Key.left):
            column = max(0, column - 1)
        elif input.was_pressed(keyboard.Key.right):
            column = min(len(self.matrix[row]) - 1, column + 1)
        elif input.was_pressed(keyboard.Key.up):
            row = max(0, row - 1)
            column = min(column, len(self.matrix[row]) - 1)
        elif input.was_pressed(keyboard.Key.down):
            row = min(len(self.matrix) - 1, row + 1)
            column = min(column, len(self.matrix[row]) - 1)

    def extra_update(self):
        pass