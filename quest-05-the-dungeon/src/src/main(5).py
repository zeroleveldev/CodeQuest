"""
Quest #5 - The Dungeon
Exploration, navigation, treasure, and combat encounters.
"""

from player import Player
from combat import battle, Enemy
from world import create_world

def main():
    print("\n=== QUEST #5 : THE DUNGEON ===")
    print("Commands: north/south/east/west | look | status | inventory | quit")
    
    name = input("\nEnter your hero's name: ").strip() or "Brave Adventurer"
    player = Player(name)
    
    # Starting gear
    player.add_gold(25)
    player.inventory.add_item("Health Potion", {"attack": 0, "defense": 0, "max_hp_bonus": 0, "lore": "Restores bitality in desperate  times."}, amount=5)
    player.inventory.add_item("Rusty Sword", {"attack": 3, "defense": 0, "max_hp_bonus": 0, "lore": "Dull but better than fists"}, amount=1)
    
    current_room = create_world()
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
        
        command = input("\nWhat do you do? ").strip().lower()
        
        if command == "quit":
            print("You flee the dungeon... for now.")
        
        elif command in ["look", "l"]:
            continue # re-describe on next loop
        
        elif command in ["status", "s"]:
            player.display_status()
        
        elif command in ["inventory", "i"]:
            player.inventory.display()
            
        elif command in ["north", "south", "east", "west"]:
            next_room = current_room.get_room_in_direction(command)
            if next_room:
                current_room = next_room
                last_direction = command # Remember for feedback
            
            else:
                print("You cant go that wat  - solid stone or darkness blocks the path.")
        else:
            print("Unknown command. Try: north/south/east/west, look, status, inventory, quit")

if __name__ == "__main__":
    main()