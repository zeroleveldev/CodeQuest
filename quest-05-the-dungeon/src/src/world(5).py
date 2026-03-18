from room import Room
from combat import Enemy

def create_world() -> Room:
    entrance = Room("Dungeon Entrance", "Cold air seeps from the stone archway. A faint roar echoes from deeper within.")
    hall = Room("Great Hall", "Torches flicker against ancient stone walls. Shadows dance unnaturally.")
    armory = Room("Abandoned Armory", "Rusting weapons line the walls. Something skitters in the corner.")
    crypt = Room("Forgotten Crypt", "The scent of dust and decay fills the air. Sarcophagi lie broken.")
    library = Room("Ancient Library", "Shelves of crumbling tomes tower above. A draft comes from behind one shelf.")
    treasure_room = Room("Treasure Chamber", "Gold and relics shimmer in torchlight. The air feels heavy with greed.")
    
    hidden_room = Room("Hidden Vault", "A secret chamber untouched for centuries. Dust motes float in thin beams of light.")
    hidden_room.hidden = True # Could be used later for special logic
    
    # Connections
    entrance.connect("south", hall)
    hall.connect("north", entrance)
    hall.connect("east", armory)
    hall.connect("west", library)
    hall.connect("south", crypt)
    crypt.connect("north", hall)
    crypt.connect("south", treasure_room)
    treasure_room.connect("north", crypt)
    armory.connect("west", hall)
    library.connect("east", hall)
    library.connect("north", hidden_room)
    hidden_room.connect("south", library)
    
    # Enemies (with quest # 4 style loot tables)
    hall.enemy = Enemy(
        "Goblin Scout", 25, base_damage=6,
        loot_table=[
            {"type": "gold", "chance": 0.85, "min": 5, "max": 25},
            {"type": "item", "item": "Goblin Ear", "chance": 0.5, "amount": 1,
             "data": {"attack":0, "defense": 0, "max_hp_bonus":0, "lore": "A trophy... or bait?"}},
        ]
    )
    
    armory.enemy = Enemy(
        "Animated Armor", 40, base_damage=7,
        loot_table=[
            {"type": "item", "item": "Rusted Gauntlets", "chance": 0.6, "amount": 1,
             "data": {"attack": 1, "defense":4, "max_hp_bonus":0, "lore": "Still faintly warm from battle."}},
            {"type": "gold", "chance": 0.7, "min": 10, "max": 50},
        ]
    )
    
    # Treasure (now uses same dict format as inventory data)
    treasure_room.treasure = {
        "Flamebrand Sword": {
            "attack": 10, "defense": 0, "max_hp_bonus": 0,
            "lore": "Forged in dwarven liquid fire, The blade hums with heat."
        },
        "ShadowSteel Armor": {
            "attack": 0, "defense": 15, "max_hp_bonus": 0,
            "lore": "Tempered in darkness beneath forgotten mountains."
        },
        "Ring of vitality": {
            "attack": 0, "defense": 0, "max_hp_bonus": 20,
            "lore": "It pulses faintly with ancient life."
        }
    }
    
    hidden_room.treasure = {
        "Crown of the First King": {
            "attack": 5, "defense": 5, "max_hp_bonus": 15,
            "lore": "Worn before history had ink. Power radiates from every gem."
        }
    }
    
    return entrance