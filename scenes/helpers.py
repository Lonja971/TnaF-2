from utils.save import load_config, update_config_value
from config.night_events import NIGHT_EVENTS

def new_game(app, update_save):
    NEW_NIGHT = 1
    update_config_value("save.json", "curr_night", NEW_NIGHT)
    update_save()
    app.set_scene("game", {"night_num": NEW_NIGHT})

def check_night_start_events(app, night_number, save_state):
    if (night_number not in NIGHT_EVENTS) or ("start" not in NIGHT_EVENTS[1]): return

    if ("completed_events" in save_state) and (f"{night_number}_start" in save_state["completed_events"]):
        app.set_scene("game", {"night_num": night_number})
    else:
        app.set_scene(NIGHT_EVENTS[night_number]["start"], {"night_num": night_number})