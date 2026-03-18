class Inventory:
    def __init__(self):
        self.items: dict[str, dict] = {}
        
    def _normalize_name(self, name: str) -> str:
        if not name:
            return ""
        return " ".join(word.capitalize() for word in name.split())
    
    def add_item(self, item_name: str, item_data: dict, amount: int=1) -> bool:
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
        normalized = self._normalize_name(item_name)
        if normalized not in self.items or self.items[normalized]["amount"] < amount:
            return False
        self.items[normalized]["amount"] -= amount
        if self.items[normalized]["amount"] == 0:
            del self.items[normalized]
        return True
    
    def has_item(self, item_name: str) -> bool:
        normalized = self._normalize_name(item_name)
        return normalized in self.items and self.items[normalized]["amount"] > 0

    def display(self):
        print("\n" + "=" * 40)
        print("          INVENTORY")
        print("=" * 40)
        
        if not self.items:
            print("   Your bag is empty.\n")
            return
        
        print("You are carrying:\n")
        
        sorted_items = sorted(self.items.items(), key=lambda x: x[0].lower())
        
        for name, entry in sorted_items:
            data = entry["data"]
            amt = entry["amount"]
            print(f" • {name}{' x' + str(amt) if amt > 1 else ''}")
        
            bonuses = []
            if data.get("attack"): bonuses.append(f"+{data['attack']} atk")
            if data.get("defense"): bonuses.append(f"+{data['defense']} def")
            if data.get("max_hp_bonus"): bonuses.append(f"+{data['max_hp_bonus']} max hp")
            if data.get("heal"): bonuses.append(f"Heals {data['heal']} hp")
            if data.get("spell_damage"): bonuses.append(f"Spell dmg: {data['spell_damage']}")
            
            if bonuses:
                print(f"    └─{', '.join(bonuses)}")
            
            if "lore" in data:
                print(f"    ↳\"{data['lore']}\"")
            print() # space between lines