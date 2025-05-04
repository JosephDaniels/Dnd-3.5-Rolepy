from character import Character
from inventory import Inventory
from equipment import Item, Weapon

class GameData:
    def __init__(self):
        self.character = None
        self.inventory = None

    def load_character(self, name):
        self.character = Character.load(name)
        self.inventory = Inventory(self.character)

    def save_all(self):
        self.character.save()
        self.inventory.save()
