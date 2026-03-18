from player import Player
from combat import battle
from world import create_world
import random
import json
import time

# ── New for Quest #7: Shop system with timed refresh ──
class Shop:
    def __init__(self):
        self.last_refresh = time.time()
        self.stock = self.generate_stock()

    def generate_stock(self):
        with open("items.json", "r") as f:
            items_data = json.load(f)
        all_items = []
        for cat in ["weapons", "armor", "accessories"]:
            for rarity in ["common", "rare", "epic", "legendary"]:
                all_items.extend(items_data[cat][rarity])
        for cat in ["potions", "spells"]:
            all_items.extend(items_data[cat])
        return random.sample(all_items, min(5, len(all_items)))

    def refresh_if_needed(self):
        if time.time() - self.last_refresh > 600:  # 10 minutes
            self.stock = self.generate_stock()
            self.last_refresh = time.time()
            print("\nThe merchant restocks their wares!")

    def display(self, player):
        self.refresh_if_needed()
        print("\n=== MERCHANT'S WARES ===")
        for i, item in enumerate(self.stock, 1):
            bonuses = []
            if "attack" in item: bonuses.append(f"+{item['attack']} atk")
            if "defense" in item: bonuses.append(f"+{item['defense']} def")
            if "max_hp_bonus" in item: bonuses.append(f"+{item['max_hp_bonus']} hp")
            if "heal" in item: bonuses.append(f"Heals {item['heal']}")
            if "spell_damage" in item: bonuses.append(f"Spell dmg {item['spell_damage']}")
            bonus_str = f" ({', '.join(bonuses)})" if bonuses else ""
            print(f"{i}. {item['name']}{bonus_str} - {item['price']} gold")
            if "lore" in item:
                print(f"   \"{item['lore']}\"")
        choice = input("\nBuy which? (number or 'cancel'): ").strip().lower()
        if choice in ["cancel", "c"]:
            return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.stock):
                item = self.stock[idx]
                if player.spend_gold(item["price"]):
                    player.inventory.add_item(
                        item["name"],
                        {k: v for k, v in item.items() if k not in ["price", "rarity"]},
                        1
                    )
                    print(f"Purchased {item['name']}!")
                    del self.stock[idx]
                else:
                    print("Not enough gold!")
        except ValueError:
            print("Invalid choice.")

