import os
import json
from datetime import date

SAVE_KEY_ABILITIES = {
    "base_fortitude": "constitution",
    "base_reflex": "dexterity",
    "base_will": "wisdom"
}


class Character:
    def __init__(self, name=""):
        self.name = name
        self.username = ""
        self.character_class = []

        # Profile info
        self.race = ""
        self.age = 0
        self.gender = ""
        self.eye_colour = ""
        self.hair_colour = ""
        self.skin_colour = ""
        self.height = ""
        self.weight = ""
        self.favorite_weapon = ""
        self.description = ""
        self.public_history = ""
        self.profile_image = None

        # Game stats
        self.strength = 10
        self.dexterity = 10
        self.constitution = 10
        self.intelligence = 10
        self.wisdom = 10
        self.charisma = 10

        self.maximum_health = 10
        self.current_health = 10
        self.armor_class = 10
        self.base_attack_bonus = 0
        self.initiative = 0
        self.xp_points = 0

        self.base_fortitude = 0
        self.base_reflex = 0
        self.base_will = 0

        self.platinum_coins = 0
        self.gold_coins = 0
        self.silver_coins = 0
        self.copper_coins = 0

        self.feats = []
        self.special_abilities = []
        self.inventory = {}

        self.dying = False
        self.dead = False
        self.date_created = str(date.today())
        self.date_modified = str(date.today())

    def get_status(self):
        if self.dying:
            state = "and you are currently dying."
        elif self.dead:
            state = "and you are currently dead."
        else:
            state = "and you are currently OK."
        return f"{self.name}'s current status: {self.current_health} / {self.maximum_health} HP, {state}"

    def get_full_profile(self):
        response = (
            f"Name: {self.name}\n"
            f"Race: {self.race}, Age: {self.age}, Gender: {self.gender}\n"
            f"Eyes: {self.eye_colour}, Hair: {self.hair_colour}, Skin: {self.skin_colour}\n"
            f"STR: {self.strength}, DEX: {self.dexterity}, CON: {self.constitution}\n"
            f"INT: {self.intelligence}, WIS: {self.wisdom}, CHA: {self.charisma}\n"
            f"HP: {self.current_health} / {self.maximum_health}, AC: {self.armor_class}\n"
            f"Weapon: {self.favorite_weapon}\n"
            f"Bio: {self.description}\n"
            f"History: {self.public_history}\n"
        )
        image_path = f"character_portraits/{self.profile_image}" if self.profile_image else None
        return response, image_path

    def save_to_json(self):
        path = f"characters/{self.name.lower()}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.__dict__, f, indent=4)
        print(f"Saved character to {path}")

    @classmethod
    def from_json(cls, filename):
        path = f"characters/{filename}"
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} not found.")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        char = cls()
        char.__dict__.update(data)
        return char

    @classmethod
    def from_txt_file(cls, filename):
        char = cls()
        txt_path = f"characters/{filename}"
        if not os.path.exists(txt_path):
            raise FileNotFoundError(f"{txt_path} not found.")

        with open(txt_path, encoding="latin-1") as f:
            lines = f.readlines()

        for line in lines:
            if "=" not in line:
                continue
            key, value = line.strip().split("=", 1)
            key = key.strip()
            value = value.strip()

            if key == "character_class":
                value = value.strip("[]").split(",")
                value = [v.strip() for v in value if v.strip()]
            else:
                try:
                    value = int(value)
                except ValueError:
                    pass

            setattr(char, key, value)

        char.date_modified = str(date.today())
        return char
