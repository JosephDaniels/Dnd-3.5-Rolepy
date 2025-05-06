import os
import json
from datetime import datetime, date

class Character:
    def __init__(self, name=""):
        self.name = name
        self.race = ""
        self.character_class = []

        self.character_identity = {
            "age": -1, "gender": "", "eye_colour": "", "hair_colour": "",
            "skin_colour": "", "height": "", "weight": "", "build": ""
        }

        self.strength = 10
        self.dexterity = 10
        self.constitution = 10
        self.intelligence = 10
        self.wisdom = 10
        self.charisma = 10

        self.constitution_status = None
        self.mental_status = None
        self.inventory = {}
        self.body_slots = {slot: [] for slot in [
            "eyes", "face", "hat", "neck", "shoulders", "chest", "upper_undergarment",
            "top", "arms", "left_wrist", "right_wrist", "left_hand", "right_hand",
            "midsection", "waist", "bottoms", "crotch", "left_thigh", "right_thigh",
            "knees", "left_ankle", "right_ankle", "left_foot", "right_foot", "rings", "piercings"
        ]}

        self.description = ""
        self.public_history = ""
        self.private_history = ""

        self.description_file = ""
        self.public_history_file = ""
        self.private_history_file = ""

        self.date_created = str(date.today())
        self.date_modified = str(date.today())

    def save_to_json(self):
        self.date_modified = datetime.now().isoformat()
        filename = self.name.lower().replace(" ", "_") + ".json"
        os.makedirs("characters", exist_ok=True)
        path = os.path.join("characters", filename)

        self.description_file = self.description_file or filename.replace(".json", "_description.txt")
        self.public_history_file = self.public_history_file or filename.replace(".json", "_public.txt")
        self.private_history_file = self.private_history_file or filename.replace(".json", "_private.txt")

        data = self.__dict__.copy()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        self._write_text_file(self.description_file, self.description)
        self._write_text_file(self.public_history_file, self.public_history)
        self._write_text_file(self.private_history_file, self.private_history)

    def _write_text_file(self, filename, content):
        os.makedirs("characters/text", exist_ok=True)
        with open(os.path.join("characters/text", filename), "w", encoding="utf-8") as f:
            f.write(content)

    def _read_text_file(self, filename):
        path = os.path.join("characters/text", filename)
        return open(path, "r", encoding="utf-8").read() if os.path.exists(path) else ""

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        char = cls()
        for key, value in data.items():
            if key == "character_identity" and isinstance(value, dict):
                char.character_identity.update(value)
            elif hasattr(char, key):
                setattr(char, key, value)

        char.description = char._read_text_file(char.description_file)
        char.public_history = char._read_text_file(char.public_history_file)
        char.private_history = char._read_text_file(char.private_history_file)

        return char
