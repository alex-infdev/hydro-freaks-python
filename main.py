import os
import pickle
import time
from datetime import datetime
from monsters import *

SAVE_FILE = "save.dat"

class HydroFreaks:
    def __init__(self):
        self.hydration_score = 0
        self.monsters = {}
        self.drink_history = []
        self.current_monster_type = "blob"
        self.load_game()
    
    def add_drink(self, drink_type, amount):
        multipliers = {
            "water": 1,
            "soda": 0.5,
            "coffee": 0.3
        }

        if drink_type not in multipliers:
            return False
        
        points = amount * multipliers[drink_type]
        self.hydration_score += points

        self.drink_history.append({
            "type": drink_type,
            "amount": amount,
            "points": points,
            "date": datetime.now().strftime("%Y-%m-%d $H:$M")
        })

        self.check_evolution()
        self.save_game()
        return True

def check_evolution(self):
    thresholds = [100, 300, 500]

    for threshold in thresholds:
        if self.hydration_score >= threshold:
            stage = next((i for i, t in enumerate(thresholds) if threshold == t), 0)

            if self.current_monster_type not in self.monsters:
                self.monsters[self.current_monster_type] = 0

            if self.monsters[self.current_monster_type] < stage + 1:
                self.monsters[self.current_monster_type] = stage + 1
                return True
            
def save_game(self):
    pass

def load_game(self):
    pass

def display_current_monster(self):
    pass

def display_monster_collection(self):
    pass

def change_monster(self):
    pass

def display_stats(self):
    pass

def add_drink_menu(self):
    pass

def view_history(self):
    pass

def clear_screen():
    pass

def main():
    pass

if __name__ == "__main__":
    main()