# dice.py

import random
import time
import os

DICE_ART = {
    1: (
        "┌─────┐",
        "│     │",
        "│  ●  │",
        "│     │",
        "└─────┘",
    ),
    2: (
        "┌─────┐",
        "│ ●   │",
        "│     │",
        "│   ● │",
        "└─────┘",
    ),
    3: (
        "┌─────┐",
        "│ ●   │",
        "│  ●  │",
        "│   ● │",
        "└─────┘",
    ),
    4: (
        "┌─────┐",
        "│ ● ● │",
        "│     │",
        "│ ● ● │",
        "└─────┘",
    ),
    5: (
        "┌─────┐",
        "│ ● ● │",
        "│  ●  │",
        "│ ● ● │",
        "└─────┘",
    ),
    6: (
        "┌─────┐",
        "│ ● ● │",
        "│ ● ● │",
        "│ ● ● │",
        "└─────┘",
    ),
}

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def animate_roll(sides: int):
    for _ in range(8):
        roll = random.randint(1, min(6, sides))
        clear_screen()
        if roll in DICE_ART:
            print("\n".join(DICE_ART[roll]))
        else:
            print(f"Rolling d{sides}...")
        time.sleep(0.1)

def roll_die(sides: int) -> int:
    animate_roll(sides)
    result = random.randint(1, sides)

    clear_screen()
    print(f"\n🎲 Final Roll: {result}")

    if result in DICE_ART:
        print("\n".join(DICE_ART[result]))

    return result