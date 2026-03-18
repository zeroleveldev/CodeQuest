from shadow_vault import ShadowVault

def main():
    print("=== QUEST #2 : THE SHADOW VAULT === ")
    
    vault = ShadowVault(min_code=1, max_code=10, max_attempts=5)
    unlock = vault.play()
    
    if unlock:
        print("\nYou may proceed deeper into the dungeon!")
    else:
        print("\nYour journey ends here for now.")

if __name__ == "__main__":
    main()