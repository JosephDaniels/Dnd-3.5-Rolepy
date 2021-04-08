import random
import time

random.seed(time.time)

from constant import *


class Character(object):
    """Character is the base class for any character that exists in the game world
        The primary attributes are:
        .strength
        .dexterity
        .constitution
        .intelligence
        .wisdom
        .charisma
        .max_hp
        .curr_hp
        .armor_class"""
    
    def __init__(self):

        #####CHARACTER ATTRIBUTES####
        self._strength = 0
        self._dexterity = 0
        self._constitution = 0
        self._intelligence = 0
        self._wisdom = 0
        self._charisma = 0
        
        ####Character Hitpoints, attack and armor####
        self.max_hp = 0
        self.curr_hp = 0
        self.attack_bonus = 0
        self.armor_class = 10
        
        ####Character Header####
        self.name = "" ##
        self.player = "" ##Name of the IRL person who owns/plays the character.
        self.charclass = None ##Class type object
        self.race = None ##Race type object
        self.alignment = None ##Personality type object
        
        ####Details####
        self.height = 0 ## A tuple of feet and inches
        self.weight = 0 ##Weight in pounds.
        self.age = 0 ##Age in years
        self.gender = "" ##Male or Female.
        self.eye_color = ""
        self.hair_color = ""
        self.skin_color = ""
        
        ####Character Score####
        self.experience = 0
        self.exp_bonus = 1000
        self.level = 1
        
        ####Character Stuff####
        self.inventory = Inventory()
        self.gold = 0

    def get_attribute_modifier(self, value):
        if value%2 == 1: ## Test if the attribute divides nicely
            value = value-1 ## If not, remove one to make it even
        elif value%2 == 0:
            pass
        modifier = int((value-10)*0.5)
        return modifier

    def classic_dnd_attribute_roll(self):
        ##Rolls 4d6 and removes the lowest one, spitting out a total of the remainder.
        pass

    def net_melee_bonus(self):
        "calcs the total amount of modifier applied on a single melee attack from attack bonus, spells, and weapon bonuses"
        total = self.attack_bonus + self.inventory.melee_bonus + self.get_modifier(self.strength) ##ADD IN SPELL MODIFIER LATER
        return total
        
    def dump(self):
        for k in self.__dict__.keys():
            print k, self.__dict__[k]

if __name__ == "__main__":
    c = Character()
    
