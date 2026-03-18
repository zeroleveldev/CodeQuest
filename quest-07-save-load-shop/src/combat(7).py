import random
from dice import roll_die

def calculate_damage(roll: int, base_damage: int) -> int:
    if roll >= 18:
        return int(base_damage * 1.5)
    return base_damage

class Enemy:
    def __init__(self, name: str, max_health: int, base_damage: int = 5, xp_value: int = 50, loot_table: list[dict] = None):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.base_damage = base_damage
        self.xp_value = xp_value
        self.loot_table = loot_table or []
    
    def take_damage(self, amount: int):
        self.health -= amount
        if self.health < 0:
            self.health = 0
            
    def is_alive(self) -> bool:
        return self.health > 0
    
    def generate_loot(self, player):
        for drop in self.loot_table:
            if random.random() < drop.get("chance", 1.0):
                if drop["type"] == "gold":
                    amt = random.randint(drop.get("min", 3), drop.get("max", 50))
                    player.add_gold(amt)
                    print(f"You found {amt} gold on the {self.name}!")
                elif drop["type"] == "item":
                    player.inventory.add_item(
                        drop["item"],
                        drop.get("data", {"attack":0, "defense":0, "max_hp_bonus":0, "heal":0, "spell_damage":0, "lore":"A mysterious find"}),
                        drop.get("amount", 1)
                    )
                    print(f"You found {drop.get('amount',1)}x {drop['item']}!")

                # ── New for Quest #7: Support random rarity-based drops from items.json ──
                elif drop["type"] == "random_item":
                    import json
                    try:
                        with open("items.json", "r") as f:
                            items_data = json.load(f)
                    except FileNotFoundError:
                        print("Warning: items.json not found! No random item dropped.")
                        continue
                    except json.JSONDecodeError:
                        print("Warning: items.json is invalid! No random item dropped.")
                        continue
                    
                    rarity = drop["rarity"]
                    cat = random.choice(["weapons", "armor", "accessories", "potions", "spells"])
                    
                    if cat in ["potions", "spells"]:
                        if cat in items_data and items_data[cat]:
                            item = random.choice(items_data[cat])
                        else:
                            print(f"Warning: No items in category '{cat}'")
                            continue
                    else:
                        if cat in items_data and rarity in items_data[cat] and items_data[cat][rarity]:
                            item = random.choice(items_data[cat][rarity])
                        else:
                            print(f"Warning: No {rarity} items in category '{cat}'")
                            continue
                        
                    player.inventory.add_item(
                        item["name"],
                        {k: v for k, v in item.items() if k not in ["price", "rarity"]},
                        1
                    )
                    print(f"You found a random {rarity} item: {item['name']}!")
                    
def battle(player, enemy):
    print(f"\nA wild {enemy.name} appears!")
    
    while player.is_alive() and enemy.is_alive():
        print("\nBattle options: [a]ttack | [u]se item | [f]lee")
        choice = input("Your action: ").strip().lower()
        
        if choice in ["f", "flee"]:
            if random.random() < 0.5:
                print("You escaped the battle!")
                return True
            else:
                print("You try to flee but the enemy blocks your path!")
        elif choice in ["u", "use", "use item"]:
            player.inventory.display()
            raw_input = input("Use which item (or 'cancel'): ").strip()
            
            if raw_input.lower() in ["cancel", "c"]:
                continue
            
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
        else:
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
                taken = player.take_damage(damage)
                
                hit_msg = "CRITICAL HIT!" if enemy_roll >= 18 else "hits"
                blocked = damage - taken
                # Shows the amount of damage blocked by armor
                if blocked > 0:
                    print(f"The {enemy.name} {hit_msg.lower()} you for {taken} damage! ({blocked} blocked by armor)")
                else:
                    print(f"The {enemy.name} {hit_msg.lower()} you for {taken} damage!")
        
        print(f"\nYour health: {player.health}/{player.get_max_health()}")
        print(f"{enemy.name} Health: {enemy.health}/{enemy.max_health}")
        
    if player.is_alive():
        print(f"\nYou defeated the {enemy.name}!")
        player.gain_xp(enemy.xp_value)
        enemy.generate_loot(player)
        return True
    else:
        print("\nYou were slain by the {enemy.name}...")
        return False