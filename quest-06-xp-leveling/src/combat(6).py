"""Quest #4 - Combat System
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
    def __init__(self, name: str, max_health: int, base_damage: int = 5 , xp_value: int = 50, loot_table: list[dict] = None):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.base_damage = base_damage
        self.xp_value = xp_value # XP given on defeat
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
                    amt = random.randint(drop.get("min", 3), drop.get("max", 50))
                    player.add_gold(amt)
                    print(f"You found {amt} gold on the {self.name}!")
                elif drop["type"] == "item":
                    player.inventory.add_item(
                        drop["item"],
                        drop.get("data", {"attack":0, "defense":0, "max_hp_bonus":0, "heal":0, "spell_damage":0,"lore":"A mysterious find"}),
                        drop.get("amount", 1)
                    )
                    print(f"You found {drop.get('amount',1)}x {drop['item']}!")
                    
def battle(player, enemy):
    """Run a turn-based battle between player and enemy."""
    print(f"\nA wild {enemy.name} appears!")
    
    while player.is_alive() and enemy.is_alive():
        print("\nBattle options: [a]ttack | [u]se item | [f]lee") # tactical menu for battle choices
        choice = input("Your action: ").strip().lower()
        
        if choice in ["f", "flee"]: # flee mechanic (50% chance, no rewards if success - risk/reward)
            if random.random() < 0.5: # 50% flee chance
                print("You escaped the battle!")
                return True
            else:
                print("You try to flee but the enemy blocks your path!")
                # Enemy attacks
        elif choice in ["u", "use", "use item"]: # item use in battle (potions heal, spells dmg enemy)
            player.inventory.display()
            raw_input = input("Use which item (or 'cancel'): ").strip()
            
            if raw_input.lower() == ["cancel", "c"]:
                continue
            
            # normalize to match stored title-case keys
            item_name = " ".join(word.capitalize() for word in raw_input.split())
            
            if player.inventory.has_item(item_name):
                data = player.inventory.items[item_name]["data"]
                if "heal" in data:
                    player.use_item(item_name)
                elif "spell_damage" in data:
                    dmg = data["spell_damage"]
                    enemy.take_damage(dmg)
                    print(f"You cast {item_name} for {dmg} damage!")
                    player.inventory.remove_item(item_name, 1)
                else:
                    print("That item can't be used in battle.")
                continue
            else:
                print("You don't have that.")
                continue
        else: # Defaul attacks
            
            input("\nPress ENTER to attack...")
        
            player_roll = roll_die(20)
            enemy_roll = roll_die(20)
        
            print(f"\nYou rolled: {player_roll}")
            print(f"{enemy.name} rolled: {enemy_roll}")
        
            if player_roll >= enemy_roll:
                damage = calculate_damage(player_roll, player.base_damage + player.get_total_attack())
                enemy.take_damage(damage)
                hit_msg = "CRITICAL STRIKE!" if player_roll >= 18 else "strike"
                print(f"You {hit_msg.lower()} the {enemy.name} for {damage} damage!")
            else:
                damage = calculate_damage(enemy_roll, enemy.base_damage)
                taken = player.take_damage(damage) # Uses new take_damage with defense
                hit_msg = "CRITICAL HIT!" if enemy_roll >= 18 else "hits"
                print(f"The {enemy.name} {hit_msg.lower()} you for {taken} damage!")
        
        print(f"\nYour health: {player.health}/{player.get_max_health()}")
        print(f"{enemy.name} Health: {enemy.health}/{enemy.max_health}")
        
    if player.is_alive():
        print(f"\nYou defeated the {enemy.name}!")
        player.gain_xp(enemy.xp_value) # Awards XP on win for progression
        enemy.generate_loot(player)
        return True
    else:
        print("\nYou were slain by the {enemy.name}...")
        return False 