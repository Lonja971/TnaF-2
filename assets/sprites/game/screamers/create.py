



name = "puppet"
frame_count = 13

print(f'''"screamer_{name}": {{
        "type": "animation",
        "frames": [''')

for i in range(1, frame_count + 1):
    comma = "," if i < frame_count else ""
    print(f'            "game/screamers/{name}/{i}.txt"{comma}')

print('''        ],
        "update_in": 0.02,
        "mode": "hold",
    },''')