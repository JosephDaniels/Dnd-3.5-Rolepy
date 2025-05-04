import os
import json
import csv
from datetime import date

# Equipment logic: blueprints, item types, and CSV table references

TABLES = {
    "food": "dnd35_food_table.csv",
    "improvised": "dnd35_improvised_weapon_table.csv",
    "armor": "dnd35srd_armour_table.csv",
    "clothing": "dnd35srd_clothing_table.csv",
    "hardness": "dnd35srd_item_hardness_table.csv",
    "mundane": "dnd35srd_mundane_items_table.csv",
    "weapon_hardness": "dnd35srd_weapon_and_shield_hardness_table.csv",
    "substance_hardness": "dnd35srd+_substance_hardness_table.csv"
}

def load_csv_items(filename):
    filepath = os.path.join("dnd_tables", filename)
    with open(filepath, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

class Item:
    def __init__(self, name, type="generic", weight=1.0, equip_slot=None, description=""):
        self.name = name
        self.type = type
        self.weight = weight
        self.equip_slot = equip_slot
        self.description = description

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "weight": self.weight,
            "equip_slot": self.equip_slot,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            type=data.get("type", "generic"),
            weight=data.get("weight", 1.0),
            equip_slot=data.get("equip_slot"),
            description=data.get("description", "")
        )

class Weapon(Item):
    def __init__(self, name, damage="1d6", enhancement_bonus=0, **kwargs):
        super().__init__(name, type="weapon", **kwargs)
        self.damage = damage
        self.enhancement_bonus = enhancement_bonus

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "damage": self.damage,
            "enhancement_bonus": self.enhancement_bonus
        })
        return base

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            damage=data.get("damage", "1d6"),
            enhancement_bonus=data.get("enhancement_bonus", 0),
            weight=data.get("weight", 1.0),
            equip_slot=data.get("equip_slot"),
            description=data.get("description", "")
        )

class Armor(Item):
    def __init__(self, name, ac_bonus=0, check_penalty=0, **kwargs):
        super().__init__(name, type="armor", **kwargs)
        self.ac_bonus = ac_bonus
        self.check_penalty = check_penalty

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "ac_bonus": self.ac_bonus,
            "check_penalty": self.check_penalty
        })
        return base

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            ac_bonus=data.get("ac_bonus", 0),
            check_penalty=data.get("check_penalty", 0),
            weight=data.get("weight", 1.0),
            equip_slot=data.get("equip_slot"),
            description=data.get("description", "")
        )

class Consumable(Item):
    def __init__(self, name, effects=None, uses=1, **kwargs):
        super().__init__(name, type="consumable", **kwargs)
        self.effects = effects if effects else []
        self.uses = uses

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "effects": self.effects,
            "uses": self.uses
        })
        return base

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            effects=data.get("effects", []),
            uses=data.get("uses", 1),
            weight=data.get("weight", 0.1),
            equip_slot=data.get("equip_slot"),
            description=data.get("description", "")
        )
