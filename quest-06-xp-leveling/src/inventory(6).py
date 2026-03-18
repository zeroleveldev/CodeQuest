"""
Quest #3 - Enchanted Inventory System
Manages items, quantities, and nice display logic.
supports item data. helpers, and now spells as items.
"""

class Inventory:
    def __init__(self):
        # Dictionary: key = item_name. value = quantity
        # Fast look up, easy quantity tracking - perfect for games!
        
        self.items: dict[str, int] = {} # name -> {"data": {...}, "amount": n}
        
    def _normalize_name(self, name: str) -> str:
        """Convert item name to consistent title case."""
        if not name:
            return 
        return " ".join(word.capitalize() for word in name.split())
    
    def add_item(self, item_name: str, item_data: dict, amount: int=1) -> bool:
        """Add one or more of an item. Returns True if successful."""
        
        if amount <= 0:
            return False
        
        normalized = self._normalize_name(item_name)
        if not normalized: 
            print("Invalid item name.")
            return False
        
        if normalized in self.items:
            self.items[normalized]["amount"] += amount
        else:
            self.items[normalized] = {"data": item_data, "amount": amount}
        return True
    
    def remove_item(self, item_name: str, amount: int=1) -> bool:
        """Remove items. Returns True only if the player had enough."""
        normalized = self._normalize_name(item_name)
        
        if normalized not in self.items or self.items[normalized]["amount"] < amount:
            return False
        
        self.items[normalized]["amount"] -= amount
        if self.items[normalized]["amount"] == 0:
            del self.items[normalized]
        return True
    
    def has_item(self, item_name: str) -> bool:
        """Returns True if the player has at least one of this item."""
        normalized = self._normalize_name(item_name)
        return normalized in self.items and self.items[normalized]["amount"] > 0

    def get_quantity(self, item_name: str) -> int:
        """Returns how many of an item the player has (0 if none)"""
        normalized = self._normalize_name(item_name)
        if normalized in self.item:
            return self.items[normalized]["amount"]
        return 0
    
    def display(self):
        """Pretty print the inventory, sorted alphabetically."""
        print("\n=== INVENTORY ===")
        if not self.items:
            print("Your bag is empty.")
            return 
        print("You are carrying:")
        
        # Sort keys case-insensitively for nicer display
        sorted_items = sorted(self.items.items(), key=lambda x: x[0].lower())
        
        for name, entry in sorted_items:
            data = entry["data"]
            amt = entry["amount"]
            print(f" - {name} x{amt}")
            bonuses = []
            if data.get("attack"): bonuses.append(f"+{data['attack']} atk")
            if data.get("defense"): bonuses.append(f"+{data['defense']} def")
            if data.get("max_hp_bonus"): bonuses.append(f"+{data['max_hp_bonus']} max hp")
            if data.get("heal"): bonuses.append(f"Heals {data['heal']} hp")
            if data.get("spell_damage"): bonuses.append(f"Spell dmg: {data['spell_damage']}")
            
            if bonuses:
                print(f"    ({', '.join(bonuses)})")
            
            if "lore" in data:
                print(f"    \"{data['lore']}\"")
        