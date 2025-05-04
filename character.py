import os
import json
from datetime import date

class Character:
    LAYER_LABELS = {
        0: "nude",
        1: "underwear",
        2: "clothing",
        3: "armor"
    }

    def __init__(self, name=""):
        self.name = name
        self.username = ""
        self.alignment = None
        self.character_class = []

        # Profile info
        self.race = ""
        self.age = -1
        self.gender = ""
        self.eye_colour = ""
        self.hair_colour = ""
        self.skin_colour = ""
        self.height = ""
        self.weight = ""
        self.favorite_weapon = None
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

        self.body_slots = {
            "eyes": [], "face": [], "hat": [], "neck": [], "shoulders": [], "chest": [],
            "upper_undergarment": [], "top": [], "arms": [], "left_wrist": [], "right_wrist": [],
            "left_hand": [], "right_hand": [], "midsection": [], "waist": [],
            "lower_undergarment": [], "bottoms": [], "crotch": [], "left_thigh": [], "right_thigh": [],
            "knees": [], "left_ankle": [], "right_ankle": [], "left_foot": [], "right_foot": [],
            "rings": [], "piercings": []
        }

    def equip_item(self, slot, item_name, layer, description="", weight=0):
        if slot not in self.body_slots:
            raise ValueError(f"Invalid slot: {slot}")
        item_entry = {"item": item_name, "layer": layer, "description": description, "weight": weight}
        self.body_slots[slot].append(item_entry)
        self.body_slots[slot].sort(key=lambda x: x.get("layer", 0))
        self.remove_item_from_inventory(item_name)
        self.date_modified = str(date.today())

    def unequip_item(self, slot):
        if slot in self.body_slots and self.body_slots[slot]:
            removed = self.body_slots[slot].pop()
            item_name = removed.get("item")
            if item_name:
                self.add_item_to_inventory(item_name)
        self.date_modified = str(date.today())

    def add_item_to_inventory(self, item_name, quantity=1):
        val = self.inventory.get(item_name, 0)
        if isinstance(val, list) and len(val) == 2 and isinstance(val[1], int):
            val = val[1]
        self.inventory[item_name] = val + quantity

    def remove_all_gear(self):
        for slot in self.body_slots:
            while self.body_slots[slot]:
                self.unequip_item(slot)
        self.date_modified = str(date.today())

    def remove_item_from_inventory(self, item_name):
        if item_name in self.inventory:
            if isinstance(self.inventory[item_name], list) and len(self.inventory[item_name]) == 2:
                quantity = self.inventory[item_name][1]
            else:
                quantity = self.inventory[item_name]

            if quantity > 1:
                self.inventory[item_name] = quantity - 1
            else:
                del self.inventory[item_name]

    def get_inventory_weight(self):
        total_weight = 0.0
        for item_name, quantity in self.inventory.items():
            if isinstance(quantity, list):
                quantity = quantity[1]
            item_weight = 1.0
            total_weight += item_weight * quantity
        return total_weight

    def get_status(self):
        state = "and you are currently OK."
        if self.dying:
            state = "and you are currently dying."
        elif self.dead:
            state = "and you are currently dead."
        return f"{self.name}'s current status: {self.current_health} / {self.maximum_health} HP, {state}"

    def get_equipped_gear(self):
        output = f"{self.name}'s Equipped Gear:\n"
        for slot, items in self.body_slots.items():
            if items:
                top_item = items[-1]
                output += f"{slot.replace('_', ' ').title()}: {top_item['item']}\n"
        return output

    def get_full_profile(self):
        response = (
            f"Name: {self.name}\n"
            f"Race: {self.race}, Age: {self.age}, Gender: {self.gender}, Alignment: {self.alignment}\n"
            f"Eyes: {self.eye_colour}, Hair: {self.hair_colour}, Skin: {self.skin_colour}\n"
            f"STR: {self.strength}, DEX: {self.dexterity}, CON: {self.constitution}\n"
            f"INT: {self.intelligence}, WIS: {self.wisdom}, CHA: {self.charisma}\n"
            f"HP: {self.current_health} / {self.maximum_health}, AC: {self.armor_class}\n"
            f"Weapon: {self.favorite_weapon or 'None'}\n"
            f"Bio: {self.description}\n"
            f"History: {self.public_history}\n"
        )
        image_path = f"character_portraits/{self.profile_image}" if self.profile_image else None
        return response, image_path

    def save_to_json(self):
        if not self.name:
            raise ValueError("Character must have a name before saving.")
        path = f"characters/{self.name.lower()}.json"
        data = self.__dict__.copy()

        clean_inventory = {}
        for k, v in self.inventory.items():
            if isinstance(v, int):
                clean_inventory[k] = v
            elif isinstance(v, list) and len(v) == 2 and isinstance(v[1], int):
                clean_inventory[k] = v[1]
        data["inventory"] = clean_inventory

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"Saved character to {path}")

    @classmethod
    def from_json(cls, filename):
        path = f"characters/{filename}"
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} not found.")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "name" not in data or not data["name"]:
            raise ValueError(f"Character data is missing a valid 'name' field: {filename}")

        char = cls()
        for key, value in data.items():
            if key == "inventory":
                cleaned_inventory = {}
                for item_name, item_val in value.items():
                    if isinstance(item_val, int):
                        cleaned_inventory[item_name] = item_val
                    elif isinstance(item_val, list):
                        try:
                            cleaned_inventory[item_name] = int(item_val[-1])
                        except (ValueError, IndexError):
                            cleaned_inventory[item_name] = 1
                setattr(char, key, cleaned_inventory)
            elif hasattr(char, key):
                setattr(char, key, value)
        return char
