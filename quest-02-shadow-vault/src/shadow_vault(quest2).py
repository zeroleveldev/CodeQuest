"""
Shadow Vault Module
Handles vault logic separately for easy reuse and intergration in larger projects.
"""

import random

class ShadowVault:
    def __init__(self, min_code=1, max_code=10, max_attempts=5):
        """
        Initialize the vault with a secret code and number of attempts.
        min_code and max_code define the range of numbers.
        max_attempts limits how many guesses the player can make.
        """
        
        self.min_code = min_code
        self.max_code = max_code
        self.max_attempts = max_attempts
        self.secret_code = random.randint(self.min_code, self.max_code)
    
    def check_guess(self, guess):
        """
        Compare the player's guess to the secret code.
        Returns "correct" if guessed right, "low" if too low, "high" if too high.
        """
        
        if guess == self.secret_code:
            return "Correct"
        elif guess < self.secret_code:
            return "Too low"
        else:
            return "Too high"
    
    def play(self):
        """
        Play the vault puzzle interactively.
        Returns True if the vault is unlocked, False if the player fails.
        """
        
        print("\nYou approach the Shadow Vault. A strange energy hums from the door.")
        print(f"Guess the secret number between {self.min_code} and {self.max_code}.")
        print(f"You have {self.max_attempts} attempts to unlock it.")
        
        attempts_left = self.max_attempts
        
        while attempts_left > 0:
            try:
                guess = int(input("\nEnter your guess: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            
            result = self.check_guess(guess)
            
            if result == "Correct":
                print("\nThe vault shudders and slowly opens. You did it!")
                return True
            elif result == "Too low":
                print("Too low...")
            else:
                print("Too high...")
                
            attempts_left -= 1
            print(f"Attempts remaining: {attempts_left}")
            
        print("\nThe vault seals shut permanently. You have failed this challenge.")
        return False