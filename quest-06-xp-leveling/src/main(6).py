"""
Quest #5 - The Dungeon
Exploration, navigation, treasure, and combat encounters.
"""

from player import Player
from combat import battle, Enemy
from world import create_world

def main():
    print("\n=== QUEST #5 : THE DUNGEON ===")
    print("Commands: north/south/east/west | look | status | inventory | gear | use <item> | equip | quit")
    
    name = input("\nEnter your hero's name: ").strip() or "Brave Adventurer"
    player = Player(name)
    
    # Starting gear
    player.add_gold(25)
    player.inventory.add_item("Health Potion", {"heal": 20, "lore": "Restores 20 health."}, amount=3)
    player.inventory.add_item("Rusty Sword", {"type": "weapon", "attack": 3, "defense": 0, "max_hp_bonus": 0, "lore": "Dull but better than fists"}, amount=1)
    player.inventory.add_item("Leather Tunic", {"type": "armor", "defense": 2, "lore": "Basic protection"}, amount=1)
    
    current_room = create_world(player.level) # Pass level for enemy scaling
    last_direction = None
    
    while True:
        print(f"\n[You are in: {current_room.name}]")
        if last_direction:
            print(f"(You just came from the {last_direction})")
            
        current_room.describe()
        
        # Check for enemy
        if current_room.enemy and current_room.enemy.is_alive():
            print(f"\n!!! {current_room.enemy.name} lunges from the shadows!")
            if not battle(player, current_room.enemy):
                print("\nYour journey ends here... Game Over.")
                break
            else:
                print("The foe is defeated. The room feels safer now.")
                current_room.enemy = None # defeated, gone
        
        # Treasure Check
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
                current_room.treasure = None # CHANGED pick up all treasure(Simpler, more rewarding)
            else:
                print("You leave the treasure... for now.")
                
        command = input("\nWhat do you do? ").strip().lower()
        
        if command == "quit":
            print("You flee the dungeon... for now.")
        
        elif command in ["look", "l"]:
            continue # re-describe on next loop
        
        elif command in ["status", "s"]:
            player.display_status()
        
        elif command in ["inventory", "i"]:
            player.inventory.display()
            
        elif command == "use" and len(command) > 1: # use <item>
            item_name = " ".join(command[1:])
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
                print("Example: equip rusty sword weapon")
                print("Item names can have spaces - just put the slot last.")
                continue
            
            # Split from the RIGHT (rsplit) - last word is the slot
            parts = rest.rsplit(maxsplit=1) # splits once from the end
            
            if len(parts) < 2:
                print("Missing slot. Example: equip rust sword weapon")
                continue
            
            item_name = parts[0].strip() # "rust sword"
            slot = parts[1].strip().lower() # "weapon"
            
            # Normalize item name to title case (if your items are stored that way)
            item_name = " ".join(word.capitalize() for word in item_name.split())
            
            player.equip_item(item_name, slot)
                    
        elif command.startswith("unequip "):
            slot = command.split(maxsplit=1)[1].strip().lower()
            player.unequip(slot)
        
        elif command in ["gear", "equipped", "g"]:
            player.display_status()
            continue
            
        elif command in ["north", "south", "east", "west"]:
            next_room = current_room.get_room_in_direction(command)
            if next_room:
                current_room = next_room
                last_direction = command  # ← already using full word, good
            else:
                print("You can't go that way - solid stone or darkness blocks the path.")
        else:
            print("Unknown command. Try: north/south/east/west, look, status, inventory, quit")

if __name__ == "__main__":
    main()