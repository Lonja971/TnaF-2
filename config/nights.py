# AI levels and changes follow the original FNaF 2 night schedule.
# The AI value is checked on each movement opportunity (once every five seconds).
NIGHTS = {
    1: {
        "anim": {"puppet": {"intelligence": 1}},
        "ai_changes": {
            1: {"new_bon": 2, "new_bird": 2},
            2: {"new_fred": 2, "new_bon": 3, "new_bird": 2},
        },
    },
    2: {
        "anim": {"puppet": {"intelligence": 5}},
        "ai_changes": {
            1: {
                "new_fred": 2,
                "new_bon": 3,
                "new_bird": 3,
                "mangle": 3,
                "bb": 3,
                "old_foxy": 1,
            },
        },
    },
    3: {
        "anim": {
            "bb": {"intelligence": 1},
            "puppet": {"intelligence": 8},
            "old_bon": {"intelligence": 1},
            "old_bird": {"intelligence": 1},
            "old_foxy": {"intelligence": 2},
        },
        "ai_changes": {
            1: {
                "new_bon": 1,
                "new_bird": 1,
                "bb": 2,
                "old_fred": 2,
                "old_bon": 2,
                "old_bird": 2,
                "old_foxy": 3,
            },
        },
    },
    4: {
        "anim": {
            "mangle": {"intelligence": 5},
            "bb": {"intelligence": 3},
            "puppet": {"intelligence": 9},
            "old_bon": {"intelligence": 1},
            "old_foxy": {"intelligence": 7},
        },
        "ai_changes": {
            2: {
                "new_bon": 1,
                "mangle": 5,
                "bb": 3,
                "puppet": 9,
                "old_fred": 3,
                "old_bon": 4,
                "old_bird": 4,
                "old_foxy": 7,
            },
        },
    },
    5: {
        "anim": {
            "new_fred": {"intelligence": 5},
            "new_bon": {"intelligence": 2},
            "new_bird": {"intelligence": 2},
            "mangle": {"intelligence": 1},
            "bb": {"intelligence": 5},
            "puppet": {"intelligence": 10},
            "old_fred": {"intelligence": 2},
            "old_bon": {"intelligence": 2},
            "old_bird": {"intelligence": 2},
            "old_foxy": {"intelligence": 5},
        },
        "ai_changes": {
            1: {
                "new_fred": 1,
                "mangle": 10,
                "old_fred": 5,
                "old_bon": 5,
                "old_bird": 5,
                "old_foxy": 7,
            },
        },
    },
    6: {
        "anim": {
            "mangle": {"intelligence": 3},
            "bb": {"intelligence": 5},
            "puppet": {"intelligence": 15},
            "old_fred": {"intelligence": 5},
            "old_bon": {"intelligence": 5},
            "old_bird": {"intelligence": 5},
            "old_foxy": {"intelligence": 10},
        },
        "ai_changes": {
            2: {
                "new_fred": 5,
                "new_bon": 5,
                "new_bird": 5,
                "mangle": 10,
                "bb": 9,
                "old_fred": 10,
                "old_bon": 10,
                "old_bird": 10,
                "old_foxy": 15,
            },
        },
    },
    7: {
        "anim": {
            "new_bon": {"intelligence": 20},
            "new_bird": {"intelligence": 20},
            "new_fred": {"intelligence": 20},
            "old_bon": {"intelligence": 20},
            "old_bird": {"intelligence": 20},
            "old_fred": {"intelligence": 20},
            "old_foxy": {"intelligence": 20},
            "mangle": {"intelligence": 20},
            "bb": {"intelligence": 20},
            "puppet": {"intelligence": 20},
        },
    },
}
