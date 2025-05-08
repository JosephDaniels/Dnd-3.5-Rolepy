import os
import json
import csv
from datetime import date, datetime
from src.character.identity import CharacterIdentity
from src.character.physical_status import PhysicalStatus
from src.character.mental_status import MentalStatus

class CharacterSheet:
    def __init__(self, name=""):
        self.name = name
        self.identity = CharacterIdentity()

        self.classes = {}

        self.strength = -1
        self.dexterity = -1
        self.constitution = -1
        self.intelligence = -1
        self.wisdom = -1
        self.charisma = -1

        self.physical_status = PhysicalStatus()
        self.mental_status = MentalStatus()

        self.inventory = {}
        self.equipment = {}

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

        self.hunger = 0
        self.thirst = 0

        self.journal = []

        self.position = {"x": 0, "y": 0}

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

        print(f"🍠 {self.name} gained a level in {class_name} (now {self.classes[class_name]})")
        print(f"  → Gained: {', '.join(level_data['special'])}")

    def save_to_json(self):
        if not self.name:
            raise ValueError("Character must have a name before saving.")

        self.date_modified = datetime.now().isoformat()
        filename = self.name.lower().replace(" ", "_") + ".json"
        os.makedirs("character_sheets", exist_ok=True)
        path = os.path.join("character_sheets", filename)

        data = self.__dict__.copy()
        data["identity"] = self.identity.to_dict()
        data["physical_status"] = self.physical_status.__dict__
        data["mental_status"] = self.mental_status.__dict__
        data["journal"] = self.journal

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print(f"Saved character to {path}")

    @classmethod
    def from_json(cls, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        data = cls.upgrade_schema(data)

        character = cls()
        for key, value in data.items():
            if key == "identity":
                continue
            elif key == "mental_status" and isinstance(value, dict):
                ms = MentalStatus()
                ms.__dict__.update(value)
                character.mental_status = ms
            elif key == "physical_status" and isinstance(value, dict):
                ps = PhysicalStatus()
                ps.__dict__.update(value)
                character.physical_status = ps
            elif key == "journal" and isinstance(value, list):
                character.journal = value
            else:
                setattr(character, key, value)
        if isinstance(data.get("identity"), dict):
            character.identity = CharacterIdentity.from_dict(data["identity"])

        return character

    @staticmethod
    def upgrade_schema(data):
        defaults = CharacterSheet().__dict__.copy()
        defaults.pop('identity')
        defaults.pop('physical_status')
        defaults.pop('mental_status')
        for key, value in defaults.items():
            if key not in data:
                data[key] = value
        if "journal" not in data:
            data["journal"] = []
        return data

if __name__ == "__main__":
    try:
        rynn = CharacterSheet.from_json("character_sheets/rynn_delon_dragonwhisper.json")
        rynn.save_to_json()
        print("✅ Rynn upgraded and saved.")
    except Exception as e:
        print(f"❌ Failed to upgrade: {e}")