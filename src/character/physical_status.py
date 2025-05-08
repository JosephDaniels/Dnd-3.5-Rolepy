import time


def evaluate_state(value, thresholds):
    for threshold, label in thresholds:
        if value >= threshold:
            return label
    return thresholds[-1][1]


class PhysicalStatus:
    def __init__(self):
        self.max_health = 100.0
        self.current_health = self.max_health
        self.temp_health = 0.0
        self.nonlethal_damage = 0.0
        self.hunger = 100.0
        self.thirst = 100.0
        self.stamina = 100.0
        self.bladder = 0.0
        self.sleep = 100.0
        self.libido = 50.0

    def update_per_round(self):
        self.hunger = max(0.0, self.hunger - 5.0)
        self.thirst = max(0.0, self.thirst - 5.0)
        self.stamina = max(0.0, self.stamina - 0.2)
        self.bladder = min(100.0, self.bladder + 1.5)
        self.sleep = max(0.0, self.sleep - 0.05)
        self.libido = min(100.0, self.libido + 0.01)

    def eat(self, amount: float):
        self.hunger = min(100.0, self.hunger + amount)
        print(f"Ate food. Hunger is now {self.hunger:.1f}.")

    def drink(self, amount: float):
        self.thirst = min(100.0, self.thirst + amount)
        self.bladder = min(100.0, self.bladder + amount * 0.5)
        print(f"Drank water. Thirst is now {self.thirst:.1f}.")

    def rest(self, amount: float = 10.0):
        self.stamina = min(100.0, self.stamina + amount)
        print(f"Rested. Stamina is now {self.stamina:.1f}.")

    def exert(self, amount: float = 10.0):
        self.stamina = max(0.0, self.stamina - amount)
        print(f"Exerted. Stamina is now {self.stamina:.1f}.")

    def add_temp_hp(self, amount: float):
        self.temp_health = max(self.temp_health, amount)
        print(f"Gained {amount:.1f} temporary HP. Temp HP is now {self.temp_health:.1f}.")

    def take_damage(self, amount: float, lethal: bool = True):
        remaining = amount
        if self.temp_health > 0:
            used = min(self.temp_health, remaining)
            self.temp_health -= used
            remaining -= used
            print(f"Absorbed {used:.1f} damage with Temp HP. Temp HP is now {self.temp_health:.1f}.")
        if remaining > 0:
            if lethal:
                self.current_health = max(0.0, self.current_health - remaining)
                print(f"Took {remaining:.1f} damage. Health is now {self.current_health:.1f}/{self.max_health:.1f}.")
            else:
                self.nonlethal_damage = min(self.current_health, self.nonlethal_damage + remaining)
                print(f"Took {remaining:.1f} non-lethal damage. Subdual damage is now {self.nonlethal_damage:.1f}.")

    def heal(self, amount: float):
        self.current_health = min(self.max_health, self.current_health + amount)
        print(f"Healed {amount:.1f}. Health is now {self.current_health:.1f}/{self.max_health:.1f}.")

    def reset_subdual(self):
        self.nonlethal_damage = 0.0
        print("Subdual damage reset.")

    def hunger_state(self) -> str:
        thresholds = [
            (95.0, "Bloated"),
            (80.0, "Full"),
            (60.0, "Normal"),
            (40.0, "Peckish"),
            (25.0, "Hungry"),
            (0.0, "Very Hungry")
        ]
        return evaluate_state(self.hunger, thresholds)

    def thirst_state(self) -> str:
        thresholds = [
            (95.0, "Saturated"),
            (80.0, "Hydrated"),
            (60.0, "Normal"),
            (40.0, "Drying"),
            (25.0, "Thirsty"),
            (0.0, "Very Thirsty")
        ]
        return evaluate_state(self.thirst, thresholds)

    def bladder_state(self) -> str:
        thresholds = [
            (100.0, "Accident Imminent"),
            (85.0, "Desperate"),
            (60.0, "Urgent"),
            (30.0, "Full"),
            (10.0, "Fine"),
            (0.0, "Empty")
        ]
        return evaluate_state(self.bladder, thresholds)

    def sleep_state(self) -> str:
        thresholds = [
            (95.0, "Fully Rested"),
            (75.0, "Rested"),
            (50.0, "Okay"),
            (30.0, "Tired"),
            (10.0, "Exhausted"),
            (0.0, "Passing Out")
        ]
        return evaluate_state(self.sleep, thresholds)

    def libido_state(self) -> str:
        thresholds = [
            (95.0, "Overflowing"),
            (75.0, "Riled Up"),
            (50.0, "Interested"),
            (30.0, "Apathetic"),
            (10.0, "Indifferent"),
            (0.0, "Suppressed")
        ]
        return evaluate_state(self.libido, thresholds)

# Note: test loops and CSV imports removed for clarity