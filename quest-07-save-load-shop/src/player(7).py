from inventory import Inventory
import json # for save/ load later

"""
Quest #3 - Player Data Model
Stores name, stats, gold, and the inventory.
Now with equipment bonuses
Now with XP, leveling and item usage.
Now with equipment slots (only equipped items give bonuses)
"""

from inventory import Inventory

class Player:
    def __init__(self, name: str):
        self.name = name
        self.gold: int = 50000
        self.inventory = Inventory()
        
        # Basic stats 
        self.level: int = 1
        self.base_health: int = 30
        self.health: int = self.base_health
        self.base_damage: int = 5
        self.xp: int = 0
        self.xp_to_next: int  = 100
        
        # Equipment slots (only these give bonuses)
        self.equipment = {
            "weapon": None, # {"name": "Iron Sword", "data": {...}}
            "armor": None,
            "accessory": None # Rings, amulets
        }
    
    def add_gold(self, amount: int) -> bool:
        """Add gold. Returns True only for positive amounts."""
        if amount <= 0:
            return False
        self.gold += amount
        return True
    
    def spend_gold(self, amount: int) -> bool:
        """Spend gold. Returns True of the player had enough."""
        if self.gold < amount:
            return False
        self.gold -= amount
        return True
    
    def take_damage(self, amount: int):
        """Apply damage to health, clamping at 0."""
        defense = self.get_total_defense()
        
        if amount <= 0:
            return 0
        
        if defense <= 0:
            damage_taken = amount
        else:
            # Percent reduction with diminishing returns (balanced)
            # 50 def = 33% reduction
            # 100 def = 50% reduction
            # 200 def = 67% reduction
            # 400 def = 80% reduction
            reduction = defense / (defense + 100.0) # <- change 100 to tune difficulty
            damage_taken = max(1, int(amount * (1 - reduction)))
        
        self.health -= damage_taken
        if self.health < 0:
            self.health = 0
            
        return damage_taken # Stil returns actual damage taken fro battle messages 
    
    def is_alive(self) -> bool:
        """Check if player is still alive"""
        return self.health > 0
    
    def gain_xp(self, amount: int): # Handles XP gain and auto-level
        self.xp += amount
        while self.xp >= self.xp_to_next:
            self.level_up()
    
    def level_up(self): # progression (boosts stats, heals, scales next XP)
        self.level += 1
        self.xp -= self.xp_to_next
        self.xp_to_next = int(self.xp_to_next * 1.5) # 50% more each level
        self.base_damage += 10 #Health increase
        self.health = self.get_max_health() # Adds the full heal after level up
        self.base_damage += 2
        print(f"\n*** LEVEL UP! You are now level {self.level} ***")
        print("Max Health +10, damage +2, and Fully RESTORED!")
    
    def get_max_health(self) -> int:
        bonus = 0
        for slot_item in self.equipment.values():
            if slot_item and slot_item["data"].get("max_hp_bonus"):
                bonus += slot_item["data"]["max_hp_bonus"]
        return self.base_health + bonus
    
    def get_total_attack(self) -> int:
        total = 0
        for slot_item in self.equipment.values():
            if slot_item and slot_item["data"].get("attack"):
                total += slot_item["data"]["attack"]
        return total
                    
    def get_total_defense(self) -> int:
        total = 0
        for slot_item in self.equipment.values():
            if slot_item and slot_item["data"].get("defense"):
                total += slot_item["data"]["defense"]
        return total
    
    def equip_item(self, item_name: str, slot: str) -> bool:
        """Equip item to slot if valid type and inventory. Returns True if successful."""
        
        # Normalize right away
        item_name = " ".join(word.capitalize() for word in item_name.split())
        
        valid_slots = ["weapon", "armor", "accessory"]
        if slot not in valid_slots:
            print(f"Invalid slot: {slot}. Use weapon, armor, accessory.")
            return False
        
        if not self.inventory.has_item(item_name):
            print(f"You don't have {item_name}.")
            return False
        
        item_data = self.inventory.items[item_name]["data"]
        item_type = item_data.get("type", "none")
        
        # validate type matches slot
        if slot == "weapon" and item_type != "weapon":
            print(f"{item_name} can't be equipped as a weapon.")
            return False
        if slot == "armor" and item_type != "armor":
            print(f"{item_name} can't be equipped as armor.")
            return False
        if slot == "accessory" and item_type != "accessory":
            print(f"{item_name} can't be equipped as accessory.")
            return False
        
        # unequip old item back to inventory
        old_item = self.equipment.get(slot)
        if old_item:
            self.inventory.add_item(old_item["name"], old_item["data"])
        
        # Move to equipment
        self.equipment[slot] = {
            "name": item_name,
            "data": item_data
        }
        self.inventory.remove_item(item_name, 1)
        print(f"Equipped {item_name} in {slot} slot!")
        return True
    
    # Unequip to inventory
    def unequip(self, slot: str) -> bool:
        if slot not in self.equipment:
            print(f"No item in {slot} slot.")
            return False
        item = self.equipment[slot]
        self.inventory.add_item(item["name"], item["data"])
        self.equipment[slot] = None
        print(f"Unequipped {item['name']} from {slot}.")
        return True
    
    def use_item(self, item_name: str) -> bool: # item interaction (potions heal, spells noted for battle )
        """USe a consumable item (e.g., potion heal). Returns True if used"""
        if not self.inventory.has_item(item_name):
            print(f"You dont have {item_name}.")
            return False
        
        data = self.inventory.items[item_name]["data"]
        
        if "heal" in data:
            heal_amt = data["heal"]
            old_health = self.health # optional debug
            self.health = min(self.get_max_health(), self.health + heal_amt)
            actual_health = self.health - old_health
            print(f"You used {item_name} and healed for {actual_health} health! ({self.health}/{self.get_max_health})")
            self.inventory.remove_item(item_name, 1)
            return True
        
        elif "spell_damage" in "data":
            # For spells - but in battle only? For now print not usable here
            print(f"{item_name} can only be used in battle.")
            return False
        
        else:
            print(f"{item_name} isn't usable.")
            return False
    
    def display_status(self):
        """Show everything important about the player."""
        print('\n === PLAYER STATUS ===')
        print(f"Name: {self.name}")
        print(f"Level: {self.level} (XP: {self.xp}/{self.xp_to_next})") # XP bar for progression visibility
        print(f"Health: {self.health}/{self.get_max_health()}")
        print(f"Gold: {self.gold} coins")
        
        atk = self.get_total_attack()
        dfn = self.get_total_defense()
        hp_b = self.get_max_health() - self.base_health
        if atk or dfn or hp_b:
            print(f"Bonuses: +{atk} Atk | +{dfn} Def | +{hp_b} Max HP")
        
        # Show equipped gear + bonuses
        print("\n=== EQUIPPED GEAR ===")
        
        for slot, item in self.equipment.items():
            if item:
                data = item["data"]
                bonuses = []
                if data.get("attack"): bonuses.append(f"+{data['attack']} atk")
                if data.get("defense"): bonuses.append(f"+{data['defense']} def")
                if data.get("max_hp_bonus"): bonuses.append(f"{data['max_hp_bonus']} max hp")
                bonus_str = f" ({', '.join(bonuses)})" if bonuses else ""
                print(f"{slot.capitalize()}: {item['name']}{bonus_str}")
                if "lore" in data:
                    print(f" \"{data['lore']}\"")
            else:
                print(f"{slot.capitalize()}: [empty]")

#----------- New for Quest #7 : Save/Load support -----------
    def to_dict(self):
        return {
            "name": self.name,
            "gold": self.gold,
            "level": self.level,
            "base_health": self.base_health,
            "health": self.health,
            "base_damage": self.base_damage,
            "xp": self.xp,
            "xp_to_next": self.xp_to_next,
            "inventory": {name: {"data": entry["data"], "amount": entry["amount"]}
                        for name, entry in self.inventory.items.items()},
            "equipment": {slot: item for slot, item in self.equipment.items() if item}
        }

    def from_dict(self, data: dict):
        self.name = data["name"]
        self.gold = data["gold"]
        self.level = data["level"]
        self.base_health = data["base_health"]
        self.health = data["health"]
        self.xp = data["xp"]
        self.xp_to_next = data["xp_to_next"]
        self.inventory.items = data["inventory"]
        self.equipment = data.get("equipment", {"weapons": None, "armor": None, "accessories": None})