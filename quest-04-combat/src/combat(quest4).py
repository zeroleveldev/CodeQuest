"""Quest #4 - Combot System
Handles enemies, battles, and loot drops.
"""

import random
from dice import roll_die

def calculate_damage(roll: int, base_damage: int) -> int:
    """Calculate damage with crit multiplier (18-20 - 1.5x). Scales perfectly with stats/weapons"""
    if roll >= 18:
        return int(base_damage * 1.5) # 50 bonus - "a little more" that grows with base
    return base_damage

class Enemy:
    def __init__(self, name: str, max_health: int, loot_table: list[dict] = None):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.base_damage: int = 5 # extensible: stronger enmeies get higher base
        self.loot_table = loot_table or []
    
    def take_damage(self, amount: int):
        """Apply damage to health, clamping at 0."""
        self.health -= amount
        if self.health < 0:
            self.health = 0
            
    def is_alive(self) -> bool:
        """Check if the enemy is still alive."""
        return self.health > 0
    
    def generate_loot(self, player):
        """Generate and add loot to the player based on the loot table."""
        for drop in self.loot_table:
            if random.random() < drop.get("chance", 1.0):
                if drop["type"] == "gold":
                    amt = random.randint(drop["min"], drop["max"])
                    player.add_gold(amt)
                    print(f"You found {amt} gold on the {self.name}!")
                elif drop["type"] == "item":
                    item = drop["item"]
                    amount = drop.get("amount", 1)
                    player.inventory.add_item(item, amount)
                    print(f"You found {amount} x {item} on the {self.name}!")
                    
def battle(player, enemy):
    """Run a turn-based battle between player and enemy."""
    print(f"\nA wild {enemy.name} appears!")
    
    while player.is_alive() and enemy.is_alive():
        input("\nPress ENTER to attack...")
        
        player_roll = roll_die(20)
        enemy_roll = roll_die(20)
        
        print(f"\nYou rolled: {player_roll}")
        print(f"{enemy.name} rolled: {enemy_roll}")
        
        if player_roll >= enemy_roll:
            damage = calculate_damage(player_roll, player.base_damage)
            enemy.take_damage(damage)
            hit_msg = "CRITICAL STRIKE!" if player_roll >= 18 else "strike"
            print(f"You {hit_msg.lower()} the {enemy.name} for {damage} damage!")
        else:
            damage = calculate_damage(enemy_roll, enemy.base_damage)
            player.take_damage(damage)
            hit_msg = "CRITICAL HIT!" if enemy_roll >= 18 else "hits"
            print(f"The {enemy.name} {hit_msg.lower()} you for {damage} damage!")
        
        print(f"\nYour health: {player.health}/{player.max_health}")
        print(f"{enemy.name} Health: {enemy.health}/{enemy.max_health}")
        
    if player.is_alive():
        print(f"\nYou defeated the {enemy.name}!")
        enemy.generate_loot(player)
        return True
    else:
        print("\nYou were slain by the {enemy.name}...")
        return False