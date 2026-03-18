"""
Quest #3 - Player Data Model
Stores name, stats, gold, and the inventory.
Now with equipment bonuses
"""

from inventory import Inventory

class Player:
    def __init__(self, name: str):
        self.name = name
        self.gold: int = 0
        self.inventory = Inventory()
        
        # Basic stats 
        self.level: int = 1
        self.base_health: int = 30
        self.health: int = self.base_health
        self.base_damage: int = 5 
    
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
        self.health -= amount
        if self.health < 0:
            self.health = 0
    
    def is_alive(self) -> bool:
        """Check if player is still alive"""
        return self.health > 0
    
    def get_max_health(self) -> int:
        bonus = sum(
            data["data"].get("max_hp_bonus", 0) * data["amount"]
            for data in self.inventory.items.values()
        )
        return self.base_health + bonus
    
    def get_total_attack(self) -> int:
        return sum(
            data["data"].get("attack", 0) * data["amount"]
            for data in self.inventory.items.values()
        )
        
    def get_total_defense(self) -> int:
        return sum(
            data["data"].get("defense", 0) * data["amount"]
            for data in self.inventory.items.values()
        )
    
    def display_status(self):
        """Show everything important about the player."""
        print('\n === PLAYER STATUS ===')
        print(f"Name: {self.name}")
        print(f"Level: {self.level}")
        print(f"Health: {self.health}/{self.get_max_health()}")
        print(f"Gold: {self.gold} coins")
        atk = self.get_total_attack()
        dfn = self.get_total_defense()
        if atk or dfn:
            print(f"Attack bonus: +{atk} | Defense bonus: +{dfn}")