# ⚔️ CodeQuest – Build a Text-Based Dungeon Crawler in Python

**A complete, step-by-step YouTube tutorial series that teaches real Python programming by building a fully functional text-based RPG / dungeon crawler from scratch.**

Perfect for beginners who want to move beyond "print('Hello World')" into **real game mechanics**, clean architecture, and professional coding practices — all while having fun adventuring!

🎥 **Watch the full series on YouTube**  
[→ Code Quest Playlist](https://youtube.com/playlist?list=PLept9bk6E1qHJ3QAl-kQtDQOomZh-_HS6&si=V0AoqqLevR1SYjYj)  
_(Each video corresponds exactly to one quest folder — jump in at any point!)_

---

## ✨ Why CodeQuest?

- **Hands-on progression** — Start with dice rolls → end with a polished save/load shop system, dual-wield equipment, and a living dungeon.
- **Zero dependencies** — Pure Python 3.8+ (standard library only).
- **Snapshot folders** — Every quest folder contains the **exact code state** at the end of that video so you can follow along or experiment instantly.
- **Clean, heavily commented code** with ASCII art, clear UI, and thoughtful design patterns.

---

## 🚀 Quick Start

```bash
git clone https://github.com/zeroleveldev/CodeQuest.git
cd CodeQuest

# Pick any quest and run it
cd quest-07-save-load-shop
python main.py

Requirements

Python 3.8 or higher
No pip install needed!

-----------------------------------------------------------------------------------

📁 Repository Structure
Each folder is a complete, runnable milestone:

CodeQuest/
├── README.md
├── quest-01-dice/          # Basics + animated dice roller
├── quest-02-shadow-vault/  # OOP puzzle module (vault)
├── quest-03-enchanted-inventory/ # Player class + inventory system
├── quest-04-combat/        # Turn-based combat with crits & loot
├── quest-05-the-dungeon/   # World map, rooms, enemies & treasure
├── quest-06-xp-leveling/   # Equipment bonuses & equip logic
├── quest-07-save-load-shop/# JSON saves + dynamic merchant shop
├── quest-08-expanded-inventory/ # 10 gear slots, dual-wield, auto-unequip
├── final-game/             # Fully polished version (all features combined)
│   ├── main.py
│   ├── player.py
│   ├── combat.py
│   ├── world.py
│   ├── room.py
│   ├── inventory.py
│   ├── dice.py
│   └── items.json
└── (most quests contain a clean `src/` layout for easy navigation)

-------------------------------------------------------------------------------------

📋 What You Learn in Each Quest

Quest,Title,Key Skills Mastered
01: Dice & Basics,"Input loops, ASCII art, random, functions"
02: Shadow Vault,"OOP classes, validation, retry limits"
03: Enchanted Inventory,"Classes, dictionaries, gold system"
04: Combat Arena,"Turn-based logic, crits, loot tables"
05: The Dungeon,"Graph-based rooms, navigation, encounters"
06: Equipment Foundations,"Item bonuses, equip/unequip flow"
07: Save/Load + Merchant,"JSON persistence, timers, random stock"
08: Expanded Gear System,"10 slots, dual-wield rules, improved UX"

Final Game Highlights:

- Realistic 10-slot equipment (2H weapons block off-hand, dual-wield supported)
- Armor always allows minimum 1 damage
- Merchant stock refreshes every 10 minutes
- Full save/load (position + inventory + equipment)
- Beautiful console UI with borders, colors (via ANSI), and smooth flow
- Vault puzzles, prophecies, crits, random loot — tons of replayability!

🎮 How to Play the Final Game
cd quest-08-expanded-inventory
cd src
python main.py

Explore commands like go north, attack, equip sword, save, shop, inventory, etc. Type help anytime!

🤝 Contributing & Feedback

- Found a bug or want a Bonus Quest (multiplayer? GUI? procedural generation?) → Open an Issue or PR!
- Video feedback → Drop a comment on the matching YouTube episode (I read every single one ❤️)

📜 License
MIT License — Free to use, modify, fork, and learn from for personal or educational purposes. Commercial use welcome too!

👤 Created by
Samuel (ZeroLvL)
Lake Elsinore, California
March 2026
Let's build epic things together!
YouTube → @CodingQuests • GitHub → zeroleveldev
```
