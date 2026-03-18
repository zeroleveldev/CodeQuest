from room import Room
from combat import Enemy
import json
import random
#---- New for Quest # 7: Load item definitions from json
with open("items.json", "r") as f:
    ITEMS_DATA = json.load(f)


# Starting area
def create_world(player_level: int) -> Room:
    entrance = Room("Dungeon Entrance", "Cold air seeps from the stone archway. A faint roar echoes from deeper within.")
    hall = Room("Great Hall", "Torches flicker against ancient stone walls. Shadows dance unnaturally.")
    armory = Room("Abandoned Armory", "Rusting weapons line the walls. Something skitters in the corner.")
    crypt = Room("Forgotten Crypt", "The scent of dust and decay fills the air. Sarcophagi lie broken.")
    library = Room("Ancient Library", "Shelves of crumbling tomes tower above. A draft comes from behind one shelf.")
    treasure_room = Room("Treasure Chamber", "Gold and relics shimmer in torchlight. The air feels heavy with greed.")
    
    # Deeper area(harder)
    lair = Room("Beast Lair", "Bones litter the floor. A low growl rumbles.")
    forge = Room("Cursed Forge", "Anvils glow with unholy fire. Heat waves distort the air.")
    throne = Room("Fallen Throne Room", "A shattered throne. Shadows of power linger.")
    abyss = Room("The Abyss", "Bottomless void. Madness creeps in.")
    
    hidden_room = Room("Hidden Vault", "A secret chamber untouched for centuries. Dust motes float in thin beams of light.")
    hidden_room.hidden = True # Could be used later for special logic
    
    #---- New for Quest #7: Dedicated shop room ----
    shop_room = Room("Merchant's Den", "Amysterious merchant has set up shop here, offering rare items for sale.")
    
    # Connections (progressive depth)
    entrance.connect("south", hall)
    hall.connect("north", entrance)
    hall.connect("east", armory)
    hall.connect("west", library)
    hall.connect("south", crypt)
    crypt.connect("north", hall)
    crypt.connect("south", treasure_room)
    treasure_room.connect("north", crypt)
    treasure_room.connect("south", lair)
    lair.connect("north", treasure_room)
    lair.connect("east", forge)
    forge.connect("west", lair)
    forge.connect("south", throne)
    throne.connect("north", forge)
    throne.connect("west", abyss)
    abyss.connect("east", throne)
    armory.connect("west", hall)
    library.connect("east", hall)
    library.connect("north", hidden_room)
    hidden_room.connect("south", library)
    shop_room.connect("west", entrance)
    
    #---- New for Quest #7: Return all roomsdictionary for save/load ----
    all_rooms = {
        "Dungeon Entrance": entrance,
        "Great Hall": hall,
        "Abandoned Armory": armory,
        "Forgotten Crypt": crypt,
        "Ancient Library": library,
        "Treasure Chamber": treasure_room,
        "Beast Laird": lair,
        "Cursed Forge": forge,
        "Fallen Throne Room": throne,
        "The Abyss": abyss,
        "Hidden Vault": hidden_room,
        "Merchant's Den": shop_room,
    }
    
    # Enemies (with quest # 4 style loot tables)
    scale = player_level * 1.2 # enemies get stronger as you level/time progresses
    
    hall.enemy = Enemy(
        "Goblin Scout", int(25 * scale), base_damage=6, xp_value=40,
        loot_table=[
            {"type": "gold", "chance": 0.85, "min": 5, "max": 25},
            {"type": "item", "item": "Goblin Ear", "chance": 0.5, "amount": 1,
             "data": {"attack":0, "defense": 0, "max_hp_bonus":0, "lore": "A trophy... or bait?"}}
        ]
    )
    
    armory.enemy = Enemy(
        "Animated Armor", int(40 * scale), base_damage=7, xp_value=60,
        loot_table=[
            {"type": "item", "item": "Rusted Gauntlets", "chance": 0.6, "amount": 1,
             "data": {"attack": 1, "defense":4, "max_hp_bonus":0, "lore": "Still faintly warm from battle."}},
            {"type": "gold", "chance": 0.7, "min": 10, "max": 50},
        ]
    )
    
    crypt.enemy = Enemy(
        "Skeletal Warrior", int(35 * scale), base_damage=8, xp_value=55,
        loot_table=[{"type": "item", "item": "Bone Shard", "chance": 0.4,
            "data": {"attack":2, "lore": "Sharp remnant."}},
            {"type": "gold", "chance": 0.9, "min": 20, "max": 50},        
        ]
    )
    
    lair.enenmy = Enemy(
        "Cave Troll", int(60 * scale), base_damage=10, xp_value=100,
        loot_table=[{"type": "item", "item": "Troll Hide", "chance": 0.3,
        "data": {"defense":6, "lore": "Thick and regenerative."}},
        {"type": "gold", "chance": 0.95, "min": 20, "max": 50},
        ]
    )
    
    forge.enemy = Enemy(
        "Fire Elemental", int(50 * scale), base_damage=9, xp_value=80,
        loot_table=[{"type": "item", "item": "Flame Essence", "chance": 0.5,
                     "data": {"spell_damage":15, "lore": "Burns eternally."}}
        ]
    )
    
    # Treasure (now uses same dict format as inventory data, More items)
    armory.treasure = {
        "Iron Sword": {
            "type": "weapon",
            "attack": 5, 
            "lore": "Strudy and sharp."
        },
        
        "Chainmail Vest": {
            "type": "armor",
            "defense": 5, 
            "lore": "Links of protection."
        }
    }
    
    library.treasure = {
        "Mana Potion": {
            "heal": 0 , 
            "spell_damage": 10, 
            "lore": "Restores magical energy"
        },
        
        "Scroll of Firebolt": {
            "spell_damage": 12, 
            "lore": "Unleash flames."
        }
    }
    
    treasure_room.treasure = {
        "Flamebrand Sword": {
            "type": "weapon",
            "attack": 10, 
            "defense": 0, 
            "max_hp_bonus": 0,
            "lore": "Forged in dwarven liquid fire, The blade hums with heat."
        },
        "ShadowSteel Armor": {
            "type": "armor",
            "attack": 0, 
            "defense": 15, 
            "max_hp_bonus": 0,
            "lore": "Tempered in darkness beneath forgotten mountains."
        },
        "Ring of vitality": {
            "type": "accessory",
            "attack": 0, 
            "defense": 0, 
            "max_hp_bonus": 20,
            "lore": "It pulses faintly with ancient life."
        },
        "Greater Health Potion:": {"heal": 40, "lore": "Potent restoration."}
    }
    
    hidden_room.treasure = {
        "Crown of the First King": {
            "type": "armor",
            "attack": 5, 
            "defense": 5, 
            "max_hp_bonus": 15,
            "lore": "Worn before history had ink. Power radiates from every gem."
        }
    }
    
    throne.treasure = {
        "Scepter of Command": {
            "type": "weapon",
            "attack": 8, 
            "max_hp_bonus": 10, 
            "lore": "Rules with authority."
        },
        
        "Elixer of Strength": {
            "heal": 50, 
            "lore": "Temporary? Full heal here."
        }
    }
    
    return entrance, all_rooms