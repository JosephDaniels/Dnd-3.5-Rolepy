from constant import *

johnfile = "john.txt"
chaifile = "chailaine.txt"
testfile = "test.txt"

import random

class Charactersheet(object):
    
    """ A module to handle Dungeons and Dragons Version 3.5 Characters. """

    def __init__(self, character_file=None):
        
        if not character_file:
            print ("Character file not found.")
        else: ## Character file found
            data = self.load(character_file)
            self.__dict__.update(data)
            for key in self.__dict__.keys():
                if key in TITLE_INFO or key in CHARACTER_DETAILS: ## These are all strings
                    print (key+" was loaded succesfully.")
                    self.__dict__[key] = str(self.__dict__[key])
                elif key in ATTRIBUTES or key in STATS: ## These are all integers
                    print (key+" was loaded succesfully.")
                    self.__dict__[key] = int(self.__dict__[key])
                else:
                    print ("attempted to load "+key+ " but failed.")
                    
        self.weapon_righthand = {}
        self.weapon_lefthand = {}
        self.inventory = []
        self.alive = True
        self.level = 1
        self.next_level_exp_requirement = 1000
        self.exp_bonus_increment = 1000
        self.calc_level()

    # example of using a property declaration
    # in usage it looks like a regular property, but it's really calculated
    def _initiative_getter(self):
        return self.calc_modifier(self.dexterity)

    initiative = property(_initiative_getter, None)

        
    def calc_modifier(self, attribute):
        if attribute%2 == 1: ## Test if the attribute divides nicely
            attribute = attribute-1 ## If not, remove one to make it even
        modifier = int((attribute-10)*0.5)
        return modifier

    def valid_input(self, expected_list):
        text = raw_input()
        if text in expected_list:
            return text
        if text not in expected_list:
            print ("Invalid entry. Going to default value.")
            pass

    def introduction(self):
        print ("Hello New Adventurer! Let's create a new character for you.")
        while True:
            print ("What is your name, Adventurer?")
            self.name = raw_input()
            print ("What is your race, %s? You can choose from %s" % (self.name, DND_RACES.keys()))
            self.race = self.valid_input(DND_RACES.keys())
            print ("The race you've selected %s, is... %s" % (self.race, DND_RACES[self.race]))
            print ("What is your class, %s? You can choose from %s" % (self.name, DND_CLASSES.keys()))
            self.charclass = self.valid_input(DND_CLASSES.keys())
            print ('%s is a %s who is a %s good at %s!' % (self.name, self.race, self.charclass, DND_CLASSES[self.charclass]))
            print ('Is this correct? y/n')
            text = raw_input()
            if text == "y":
                break
            if text == "n":
                continue
            
    def clone_attribs_from(self, profile):
        """ copy atrributes from the profile into our class """
        attribs = ["name", "experience", "strength", "dexterity", "constitution"]
        for key in attribs:
            self.__dict__[key] = profile.__dict__.get(key)

    def add_experience(self, value):
        self.experience+=int(value)
        self.try_lvl_up()

    def try_lvl_up(self):
        if self.experience >= self.next_level_exp_requirement: ## Try to level once
            print ("You've Leveled Up!") 
            self.level+=1
            self.exp_bonus_increment = self.exp_bonus_increment+1000
            self.next_level_exp_requirement += self.exp_bonus_increment
        else:
            left = self.next_level_exp_requirement-self.experience
            print ("You have %i experience points and need %i more experience points to become stronger." % (self.experience,left))

    def calc_level(self, debug=False):
        while True: ## Keep leveling up until at the correct current level
            if self.experience >= self.next_level_exp_requirement:
                self.level+=1
                self.exp_bonus_increment = self.exp_bonus_increment+1000
                self.next_level_exp_requirement += self.exp_bonus_increment
            else:
                break
        print ("A level %i %s %s named %s has been initialized." % (self.level, self.race, self.character_class, self.name))

    def add_gold(self, val):
        self.gold+=val
        self.dump_gold_info()

    def add_currency(self, val, money_type):
        """ Automatically converts all currency into gold and tells you net worth."""
        conversion_factor = money_dictionary[money_type]
        self.currency+=value*conversion_factor

    def dump_gold_info(self):
        print ("%s has a pouch containing %i gold pieces!." % (self.name, self.gold))
            
    def load(self, filename):
        """reads a text file and reads the data, turning it into names, experience etc."""
        profile = {}
        character_file = open(filename, 'r')
        for line in character_file:
            try:
                x = line.split()
                key, value = x[0],x[1]
                profile[key] = value
            except:
                print("Found an invalid line in the file")
                print ("|" + line + "|")
        character_file.close()
        return profile

    def save(self, filename):
        """saves data about this level system to a text file for later reading."""
        dest = open(filename, 'w')
        for key in self.__dict__.keys():
            dest.write('\n%s %s' % (key, self.__dict__[key]))
        dest.close()
        print ("Saved.")

    def quick_save(self):
        self.save(testfile)

    def tell_me_about(self):
        print ("%s is a level %s %s %s with %s experience points. They have %s gold." % (self.name, self.level, self.race, self.character_class, self.experience, self.gold))
        print ("Strength:%s\nDexterity:%s\nConstitution:%s\nIntelligence:%s\nWisdom:%s\nCharisma:%s\n" % (self.strength, self.dexterity, self.constitution, self.intelligence, self.wisdom, self.charisma))
        
def test_functionality():
    
    input_dictionary = {
    "me":Charactersheet.tell_me_about,
    "save":Charactersheet.quick_save,
    "exp":Charactersheet.add_experience,
    "gold":Charactersheet.add_gold
    }
    
    newplayer = Charactersheet(character_file=johnfile)
    
    while True:
        txt = input()
        params = txt.split()
        command = input_dictionary[params[0]] #command lookup
        if len(params) == 1:
            command(newplayer)
        if len(params) == 2:
            command(newplayer, int(params[1]))
        
if __name__ == "__main__":
    test_functionality()
