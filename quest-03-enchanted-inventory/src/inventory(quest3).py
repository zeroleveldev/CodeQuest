"""
Quest 3 - Enchanted Inventory System
Manages items, quantities. and nice display logic
"""

class Inventory:
    def __init__(self):
        # Dictionary: key = item_name, value = quantity
        # Fast lookup, easy quantity tracking - perfect for game!
        self.items: dict[str, int] = {}
        
    def add_item(self, item_name: str, amount: int = 1) -> bool:
        """Add one or more of an item. Returns True if successful."""
        if amount <= 0:
            return False
        if item_name in self.items:
            self.items[item_name] += amount
        else:
            self.items[item_name] = amount
        
        return True
    
    def remove_item(self, item_name: str, amount: int = 1) -> bool:
        """Remove items. Returns Ture only if the player had enough."""
        if item_name not in self.items:
            return False
        if self.items[item_name] < amount:
            return False
        
        self.items[item_name] -= amount
        if self.items[item_name] == 0:
            del self.items[item_name]
        return True
    
    def has_item(self, item_name: str) -> bool:
        """True if the player has at least one of this item."""
        return item_name in self.items
    
    def get_quantity(self, item_name: str) -> int:
        """Returns how many of an item the player has (0 if none)."""
        return self.items.get(item_name, 0)
    
    def display(self):
        """Pretty-print the inventory, sorted alphabetically."""
        print("\n=== INVENTORY ===")
        if not self.items:
            print("Your bag is empty.")
            return
        
        print("You are carrying:")
        for item in sorted(self.items): # Sorted = nice, consistent order
            print(f" - {item} x{self.items[item]}")