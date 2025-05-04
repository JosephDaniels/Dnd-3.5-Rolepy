# constitution.py
import time

def evaluate_state(value, thresholds):
    for threshold, label in thresholds:
        if value >= threshold:
            return label
    return thresholds[-1][1]


class ConstitutionStatus:
    def __init__(self):
        self.hunger = 100
        self.thirst = 100
        self.stamina = 100
        self.bladder = 0

    def update_per_round(self):
        self.hunger = max(0, self.hunger - 5.0)
        self.thirst = max(0, self.thirst - 5.0)
        self.stamina = max(0, self.stamina - 0.2)
        self.bladder = min(100, self.bladder + 1.5)

    def eat(self, amount):
        self.hunger = min(100, self.hunger + amount)
        print(f"Ate food. Hunger is now {self.hunger:.1f}.")

    def drink(self, amount):
        self.thirst = min(100, self.thirst + amount)
        self.bladder = min(100, self.bladder + amount * 0.5)
        print(f"Drank water. Thirst is now {self.thirst:.1f}.")

    def rest(self, amount=10):
        self.stamina = min(100, self.stamina + amount)
        print(f"Rested. Stamina is now {self.stamina:.1f}.")

    def exert(self, amount=10):
        self.stamina = max(0, self.stamina - amount)
        print(f"Exerted. Stamina is now {self.stamina:.1f}.")

    def hunger_state(self):
        thresholds = [
            (95, "Bloated"),
            (80, "Full"),
            (60, "Normal"),
            (40, "Peckish"),
            (25, "Hungry"),
            (0, "Very Hungry")
        ]
        return evaluate_state(self.hunger, thresholds)

    def thirst_state(self):
        thresholds = [
            (95, "Saturated"),
            (80, "Hydrated"),
            (60, "Normal"),
            (40, "Drying"),
            (25, "Thirsty"),
            (0, "Very Thirsty")
        ]
        return evaluate_state(self.thirst, thresholds)

    def bladder_state(self):
        thresholds = [
            (100, "Accident Imminent"),
            (85, "Desperate"),
            (60, "Urgent"),
            (30, "Full"),
            (10, "Fine"),
            (0, "Empty")
        ]
        return evaluate_state(self.bladder, thresholds)


def test_constitution_loop():
    in_game_seconds = 0
    c = ConstitutionStatus()
    journal = []
    round_counter = 0

    while True:
        round_counter += 1
        in_game_seconds += 6
        c.update_per_round()

        hours = (in_game_seconds // 3600) % 24
        minutes = (in_game_seconds % 3600) // 60
        seconds = in_game_seconds % 60
        print(f"--- Round {round_counter} (In-game Time {hours:02}:{minutes:02}:{seconds:02}) ---")
        print(f"Hunger: {c.hunger:.1f} ({c.hunger_state()})")
        print(f"Thirst: {c.thirst:.1f} ({c.thirst_state()})")
        print(f"Stamina: {c.stamina:.1f}")
        print(f"Bladder: {c.bladder:.1f} ({c.bladder_state()})")

        if c.hunger < 25:
            journal.append(f"[{hours:02}:{minutes:02}:{seconds:02}] Hunger was {c.hunger:.1f} ({c.hunger_state()}). Ate food.")
            c.eat(30)

        if c.thirst < 25:
            journal.append(f"[{hours:02}:{minutes:02}:{seconds:02}] Thirst was {c.thirst:.1f} ({c.thirst_state()}). Drank water.")
            c.drink(30)

        if c.bladder > 60:
            journal.append(f"[{hours:02}:{minutes:02}:{seconds:02}] Bladder was {c.bladder:.1f} ({c.bladder_state()}). Relieved self.")
            c.bladder = 0

        if c.stamina < 20:
            journal.append(f"[{hours:02}:{minutes:02}:{seconds:02}] Stamina was low ({c.stamina:.1f}). Rested.")
            c.rest(15)

        time.sleep(1.0)

        if round_counter % 20 == 0:
            print("\n--- JOURNAL ---")
            for entry in journal:
                print(entry)
            print("--- END ---\n")


if __name__ == "__main__":
    test_constitution_loop()
