import os
import random
import json
from datetime import datetime
from src.character.charactersheet import CharacterSheet
from src.character.physical_status import PhysicalStatus
from src.character.mental_status import MentalStatus
from src.games.rolepy_dice import rolld

class NPC(CharacterSheet):
    def __init__(self, npc_type: str = None):
        # Initialize base character sheet
        super().__init__(name=npc_type or "NPC")
        # Replace stats with embedded status objects
        self.physical_status = PhysicalStatus()
        self.mental_status = MentalStatus()
        # Remove unused attributes from CharacterIdentity
        # (assuming identity loaded separately if needed)
        # Load NPC data from JSON if exists
        if npc_type:
            path = f"npc/{npc_type.lower()}.json"
            if os.path.exists(path):
                data = json.load(open(path, 'r', encoding='utf-8'))
                # Merge relevant fields
                for key, val in data.items():
                    if hasattr(self, key):
                        setattr(self, key, val)

    def update_status(self):
        # Simulate per-round decay/growth
        self.physical_status.update_per_round()
        self.mental_status.update_per_tick()

    def decide_action(self):
        ps = self.physical_status
        ms = self.mental_status
        # Prioritize basic needs
        if ps.hunger < 30:
            return self.eat()
        if ps.thirst < 30:
            return self.drink()
        if ps.stamina < 30:
            return self.rest()
        if ms.social < 30:
            return self.socialize()
        # Otherwise random work or wander
        return random.choice([self.work, self.wander])()

    def eat(self):
        amt = random.uniform(20, 40)
        self.physical_status.eat(amt)
        return f"{self.name} eats and restores {amt:.1f} hunger."

    def drink(self):
        amt = random.uniform(20, 40)
        self.physical_status.drink(amt)
        return f"{self.name} drinks and restores {amt:.1f} thirst."

    def rest(self):
        amt = random.uniform(20, 50)
        self.physical_status.rest(amt)
        return f"{self.name} rests and recovers {amt:.1f} stamina."

    def socialize(self):
        amt = random.uniform(20, 40)
        self.mental_status.social = min(100, self.mental_status.social + amt)
        return f"{self.name} socializes and gains {amt:.1f} social."

    def work(self):
        cost = random.uniform(5, 15)
        self.physical_status.exert(cost)
        return f"{self.name} works and uses {cost:.1f} stamina."

    def wander(self):
        move_cost = random.uniform(1, 5)
        self.physical_status.exert(move_cost)
        return f"{self.name} wanders around using {move_cost:.1f} stamina."

    def log_journal(self, message: str):
        if not hasattr(self, 'journal'):
            self.journal = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.journal.append(f"[{timestamp}] {self.name} {message}")
        # Persist to file
        self.save_to_json()

    def save_to_json(self):
        # Extend CharacterSheet save to include journal and statuses
        data = self.__dict__.copy()
        data['physical_status'] = self.physical_status.__dict__
        data['mental_status'] = self.mental_status.__dict__
        with open(f"npc/{self.name.lower()}.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def __str__(self):
        return f"NPC<{self.name}> - HP: {self.physical_status.current_health:.1f}/{self.physical_status.max_health:.1f}, Mood: {self.mental_status.overall_mood()}"

# Example batch creation
if __name__ == '__main__':
    count = rolld(6) + rolld(6)
    npcs = [NPC('goblin') for _ in range(count)]
    for npc in npcs:
        print(npc)
        action = npc.decide_action()
        print(action)
