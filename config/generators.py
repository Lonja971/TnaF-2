from engine.generator_fx import (
    generate_dot_background,
    generate_main_menu_options,
    generate_black_background,
    none_bg,
    generate_game_buttery,
    game_timeblock,
    game_nightnumber,
    generate_camera_map,
    generate_camera_music_box_power,
    generate_ascii_text,
    generate_stars,
    generate_custom_options_grid,
    generate_custom_options_ready
)

GENERATORS = {
    "None": none_bg,
    "background_dots": generate_dot_background,
    "background_black": generate_black_background,
    "main_menu_options": generate_main_menu_options,
    "game_buttery": generate_game_buttery,
    "game_timeblock": game_timeblock,
    "game_nightnumber": game_nightnumber,
    "camera_map": generate_camera_map,
    "music_box_power": generate_camera_music_box_power,
    "ascii_text": generate_ascii_text,
    "stars": generate_stars,
    "custom_options_grid": generate_custom_options_grid,
    "custom_options_ready": generate_custom_options_ready
}