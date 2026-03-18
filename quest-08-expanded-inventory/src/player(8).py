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
        # Expanded equipment slots using slot_type from item.json
        self.equipment = {
            "main_hand": None,
            "off_hand": None,
            "head": None,
            "shoulders": None,
            "chest": None,
            "gloves": None,
            "pants": None,
            "boots": None,
            "necklace": None,
            "ring": None, # One ring for now we can add more later
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
        
        if not self.inventory.has_item(item_name):
            print(f"You don't have {item_name}.")
            return False
        
        item_data = self.inventory.items[item_name]["data"]
        item_slot_type = item_data.get("slot_type")
        
        # Normalize slot input to match our equipment keys
        valid_slots = list(self.equipment.keys())
        if slot not in valid_slots:
            print(f"Invalid slot: {slot}. Valid slots: {', '.join(valid_slots)}")
            return False
        
        # --- Allow dual wield (two 1h weapons) ---
        is_one_handed = item_slot_type in ["main_hand", "off_hand"]
        
        # --- Confilct checks & auto-unequip logic ---
        if slot == "main_hand":
            if item_slot_type == "two_hand":
                # Two-hand weapon -> auto-unequip off-hand if occupied
                if self.equipment["off_hand"]:
                    old_off = self.equipment["off_hand"]
                    self.inventory.add_item(old_off["name"], old_off["data"])
                    self.inventory["off_hand"] = None
                    print(f"Auto-unequipped {old_off['name']} from off_hand to equip two-handed weapon.")
            elif item_slot_type in ["main_hand", "off_hand"]:
                # 1H weapon in main -> allow off-hand to stay (dual wield possible)
                pass
            else:
                print(f"{item_name} cannot go in main_hand.")
                return False
        
        elif slot == "off_hand":
            main_item = self.equipment.get("main_hand.")
            
            if main_item and main_item["data"].get("slot_type") == "two_hand":
                print("Cannot equip off-hand while holding a two-handed weapon!")
                return False
            
            # Allow 1H weapin or shield/accessory in off-hand
            if item_slot_type not in ["off_hand", "main_hand", "accessory"]:
                print(f"{item_name} cannot go in off_hand.")
                return False
            
            # If putting 1H weapon in off_hand ites dual wield - no conflict with main           
        
        # --- 2H weapon rule ---
        if item_slot_type == "two_hand" and slot != "main_hand":
            print(f"{item_name} is a two-handed weapon and can only go in main_hand")
            return False
        
        # --- Shield / off-hand rule ---
        if slot == "off_hand":
            main = self.equipment.get("main_hand")
            if main and main["data"].get("slot_type") == "two-hand":
                print("You cannot use an off-hand item while holding a two-handed weapon!")
                return False
            if item_slot_type not in ["off-hand", "accessory"]: # shields are off_hand
                print(f"{item_name} cannot go in off-hand.")
                return False
        
        # --- Main-hand can accept 1H or 2H ---
        if slot == "main-hand" and item_slot_type not in ["main_hand", "two_hand"]:
            print(f"{item_name} cannot go in main_hand.")
            return False
        
        # Accessory mapping (necklace or ring)
        if item_slot_type == "accessory" and slot not in ["necklace", "ring"]:
            print(f"Accessories can only go in necklace or ring slots.")
            return False
        
        # All other armor slots must match exactly
        if item_slot_type in ["head", "shoulders", "chest", "gloves", "pants", "boots"] and slot != item_slot_type:
            print(f"{item_name} belongs in the {item_slot_type} slot.")
            return False
        
        # unequip old item back to inventory
        old_item = self.equipment.get(slot)
        if old_item:
            self.inventory.add_item(old_item["name"], old_item["data"])
            print(f"Unequipped {old_item['name']} from {slot}.")
            # If we just unequipped a 2H from main_hand, off_hand is now free again
            if slot == "main_hand" and old_item["data"].get("slot_type") == "two_hand":
                print("(Your off-hand is now free again)")
        
        # Equip new item
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
        if item:
            self.inventory.add_item(item["name"], item["data"])
            self.equipment[slot] = None
            print(f"Unequipped {item['name']} from {slot}.")
            # If we unequipped a 2H, remind player off-hand is free
            if slot == "main_hand" and item["data"].get("slot_type") == "two_hand":
                print("Your off-hand is now free again")
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
        print("\n" + "═" * 50)
        print(f"  {self.name.upper()}  —  Level {self.level}")
        print("═" * 50)
        
        print(f"  Health     : {self.health:3d} / {self.get_max_health():3d}")
        print(f"  Gold       : {self.gold:,} coins")
        print(f"  XP         : {self.xp:,} / {self.xp_to_next:,}")
        
        atk = self.get_total_attack()
        dfn = self.get_total_defense()
        hp_b = self.get_max_health() - self.base_health
        
        bonuses = []
        
        if atk: bonuses.append(f"+{atk} atk")
        if dfn: bonuses.append(f"+{dfn} def")
        if hp_b: bonuses.append(f"+{hp_b} max hp")
        
        if bonuses:
            print(f"  Bonuses    : {', '.join(bonuses)}")
        else:
            print("  Bonuses    : none")
                
        print("\n" + "─" * 50)
        print("  EQUIPPED GEAR")
        print("─" * 50)
        
        for slot, item in self.equipment.items():
            slot_name = slot.replace("_", " ").title()
            if item:
                data = item["data"]
                bonuses = []
                if data.get("attack"): bonuses.append(f"+{data['attack']} atk")
                if data.get("defense"): bonuses.append(f"+{data['defense']} def")
                if data.get("max_hp_bonus"): bonuses.append(f"{data['max_hp_bonus']} max hp")
                bonus_str = f" ({', '.join(bonuses)})" if bonuses else ""
                print(f"  {slot_name:12} : {item['name']}{bonus_str}")
                if "lore" in data:
                    print(f" \"{data['lore']}\"")
            else:
                print(f"               ↳ \"{data['lore']}\"")
                print()
        
        print("=" * 50 + "\n")
                
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