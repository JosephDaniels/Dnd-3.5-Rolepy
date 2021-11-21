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
            data = load(character_file)
            __dict__.update(data)
            for key in __dict__.keys():
                if key in TITLE_INFO or key in CHARACTER_DETAILS: ## These are all strings
                    print (key+" was loaded succesfully.")
                    __dict__[key] = str(__dict__[key])
                elif key in ATTRIBUTES or key in STATS: ## These are all integers
                    print (key+" was loaded succesfully.")
                    __dict__[key] = int(__dict__[key])
                else:
                    print ("attempted to load "+key+ " but failed.")
                    
        weapon_righthand = {}
        weapon_lefthand = {}
        inventory = []
        alive = True
        level = 1
        next_level_exp_requirement = 1000
        exp_bonus_increment = 1000
        calc_level()

    # example of using a property declaration
    # in usage it looks like a regular property, but it's really calculated
    def _initiative_getter(self):
        return calc_modifier(dexterity)

    initiative = property(_initiative_getter, None)

        
    def calc_modifier(self, value):
        if value%2 == 1: ## Test if the attribute divides nicely
            value = value-1 ## If not, remove one to make it even
        modifier = int((value-10)/2) ## Attribute-1/2 is modifier formula
        return modifier

    def valid_input(self, expected_list):
        text = raw_input()
        if text in expected_list:
            return text
        if text not in expected_list:
            print ("Invalid entry. Going to default value.")
            pass
            
    def clone_attribs_from(self, profile):
        """ copy atrributes from the profile into our class """
        attribs = ["name", "experience", "strength", "dexterity", "constitution"]
        for key in attribs:
            __dict__[key] = profile.__dict__.get(key)

    def add_experience(self, value):
        experience+=int(value)
        try_lvl_up()

    def try_lvl_up(self):
        if experience >= next_level_exp_requirement: ## Try to level once
            print ("You've Leveled Up!") 
            level+=1
            exp_bonus_increment = exp_bonus_increment+1000
            next_level_exp_requirement += exp_bonus_increment
        else:
            left = next_level_exp_requirement-experience
            print ("You have %i experience points and need %i more experience points to become stronger." % (experience,left))

    def calc_level(self, debug=False):
        while True: ## Keep leveling up until at the correct current level
            if experience >= next_level_exp_requirement:
                level+=1
                exp_bonus_increment = exp_bonus_increment+1000
                next_level_exp_requirement += exp_bonus_increment
            else:
                break
        print ("A level %i %s %s named %s has been initialized." % (level, race, character_class, name))

    def add_gold(self, val):
        gold+=val
        dump_gold_info()

    def add_currency(self, val, money_type):
        """ Automatically converts all currency into gold and tells you net worth."""
        conversion_factor = money_dictionary[money_type]
        currency+=value*conversion_factor

    def dump_gold_info(self):
        print ("%s has a pouch containing %i gold pieces!." % (name, gold))
            
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
        for key in __dict__.keys():
            dest.write('\n%s %s' % (key, __dict__[key]))
        dest.close()
        print ("Saved.")

    def quick_save(self):
        save(testfile)

    def tell_me_about(self):
        print ("%s is a level %s %s %s with %s experience points. They have %s gold." % (name, level, race, character_class, experience, gold))
        print ("Strength:%s\nDexterity:%s\nConstitution:%s\nIntelligence:%s\nWisdom:%s\nCharisma:%s\n" % (strength, dexterity, constitution, intelligence, wisdom, charisma))
        
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
