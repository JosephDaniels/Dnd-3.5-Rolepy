from constant import *

nathanfile = "nathan.txt"
carolinefile = "caroline.txt"
testfile = "test.txt"


class CharacterSheet(object):
    """ A level system similar to Dungeons and Dragons 3.5 Leveling. Uses a
        value of EXP points, works with event handling and without. """

    CORE_ATTRIBUTES = ["attack", "armor", "name", "max_hp", "curr_hp", "init_mod"]
    
    def __init__(self, save_file=None, dict_file = None,
                 name="Chicken Chaser", charclass="Peasant", race = "Human"):
        if save_file:
            self.__dict__.update(self.load(save_file))
            try:
                for key in self.__dict__.keys():
                    if key in DND_TITLE:
                        self.__dict__[key] = str(self.__dict__[key])
                    if key in DND_STATS:
                        self.__dict__[key] = int(self.__dict__[key])
                    if key in DND_ATTRIBUTES:
                        self.__dict__[key] = int(self.__dict__[key])
            except AttributeError:
                #### bug fixing. If experience is not found in the character sheet, it should default back to zero! #####
                print "Attribute not found in character sheet file. Using a default value"
        elif dict_file:
            for key in self.__dict__.keys():
                self.__dict__[key] = dict_file[key]
        else:
            self.attack = 1
            self.armor = 10
            self.experience = 0
            self.currency = 0
            self.name = name
            self.charclass = charclass
            self.race = race
            self.introduction()
        self.init_mod = 1
        self.weapon = "shotgun"
        self.inventory = ""
        self.max_hp = 10
        self.curr_hp = 10
        self.dead = False
        self.level_requirement = 1000
        self.exp_bonus = 1000
        self.level = 1
        self.do_leveling()

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
            
    def level_up(self):
        self.max_hp+=random.randint(1,6)
        self.init_mod+=1
        self.level+=1
        self.attack+=1
        self.armor+=1

    def add_experience(self, value):
        self.experience+=value
        self.try_lvl_up()

    def try_lvl_up(self):
        if self.experience >= self.level_requirement:
            print ("Level Up!")
            self.level_up()
            self.exp_bonus = self.exp_bonus+1000
            self.level_requirement += self.exp_bonus
        else:
            left = self.level_requirement-self.experience
            print ("You have %i experience points and need %i more experience points to become stronger." % (self.experience,left))

    def add_gold(self, val):
        self.gold+=val
	self.tell_gold()

    def add_currency(self, val, money_type):
        conversion_factor = money_dictionary[money_type]
        self.currency+=value*conversion_factor

    def tell_gold(self):
	print ("%s has a pouch containing %i gold pieces!." % (self.name, self.gold))

    
    def do_leveling(self):
        x =0
        while True:
            if self.experience >= self.level_requirement:
                x+=1
                self.level+=1
                self.exp_bonus = self.exp_bonus+1000
                self.level_requirement += self.exp_bonus     
            else:
                print ("A level %i %s %s named %s has been initialized." % (self.level, self.race, self.charclass, self.name))
                return False  
            
    def load(self, filename):
        """reads a text file and reads the data, turning it into names, experience etc."""
        profile = {}
        save_file = open(filename, 'rb')
        for line in save_file:
            try:
                x = line.split()
                key, value = x[0],x[1]
                for key in self.__dict__.keys():
                    profile[key] = value
            except:
                print("Found an invalid line in the file")
                print "|" + line + "|"
        save_file.close()
        return profile

    def save(self, filename):
        """saves data about this level system to a text file for later reading."""
        dest = open(filename, 'w')
        for key in self.__dict__.keys():
            for param in character_sheet_params:
                if key in param:
                    dest.write('\n%s %s' % (key, self.__dict__[key]))
        dest.close()

    def quick_save(self):
        self.save(testfile)

    def tell_me_about(self):
        print ("%s is a level %i %s %s with %i experience points under their belt." % (self.name, self.level, self.race, self.charclass, self.experience))

class Charclass:
    def __init__(self):
        pass
    
def test_functionality():
    input_dictionary = {
    "me":CharacterSheet.tell_me_about,
    "save":CharacterSheet.quick_save,
    "exp":CharacterSheet.add_experience,
    "gold":CharacterSheet.add_gold
    }
    newplayer = CharacterSheet()
    while True:
        text = raw_input()
        params = text.split()
        command = input_dictionary[params[0]]
        if len(params) == 1:
            apply(command, [newplayer])
        if len(params) == 2:
            apply(command, [newplayer,int(params[1])])
        
if __name__ == "__main__":
    test_functionality()
