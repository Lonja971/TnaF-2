from utils.save import load_config, update_config_value
from config.night_events import NIGHT_EVENTS

def new_game(app, update_save):
    NEW_NIGHT = 1
    update_config_value("save.json", "curr_night", NEW_NIGHT)
    update_config_value("save.json", "completed_events", [])
    update_save()
    app.set_scene("nightmare", {"night_num": 0})

def check_night_start_events(app, night_number, save_state):
    if (night_number not in NIGHT_EVENTS) or ("start" not in NIGHT_EVENTS[night_number]):
        app.set_scene("game", {"night_num": night_number})
    else:
        if ("completed_events" in save_state.data) and (f"{night_number}_start" in save_state.data["completed_events"]):
            app.set_scene("game", {"night_num": night_number})
        else:
            app.set_scene(NIGHT_EVENTS[night_number]["start"], {"night_num": night_number})

def check_night_end_events(app, night_number, save_state):
    save_state.update()
    if (night_number not in NIGHT_EVENTS) or ("end" not in NIGHT_EVENTS[night_number]):
            app.set_scene("menu")
    else:
        if ("completed_events" in save_state.data) and (f"{night_number}_end" in save_state.data["completed_events"]):
            app.set_scene("menu")
        else:
            app.set_scene(NIGHT_EVENTS[night_number]["end"], {"night_num": night_number})