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
        game_data = {
            "hydration_score": self.hydration_score,
            "monsters": self.monsters,
            "drink_history": self.drink_history,
            "current_monster_type": self.current_monster_type
        }

        try:
            with open(SAVE_FILE, "wb") as f:
                pickle.dump(game_data, f)
        except Exception as e:
            print(f"Error saving game: {e}")

    def load_game(self):
        if not os.path.exists(SAVE_FILE):
            return
    
        try:
            with open(SAVE_FILE, "rb") as f:
                game_data = pickle.load(f)

            self.hydration_score = game_data.get("hydration_score", 0)
            self.monsters = game_data.get("monsters", {})
            self.drink_history = game_data.get("drink_history", [])
            self.current_monster_type = game_data.get("current_monster_type", "blob")
        except Exception as e:
            print(f"Error loading game: {e}")

    def display_current_monster(self):
        monster_type = self.current_monster_type
        stage = 0

        if monster_type in self.monsters:
            stage = self.monsters[monster_type] - 1
            if stage < 0:
                stage = 0

        if monster_type in MONSTER_TYPES and stage < len(MONSTER_STAGES):
            ascii_art = MONSTER_STAGES[stage].get(monster_type, "")
            print(ascii_art)
            print(f"Monster type: {monster_type.title()}")
            print(f"Evolution stage: {stage + 1}/3")
        else:
            print("No monster selected or invalid monster type.")

    def display_monster_collection(self):
        if not self.monsters:
            print("Your collection is empty. Drink more water!")
            return
        
        print("\n===== MONSTER COLLECTION =====")
        for monster_type, stage in self.monsters.items():
            print(f"{monster_type.title()}: Evolution stage {stage}/3")

    def change_monster(self):
        clear_screen()
        print("===== SELECT MONSTER =====")

        available_types = list(MONSTER_TYPES)
        for i, monster_type in enumerate(available_types, 1):
            evolution = self.monsters.get(monster_type, 0)
            status = "Unlocked" if evolution > 0 else "Locked"
            print(f"{i}. {monster_type.title()} [{status}]")

        print("\nEnter the number of the monster you want to select (or 0 to cancel):")
        try:
            choice = int(input("> "))
            if 1 <= choice <= len(available_types):
                selected_type = available_types[choice - 1]

                if self.monsters.get(selected_type, 0) > 0:
                    self.current_monster_type = selected_type
                    print(f"\nYou selected: {selected_type.title()}")
                else:
                    print("\nThat monster is locked! Drink more to unlock it.")

            elif choice != 0:
                print("\nInvalid selection.")
            
        except ValueError:
            print("\nPlease enter a valid number.")
        
        input("\nPress Enter to continue...")

    def display_stats(self):
        print(f"\nTotal hydration score: {self.hydration_score:.lf}")
        print(f"Freaks collected: {sum(1 for v in self.monsters.values() if v > 0)}/{len(MONSTER_TYPES)}")

        next_threshold = None
        for threshold in [100, 300, 500]:
            if self.hydration_score < threshold:
                next_threshold = threshold
                break

        if next_threshold:
            points_needed = next_threshold - self.hydration_score
            print(f"Points to next evolution: {points_needed:.lf}")
        else:
            print("All evolutions complete for current monster!")

    def add_drink_menu(self):
        clear_screen()
        print("===== ADD HYDRATION =====")
        print("1. Water (1.0x points)")
        print("2. Soda (0.5x points)")
        print("3. Coffee (0.3x points)")
        print("0. Cancel")

        try:
            choice = int(input("\nSelect drink type: "))

            if choice == 0:
                return
            
            if 1 <= choice <= 3:
                drink_types = ["water", "soda", "coffee"]
                selected_drink = drink_types[choice - 1]

                amount = float(input(f"\nEnter amount in milliliters (ml): "))
                if amount <= 0:
                    print(f"How do you consume negative {selected_drink}?")
                    time.sleep(1.5)
                    return

                self.add_drink(selected_drink, amount)
                print(f"\nAdded {amount}ml of {selected_drink}!")

                if self.check_evolution():
                    print(f"Your freak just evolved!!!")
                    self.display_current_monster()
            else:
                print("\nInvalid selection.")

        except ValueError:
            print("\nPlease enter valid numbers.")

        input("\nPress Enter to continue...")

    def view_history(self):
        clear_screen()
        print("====== DRINK HISTORY ======")

        if not self.drink_history:
            print("No drink recorded yet.")
            input("\nPress Enter to continue...")
            return
        
        for i, entry in enumerate(reversed(self.drink_history[-10:]), 1):
            print(f"{i}. {entry['date']}: {entry['amount']}ml of {entry['type']} (+{entry['points']:.lf} pts)")

        if len(self.drink_history) > 10:
            print(f"\n...and {len(self.drink_history) - 10} more entries.")

        input(f"\nPress Enter to continue...")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def main():
    game = HydroFreaks()

    while True:
        clear_screen()
        print("===============================")
        print("     H Y D R O  F R E A K S    ")
        print("===============================")

        game.display_current_monster()
        game.display_stats()

        print("\n===== MENU =====")
        print("1. Add drink")
        print("2. View the collection of freaks")
        print("3. Change active freak")
        print("4. View drink history")
        print("0. Exit")

        try:
            choice = int(input("\nSelect option: "))

            if choice == 0:
                print("\nThanks for playing, stay hydrated!")
                break
            elif choice == 1:
                game.add_drink_menu()
            elif choice == 2:
                clear_screen()
                game.display_monster_collection()
                input("\nPress Enter to continue...")
            elif choice == 3:
                game.change_monster()
            elif choice == 4:
                game.view_history()
            else:
                print("\nInvalid option.")
                time.sleep(1)

        except ValueError:
            print("\nPlease enter a valid number.")
            time.sleep(1)

if __name__ == "__main__":
    main()