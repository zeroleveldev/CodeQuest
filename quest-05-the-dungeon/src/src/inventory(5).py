"""
Quest #3 - Enchanted Inventory System
Manages items, quantities, and nice display logic.
"""

class Inventory:
    def __init__(self):
        # Dictionary: key = item_name. value = quantity
        # Fast look up, easy quantity tracking - perfect for games!
        
        self.items: dict[str, int] = {} # name -> {"data": {...}, "amount": n}
    
    def add_item(self, item_name: str, item_data: dict, amount: int=1) -> bool:
        """Add one or more of an item. Returns True if successful."""
        if amount <= 0:
            return False
        if item_name in self.items:
            self.items[item_name]["amount"] += amount
        else:
            self.items[item_name] = {"data": item_data, "amount": amount}
        return True
    
    def remove_item(self, item_name: str, amount: int=1) -> bool:
        """Remove items. Returns True only if the player had enough."""
        if item_name not in self.items or self.items[item_name]["amount"] < amount:
            return False
        self.items[item_name]["amount"] -= amount
        if self.items[item_name]["amount"] == 0:
            del self.items[item_name]
        return True
    
    def has_item(self, item_name: str) -> bool:
        """Returns True if the player has at least one of this item."""
        return item_name in self.items and self.items[item_name]["amount"] > 0

    def get_quantity(self, item_name: str) -> int:
        """Returns how many of an item the player has (0 if none)"""
        if item_name in self.items:
            return self.items[item_name]["amount"]
        return 0
    
    def display(self):
        """Pretty print the inventory, sorted alphabetically."""
        print("\n=== INVENTORY ===")
        if not self.items:
            print("Your bag is empty.")
            return 
        print("You are carrying:")
        for name, entry in sorted(self.items.items()):
            data = entry["data"]
            amt = entry["amount"]
            print(f" - {name} x{amt}")
            if "attack" in data or "defense" in data or "max_hp_bonus" in data:
                bonuses = []
                if data.get("attack"): bonuses.append(f"+{data['attack']} atk")
                if data.get("defense"): bonuses.append(f"+{data['defense']} def")
                if data.get("max_hp_bonus"): bonuses.append(f"{data['max_hp_bonus']} max hp")
                print(f"    ({', '.join(bonuses)})")
            if "lore" in data:
                print(f"    \"{data['lore']}\"")
        