def main():
    print("\n=== QUEST #7 : THE DUNGEON WITH SAVE/LOAD AND SHOP ===")
    print("Commands: north/south/east/west | look | status | inventory | gear | use <item> | equip | save | load | quit")
    
    load_game = input("\nLoad saved game? (y/n): ").strip().lower() == "y"
    
    if load_game:
        try:
            with open("save.json", "r") as f:
                data = json.load(f)
            player = Player("temp")
            player.from_dict(data["player"])
            current_room, all_rooms = create_world(player.level)
            for name in data.get("cleared_enemies", []):
                if name in all_rooms:
                    all_rooms[name].enemy = None
            for name in data.get("taken_treasures", []):
                if name in all_rooms:
                    all_rooms[name].treasure = None
            current_room = all_rooms[data["current_room"]]
            print("Game loaded successfully!")
        except FileNotFoundError:
            print("No save file found. Starting new game.")
            load_game = False
    
    if not load_game:
        name = input("\nEnter your hero's name: ").strip() or "Brave Adventurer"
        player = Player(name)
        player.add_gold(25)
        player.inventory.add_item("Health Potion", {"heal": 20, "lore": "Restores 20 health."}, amount=3)
        player.inventory.add_item("Rusty Sword", {"type": "weapon", "attack": 3, "defense": 0, "max_hp_bonus": 0, "lore": "Dull but better than fists"}, amount=1)
        player.inventory.add_item("Leather Tunic", {"type": "armor", "defense": 2, "lore": "Basic protection"}, amount=1)
        current_room, all_rooms = create_world(player.level)
    
    shop = Shop()
    last_direction = None
    opposites = {"north": "south", "south": "north", "east": "west", "west": "east"}
    
    while True:
        print(f"\n[You are in: {current_room.name}]")
        if last_direction:
            print(f"(You just came from the {last_direction})")
            
        current_room.describe()
        
        # ── New for Quest #7: Shop appears 100% in Merchant's Den, 10% chance elsewhere ──
        if current_room.name == "Merchant's Den" or random.random() < 0.1:
            if current_room.name == "Merchant's Den":
                print("\nThe merchant greets you with a sly smile.")
            else:
                print("\nA traveling merchant appears out of the shadows!")
            shop.display(player)
        
        if current_room.enemy and current_room.enemy.is_alive():
            print(f"\n!!! {current_room.enemy.name} lunges from the shadows!")
            if not battle(player, current_room.enemy):
                print("\nYour journey ends here... Game Over.")
                break
            else:
                print("The foe is defeated. The room feels safer now.")
                current_room.enemy = None
        
        if current_room.treasure:
            print("\nYou spot treasure glinting in the dim light!")
            items = list(current_room.treasure.keys())
            for i, item in enumerate(items, 1):
                data = current_room.treasure[item]
                bonuses = []
                if "attack" in data: bonuses.append(f"+{data['attack']} atk")
                if "defense" in data: bonuses.append(f"+{data['defense']} def")
                if "max_hp_bonus" in data: bonuses.append(f"+{data['max_hp_bonus']} hp")
                if "heal" in data: bonuses.append(f"Heals {data['heal']}")
                if "spell_damage" in data: bonuses.append(f"Spell {data['spell_damage']} dmg")
                print(f" {i}. {item} ({', '.join(bonuses)})")
                if "lore" in data:
                    print(f"    \"{data['lore']}\"")
            choice = input("\nPickup all (y/n)").lower()
            if choice in ["y", "yes"]:
                for item, data in list(current_room.treasure.items()):
                    player.inventory.add_item(item, data)
                    print(f"Obtained {item}!")
                current_room.treasure = None
            else:
                print("You leave the treasure... for now.")
                
        command = input("\nWhat do you do? ").strip().lower()
        
        if command == "quit":
            print("You flee the dungeon... for now.")
            break
        
        elif command == "save":
            data = {
                "player": player.to_dict(),
                "current_room": current_room.name,
                "cleared_enemies": [name for name in all_rooms if all_rooms[name].enemy is None],
                "taken_treasures": [name for name in all_rooms if all_rooms[name].treasure is None]
            }
            with open("save.json", "w") as f:
                json.dump(data, f)
            print("Game saved!")
        
        elif command == "load":
            try:
                with open("save.json", "r") as f:
                    data = json.load(f)
                player.from_dict(data["player"])
                current_room, all_rooms = create_world(player.level)
                for name in data.get("cleared_enemies", []):
                    if name in all_rooms:
                        all_rooms[name].enemy = None
                for name in data.get("taken_treasures", []):
                    if name in all_rooms:
                        all_rooms[name].treasure = None
                current_room = all_rooms[data["current_room"]]
                print("Game loaded!")
            except FileNotFoundError:
                print("No save file found.")
        
        elif command in ["look", "l"]:
            continue
        
        elif command in ["status", "s"]:
            player.display_status()
        
        elif command in ["inventory", "i"]:
            player.inventory.display()
            
        elif command.startswith("use "):
            item_name = command[4:].strip()
            player.use_item(item_name)
        
        elif command == "equip":
            print("Usage: equip <item name> <slot>")
            print("Example: equip rusty sword weapon")
            print("Slots: weapon, armor, accessory")
            continue
        
        elif command.startswith("equip "):
            rest = command[6:].strip()
            if not rest:
                print("Usage: equip <item name> <slot>")
                continue
            parts = rest.rsplit(maxsplit=1)
            if len(parts) < 2:
                print("Missing slot.")
                continue
            item_name = " ".join(word.capitalize() for word in parts[0].split())
            slot = parts[1].strip().lower()
            player.equip_item(item_name, slot)
                    
        elif command.startswith("unequip "):
            slot = command[9:].strip().lower()
            player.unequip(slot)
        
        elif command in ["gear", "equipped", "g"]:
            player.display_status()
            continue
            
        elif command in ["north", "south", "east", "west"]:
            next_room = current_room.get_room_in_direction(command)
            if next_room:
                current_room = next_room
                last_direction = opposites.get(command)
            else:
                print("You can't go that way.")
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()