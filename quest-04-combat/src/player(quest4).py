"""
Quest #3 - Player Data Model
Stores name, stats, gold, and the inventory.
"""

from inventory import Inventory

class Player:
    def __init__(self, name: str):
        self.name = name
        self.gold: int = 0
        self.inventory = Inventory()
        
        # Basic stats 
        self.level: int = 1
        self.health: int = 30
        self.max_health: int = 30
        self.base_damage: int = 5 # Extensible: weapons/level will boost this
    
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
    
    def display_status(self):
        """Show everything important about the player."""
        print('\n === PLAYER STATUS ===')
        print(f"Name: {self.name}")
        print(f"Level: {self.level}")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Gold: {self.gold} coins")