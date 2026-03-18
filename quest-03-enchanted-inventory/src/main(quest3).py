"""
Quest #3 - Demo
Runs the full player + inventory system.
"""

from player import Player

def main():
    print("\n=== QUEST #3 : THE ENCHANTED INVENTORY ===")
    
    # Get hero name
    name = input("Enter your hero's name: ").strip()
    if not name: 
        name = "Brave Adventurer"
    
    player = Player(name)
    
    # Starting Inventory
    player.add_gold(25)
    player.inventory.add_item("Health Potion", 2)
    player.inventory.add_item("Iron Sword", 1)
    player.inventory.add_item("Iron Helm", 3)
    player.inventory.add_item("Magic Scroll", 5)
    
    # Show everything
    player.display_status()
    player.inventory.display()
    
if __name__ == "__main__":
    main()