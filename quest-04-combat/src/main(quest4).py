"""
Quest #4 - Demo
Runs the full combat system with player, enemy, and loot.
"""

from player import Player
from combat import Enemy, battle

def main():
    print("\n=== QUEST #4 : THE COMBAT SYSTEM ===")
    
    # Get hero name
    name = input("Enter your hero's name: ").strip()
    if not name:
        name = "Brave Adventurer"
    
    player = Player(name)
    
    # Starting inventory
    player.add_gold(25)
    player.inventory.add_item("Health Potion", 2)
    player.inventory.add_item("Rusty Sword", 1)
    
    # Show initial status
    print("\nYour starting status:")
    player.display_status()
    player.inventory.display()
    
    # Create an enemy with a loot table
    goblin_loot = [
        {"type": "item", "item": "Health Potion", "chance": 0.2, "amount": 1}, # 20% chance 
        {"type": "item", "item": "Iron Dagger", "chance": 0.05, "amount": 1}, # 5% chance
        {"type": "item", "item": "The Legend of the IceSplinter", "chance": 0.005}, # .05% chance
        {"type": "gold", "chance": 0.9, "min": 2, "max": 50}, # 90% chance for 5-20 gold
        {"type": "item", "item": "Goblin Tooth", "chance": 0.3, "amount": 2}, # 30% chance for 2 teeth to drop (collectible / quest items)
    ]
    enemy = Enemy("Goblin", 30, loot_table=goblin_loot) # High health for a bit more challenge 
    
    # Start battle
    if battle(player, enemy):
        print("\nVictory! Here's your updated status:")
        player.display_status()
        player.inventory.display()
    else:
        print("\nDefeat... Game Over.")

if __name__ == "__main__":
    main()