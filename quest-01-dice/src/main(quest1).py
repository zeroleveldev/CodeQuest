import random
import time
import os
from assets.ascii_art import DICE_FACES, LOGO, DIVIDER

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
    
def get_user_settings():
    dice_count = int(input("How many dice? "))
    sides = int(input("How many sides per die? "))
    modifier = int(input("Modifier (0 if none): "))
    
    return dice_count, sides, modifier

def roll_dice(count: int, sides: int) -> list[int]:
    return [random.randint(1, sides) for _ in range(count)]

def display_dice(rolls: list[int]) -> None:
    for roll in rolls:
        if roll in DICE_FACES:
            for line in DICE_FACES[roll]:
                print(line)
            print()
        else:
            print("+-------+")
            print(f"| {roll: ^3}   |")
            print("|       |")
            print("|       |")
            print("+-------+")
            print()

def rolling_animation():
    for _ in range(3):
        print("Rolling the ancient dice...")
        time.sleep(0.4)
        clear_screen()

def get_prophecy(total: int, max_possible) -> str:
    ratio = total / max_possible
    
    if ratio >= 0.9:
        return "LEGENDARY FATE! God Himself whisper your name."
    elif ratio >= 0.7:
        return "Great treasure awaits you!"
    elif ratio >= 0.4:
        return "Fortune smiles upon your path."
    else:
        return "Dark omens stir in the shadows."

def main():
    clear_screen()
    print(LOGO)
    
    dice_count, sides, modifier = get_user_settings()
    
    rolling_animation()
    rolls = roll_dice(dice_count, sides)
    
    clear_screen()
    print(DIVIDER)
    
    display_dice(rolls)
    
    total = sum(rolls) + modifier
    max_possible = (dice_count * sides) + modifier
    
    if sides == 20 and 20 in rolls:
        print()
        print("⚔️  NATURAL 20! CRITICAL SUCCESS! ⚔️")
    
    print(DIVIDER)
    print(f"Rolls: {rolls}")
    print(f"Modifier: {modifier}")
    print(f"Total: {total}")
    print()
    print(get_prophecy(total, max_possible))
    
if __name__ == "__main__":
    main()