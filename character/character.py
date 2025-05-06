import os
import json
import csv
from datetime import date, datetime
from character.identity import CharacterIdentity

class Character:
    def __init__(self, name=""):
        self.name = name
        self.identity = CharacterIdentity()

        self.classes = {}  # e.g., {"Barbarian": 2, "Rogue": 1}
        self.class_progressions = {}  # e.g., {"Barbarian": [...], "Rogue": [...]}
        self.character_class = []  # for UI compatibility

        self.strength = -1
        self.dexterity = -1
        self.constitution = -1
        self.intelligence = -1
        self.wisdom = -1
        self.charisma = -1

        self.constitution_status = None
        self.mental_status = None

        self.inventory = None
        self.body_slots = {
            "eyes": [], "face": [], "hat": [], "neck": [], "shoulders": [], "chest": [],
            "upper_undergarment": [], "top": [], "arms": [], "left_wrist": [], "right_wrist": [],
            "left_hand": [], "right_hand": [], "midsection": [], "waist": [],
            "bottoms": [], "crotch": [], "left_thigh": [], "right_thigh": [],
            "knees": [], "left_ankle": [], "right_ankle": [], "left_foot": [], "right_foot": [],
            "rings": [], "piercings": []
        }

        self.feats = []
        self.special_abilities = []
        self.xp = 0
        self.ruleset = "3.5e"

        self.date_created = str(date.today())
        self.date_modified = str(date.today())

    def total_level(self):
        return sum(self.classes.values())

    def get_status(self):
        return (
            f"Level {self.total_level()} | "
            f"STR {self.strength}, DEX {self.dexterity}, CON {self.constitution}, "
            f"INT {self.intelligence}, WIS {self.wisdom}, CHA {self.charisma}"
        )

    def load_class_progression(self, class_name, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Class progression file not found: {filepath}")

        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.class_progressions[class_name] = []
            for row in reader:
                self.class_progressions[class_name].append({
                    "level": int(row["level"]),
                    "base_attack_bonus": row["base_attack_bonus"],
                    "fort": int(row["base_fortitude"]),
                    "ref": int(row["base_reflex"]),
                    "will": int(row["base_will"]),
                    "special": [s.strip() for s in row["special"].split(",")] if row["special"] else []
                })

    def add_class_level(self, class_name):
        if class_name not in self.class_progressions:
            raise ValueError(f"Progression data for class '{class_name}' not loaded.")

        current_level = self.classes.get(class_name, 0)
        class_table = self.class_progressions[class_name]

        if current_level >= len(class_table):
            print(f"⚠️ No more levels available in {class_name} progression.")
            return

        level_data = class_table[current_level]
        self.special_abilities.extend([s for s in level_data["special"] if s not in self.special_abilities])
        self.classes[class_name] = current_level + 1

        print(f"🎡️ {self.name} gained a level in {class_name} (now {self.classes[class_name]})")
        print(f"  → Gained: {', '.join(level_data['special'])}")

    def save_to_json(self):
        if not self.name:
            raise ValueError("Character must have a name before saving.")

        self.date_modified = datetime.now().isoformat()
        filename = self.name.lower().replace(" ", "_") + ".json"
        os.makedirs("characters", exist_ok=True)
        path = os.path.join("characters", filename)

        data = {
            "name": self.name,
            "identity": self.identity.to_dict(),
            "classes": self.classes,
            "strength": self.strength,
            "dexterity": self.dexterity,
            "constitution": self.constitution,
            "intelligence": self.intelligence,
            "wisdom": self.wisdom,
            "charisma": self.charisma,
            "constitution_status": self.constitution_status,
            "mental_status": self.mental_status,
            "inventory": self.inventory,
            "body_slots": self.body_slots,
            "feats": self.feats,
            "special_abilities": self.special_abilities,
            "xp": self.xp,
            "ruleset": self.ruleset,
            "date_created": self.date_created,
            "date_modified": self.date_modified
        }

        print("[DEBUG] Saving character with data:")
        for key, value in data.items():
            print(f"  {key}: {value}")

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print(f"Saved character to {path}")

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        char = cls()
        allowed_fields = set(char.__dict__.keys())

        for key, value in data.items():
            if key == "identity" and isinstance(value, dict):
                char.identity = CharacterIdentity.from_dict(value)
            elif key in allowed_fields:
                setattr(char, key, value)

        if not char.name:
            char.name = os.path.splitext(os.path.basename(filepath))[0].replace("_", " ").title()

        return char