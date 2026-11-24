import curses, sys
from engine.scenes_manager import  ScenesManager
from utils.print_border import print_border
from utils.config_manager import ensure_config
from utils.save import load_config
from utils.paths import SAVE_DIR

def main(stdscr):
    ensure_config("settings.json")
    ensure_config("save.json")

    config = load_config("settings.json")
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, 233)

    check_ter_size(stdscr, config)

    main_win = curses.newwin(config["terminal_min_height"], config["terminal_min_width"], 0, 0)
    main_win.bkgd(' ', curses.color_pair(1))
    main_win.keypad(True)

    scenes_manager = ScenesManager(main_win)

    if "first_nightmare" not in scenes_manager.save_state.data["completed_events"]:
        scenes_manager.set_scene("nightmare", {"night_num": 0})
    else:
        scenes_manager.set_scene("menu")

    scenes_manager.run()

def check_ter_size(stdscr, config):
    h, w = stdscr.getmaxyx()
    if w < config["terminal_min_width"] or h < config["terminal_min_height"]:
        curses.endwin()
        print_border()
        print("\nThe window is too small!\nCan you see the image at the top? Click on the '-' sign until the image is the right size")
        sys.exit()

curses.wrapper(main)