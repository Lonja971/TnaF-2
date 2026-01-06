import curses, sys
from engine.config_manager import ConfigManager
from engine.scenes_manager import  ScenesManager

def main(stdscr):
    config = ConfigManager()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, 233)

    check_ter_size(stdscr, config)

    main_win = curses.newwin(config.terminal_min_height, config.terminal_min_width, 0, 0)
    main_win.bkgd(' ', curses.color_pair(1))
    main_win.keypad(True)

    scenes_manager = ScenesManager(main_win)

    scenes_manager.set_scene("menu")
    scenes_manager.run()

def check_ter_size(stdscr, config):
    h, w = stdscr.getmaxyx()
    if w < config.terminal_min_width or h < config.terminal_min_height:
        curses.endwin()
        for i in range(config.terminal_min_height):
            if i == 0:
                print("#"*config.terminal_min_width)
            else:
                print("#")

        print("Not enought")
        sys.exit()

curses.wrapper(main)