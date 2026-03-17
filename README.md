# Code Quest – Build a Text-Based Dungeon Crawler in Python

A complete step-by-step YouTube tutorial series that teaches Python programming by building an ever-evolving **text-based RPG / dungeon crawler** from the ground up.

- Beginner-friendly → advanced features
- Real game mechanics: rooms, combat, dice rolls, inventory, equipment slots, save/load, shop system, dual-wield logic, and more
- Clean, well-commented code with progressive difficulty

🎥 **Full playlist on YouTube**: [Code Quest Series]https://youtube.com/playlist?list=PLept9bk6E1qHJ3QAl-kQtDQOomZh-_HS6&si=V0AoqqLevR1SYjYj

Created by **ZeroLvL**  
Current status: Series complete (8 main quests + polish pass)

## Repository Structure

Each folder contains the **exact code state at the end of that video/quest**, so you can jump to any lesson and run it immediately.

code-quest-python-rpg/ ├── README.md ├── quest-01-basics/              # First dice roller & basic structure ├── quest-02-shadow-vault/        # Number-guessing vault puzzle module ├── quest-03-player-inventory/    # Player class + simple inventory ├── quest-04-combat/              # Turn-based combat with dice + crits ├── quest-05-dungeon/             # Rooms, navigation, enemies, treasure ├── quest-06-equipment-basics/    # First equipment bonuses & equip logic ├── quest-07-save-load-shop/      # JSON save/load + merchant with refresh ├── quest-08-expanded-equipment/  # Full gear slots, dual-wield, auto-unequip └── final-game/                   # Polished final version after all quests ├── main.py ├── player.py ├── combat.py ├── world.py ├── room.py ├── inventory.py ├── dice.py └── items.json

## How to Run Any Quest

1. Clone the repository
   ```bash
   git clone https://github.com/YOUR_USERNAME/code-quest-python-rpg.git
   cd code-quest-python-rpg

2.  Go to the quest you want to 
    cd quest-07-save-load-shop

3.  Run 
    python main.py

Requirements
•  Python 3.8+
•  No external packages needed (pure standard library + built-in modules)


Series Progression – What You Learn in Each Quest
    01.  Basics & Dice - Animated dice rolling, user input, ASCII art
    02.  Modular Puzzle - OOP vault class, input validation, attempts limit
    03.  Player & Inventory - Class design, gold, simple item quantities
    04.  Combat System - Dice-based turns, critical hits, loot tables
    05.  Dungeon World - Room connections, navigation, enemies, treasure
    06.  Equipment Intro - Bonuses from items, first equip/unequip logic
    07.  Save/Load + Shop - JSON persistence, timed merchant stock, random gear
    08.  Expanded Gear - 10 slots (main/off hand, armor pieces, accessories), dual-wield rules, auto-unequip flow, improved UI

Final Game Highlights (quest-08 & final-game)
•  10 equipment slots with realistic rules (2H weapons disable off-hand, dual-wield allowed)
•  Percentage-based armor that always lets at least 1 damage through
•  Merchant with rotating stock (refreshes every 10 min)
•  Save/load system preserving inventory, equipment, position & progress
•  Beautiful, readable console UI with dividers and clean formatting
•  Random loot, crits, prophecies, vault puzzles, and more
Contributing & Feedback
Found a bug? Have an idea for a bonus quest?
→ Open an issue or pull request — contributions welcome!
You can also leave feedback directly in the YouTube comments — I read every one.
License
MIT License
Feel free to use, modify, and learn from this code for personal or educational purposes.
Happy adventuring! ⚔️
— Samuel
Lake Elsinore, California
March 2026