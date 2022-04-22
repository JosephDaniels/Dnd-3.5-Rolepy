from datetime import date

from skills import * ## import skill information

from xp import * ## import xp chart

from race import * ## import race data

SAVE_KEY_ABILITIES = {
    "base_fortitude"    :   "constitution",
    "base_reflex"       :   "dexterity",
    "base_will"         :   "wisdom"
    }

class Data(object):
    def __init__(self):
        return
    def __str__(self):
        return

class Character(object):
    """
This handles a DnD 3.5e character sheet.
This was built for use with the Rolepy Python Discord Bot.
The class holds character information once its loaded inside from
a text file. Please see the load for more information.

If an attribute has a value of -1 then it has not been set or was corrupted somehow.
    """
    def __init__(self, character_name = "",
                 picture_caption = "",
                 profile_image=None):

        ## CHARACTER INFO
        self.username = "" ## e.g. what they type to !login to the system
        self.display_name = "" ## e.g. Their long name like "Ulfric Northsun of the Bearmantle Clan"
        self.discord_username = "" ## The player's discord username such as Villager#1999
        self.player_name = "" ## The actual name of the person who the character belongs to e.g. John A. Macdonald
        self.character_class= [] ## lowercase character class with associated level e.g. ["fighterLv1","rogueLv2"]
        self.alignment = "" ## Lawful <-> Chaotic and Evil <-> Good E.G. "Lawful Good" or "Chaotic Evil" or "True Neutral"
        self.race = "" ## the name of their race in lowercase letters.

        ## PROFILE INFO

        self.age = -1
        self.height = ""
        self.weight = ""
        self.gender = ""
        self.eye_colour = ""
        self.hair_colour = ""
        self.skin_colour = ""
        self.favorite_weapon = ""

        ## Possible text documents
        self.description = ""
        self.public_history = ""  # What other players see when they look at your profile
        self.personal_history = ""  # The full back story of your character that only you and the DM know

        self.profile_image = profile_image ## something like bobby.jpg or something

        ## GAME INFO
        self.dying = False
        self.dead = False

        ## ATTRIBUTES
        self.strength = -1
        self.dexterity = -1
        self.constitution = -1
        self.intelligence = -1
        self.wisdom = -1
        self.charisma = -1

        ## STATISTICS
        self.maximum_health = -1
        self.current_health = -1
        self.armor_class = -1
        self.base_attack_bonus = -1
        self.initiative = -1
        self.xp_points = -1
        self.platinum_coins = 0
        self.gold_coins = 0
        self.silver_coins = 0
        self.copper_coins = 0

        ## SAVING THROWS
        self.base_fortitude = -1
        self.base_reflex = -1
        self.base_will = -1

        ## SKILLS
        self.init_all_skills() ## Initializes all skills at -1 before they are overridden properly

        self.feats = [] ## feats will get added to this list
        self.special_abilities = [] ## special class abilities are added to this list

        if character_name:
            filename = "characters/%s.txt" % (character_name) ## always the same
            self.load(filename)

        ## META DATA

        self.date_modified = date.today()
        self.date_created = date.today() ## Changed when it has loaded

    def init_all_skills(self):
        for skill in ALL_STANDARD_SKILLS:
            self.skill = -1

    def __lt__(self,other):
        return True ## It's a hack so that it sorts properly during initiative

    @staticmethod
    def parse_character_class(st):
        classes = []
        st = st.strip('[]')
        for char_class in st.split(","):
            classes.append(char_class.strip('"'))
        return classes

    def save(self, filename, show_all=True):
        self.date_modified = date.today()
        data = self.get_character_sheet(show_all=show_all)
        f = open(filename, mode='w+')
        f.write(data)
        f.close()

    def load(self, filename):
        """reads a text file and reads the data, turning it into names, experience etc.
            any variables that start with an underscore are internal variables and should not be
            modified or overridden by external sources.
            EXAMPLE FORMAT:
            name = zandrius
            display_name = zandrius_selwynn
            character_class = "fighterLv1,"wizardLv1","rogueLv1",
            strength = 12
            dexterity = 13
            constitution = 14
            intelligence = 12
            wisdom = 13
            charisma = 14
            gold_coins = 23
            silver_coins = 12
            copper_coins = 79
            total_experience = 78000
            current_hitpoints = 68
            total_hitpoints = 98
            _initiative_bonus = 1
            _total_hp = 93
            _total_
            etc..."""
        profile = {}
        character_file = open(filename, encoding="latin-1").read()
        character_file = character_file.split("\n")
        for line in character_file: ## Reading each line in the character like strength = 18
            key, value = line.split("=") ## Splits the arguments by the equals sign
            key, value = key.strip(), value.strip() ## remove whitespace
            if key == "character_class": ## SPECIAL PARSING FOR CHARACTERS CLASSES WHICH ARE ARRAYS
                # the character's classes are formatted in the file as
                #     character_class = clericLv1, druidLv10
                # so split at the ',' and then each is split further on "Lv"
                # The output will be a list of tuples like this:
                # [ ('cleric', 1), ('druid', 10)]
                parsed_classes = []
                # check if the character class is blank
                if len(value.strip("[]")) > 0:
                    char_classes = value.strip('[]').split(",") # split on comma, will give each class and their associated level
                    for raw_char_st in char_classes: ## Alan put this line it handles the full character string such as "fighterLv3" or "rogueLv2"
                        char_class_name, level = raw_char_st.split("Lv") # split between class name and level
                        try:
                            level = int(level)
                        except:
                            pass
                        parsed_classes.append( (char_class_name, level) )
                    value = parsed_classes
            if "(" in key: # detected that the user typed something like knowledge(arcana)
                main_key, sub_key = key.strip(")").split("(")
                if main_key in MULTIAREA_SKILL_CATEGORIES:
                    key = main_key+"_"+sub_key ## constructs the key e.g. knowledge_arcana
            else:   
                try:
                    value = int(value) ## tries to convert to a number
                except:
                    pass ## doesn't matter, stays a string
            profile[key] = value
        self.__dict__.update(profile)

    def get_full_profile(self):
        """ Returns a string that tells you ALL information about the character.
        CAREFUL! This might contain secret character information."""
        picture_status = ""
        image_file = ""
        if self.profile_image == None:
            picture_status = "-No Profile Picture Found-"
        response = " Username: %s\n" \
                   " Character Name: %s\n"\
                   " Race: %s\n" \
                   " Age: %i\n" \
                   " Gender: %s\n" \
                   " Eye colour: %s\n" \
                   " Hair colour: %s\n" \
                   " Skin colour: %s\n" \
                   " Strength: %s\n" \
                   " Dexterity: %s\n" \
                   " Constitution: %s\n" \
                   " Intelligence: %s\n" \
                   " Wisdom: %s\n" \
                   " Charisma: %s\n" \
                   " Max Health: %s\n" \
                   " Current Health: %s\n" \
                   " Height: %s\n" \
                   " Weight: %s\n" \
                   " Preferred Weapon, if any: %s\n" \
                   " Description: %s\n" \
                   " History: %s\n" \
                   " Picture: %s " %\
                   (self.username, self.display_name, self.race,
                    self.age, self.gender,
                    self.eye_colour.capitalize(),
                    self.hair_colour.capitalize(),
                    self.skin_colour.capitalize(),
                    self.strength,
                    self.dexterity,
                    self.constitution,
                    self.intelligence,
                    self.wisdom,
                    self.charisma,
                    self.maximum_health,
                    self.current_health,
                    self.height, self.weight, self.favorite_weapon,
                    self.description, self.public_history, picture_status)
        try:
            image_file = "character_portraits/"+self.profile_image
        except: ## Image file not found
            picture_status = "-No Profile Picture Found-"
            print("Wasn't able to find this image file! : %s" % (self.profile_image))
        return response, image_file

    def dump_info(self):
        for k in self.__dict__.keys():
            print (k, ":", self.__dict__[k])

    def get_profile(self):
        """ Returns a string that tells you public information about the character."""
        picture_status = ""
        image_file = ""
        if self.profile_image == None:
            picture_status = "-No Profile Picture Found-"
        response = " Username: %s\n" \
                   " Character Name: %s\n"\
                   " Race: %s\n" \
                   " Age: %i\n" \
                   " Gender: %s\n" \
                   " Eye colour: %s\n" \
                   " Hair colour: %s\n" \
                   " Skin colour: %s\n" \
                   " Height: %s\n" \
                   " Weight: %s\n" \
                   " Preferred Weapon, if any: %s\n" \
                   " Description: %s\n" \
                   " History: %s\n" \
                   " Picture: %s " %\
                   (self.username, self.display_name, self.race,
                    self.age, self.gender,
                    self.eye_colour.capitalize(),
                    self.hair_colour.capitalize(),
                    self.skin_colour.capitalize(),
                    self.height, self.weight, self.favorite_weapon,
                    self.description, self.public_history, picture_status)
        try:
            image_file = "character_portraits/"+self.profile_image
        except: ## Image file not found
            picture_status = "-No Profile Picture Found-"
            print("Wasn't able to find this image file! : %s" % (self.profile_image))
        return response, image_file

    def get_character_sheet(self, show_all = False):
        lines = []
        today = date.today()
        for key in self.__dict__.keys(): ## Goes through all the attributes of the character - strength, dex, skills etc
            value = self.__dict__[key] ## retrieves what the attribute corresponds to - so the value of strength or base_fortitude
            #Depending on the type we'll format it correctly
            if type(value) == Data:  # got a data object not currently used for anything just yet
                pass
            elif key == "character_class":
                char_classes = []
                for char_class_and_level in value:
                    char_class, level = char_class_and_level[0],char_class_and_level[1]
                    char_classes.append("%sLv%i" % (char_class,level))
                lines.append('%s = %s' % (key, char_classes))
            elif value == -1: ## Non-valid value
                if show_all == True:
                    lines.append("%s = %s" % (key, value))
            else: ## too much flowing through else exception
                lines.append('%s = %s' % (key, value))
        return "\n".join(lines)

    @staticmethod
    def _calculate_modifier(value):
        if value%2 == 1: ## Test if the attribute divides nicely
            value = value-1 ## If not, remove one to make it even
        modifier = int((value-10)/2) ## Attribute-1/2 is modifier formula
        return modifier

    def get_melee_attack_bonus(self,misc_modifier=0):
        relevant_attribute = "strength"
        attribute_value = self.__dict__[relevant_attribute] ## looks up the exact value of the attribute for the character
        attribute_modifier = Character._calculate_modifier(attribute_value)
        attack_value = self.base_attack_bonus+attribute_modifier+misc_modifier
        return attack_value

    def get_ranged_attack_bonus(self,misc_modifier=0):
        relevant_attribute = "dexterity"
        attribute_value = self.__dict__[relevant_attribute] ## looks up the exact value of the attribute for the character
        attribute_modifier = Character._calculate_modifier(attribute_value)
        attack_value = self.base_attack_bonus+attribute_modifier+misc_modifier
        return attack_value

    def get_spell_save(self, casting_attribute, spell_level=0, misc_modifier=0):
        attribute_value = self.__dict__[casting_attribute] ## looks up the exact value of the attribute for the character
        attribute_modifier = Character._calculate_modifier(attribute_value)
        spell_save = 10+attribute_modifier+spell_level+misc_modifier
        return spell_save

    def get_skill_ranks(self, skill):
        if self.__dict__[skill] == -1:
            print("Character doesn't have that skill. skill[%s]" % skill)
        else:
            skill_ranks = self.__dict__[skill] ##Looks up the number of ranks you have in a certain skill
            return int(skill_ranks)

    def get_skill_total(self, skill, misc_modifier=0):
        total = 0
        if self.__dict__[skill] == -1:
            print("Character %s doesn't have that skill. skill[%s]" % (self.username, skill))
        else:
            if "(" in skill:  # Case handling for someone typing something like knowledge(arcana)"
                words = skill.strip(")") ## Removes the trailing bracket knowledge(arcana) -> knowledge(arcana
                words = words.split("(") ## Splits the argument between the first bracket e.g. "knowledge", "arcana"
                multi_area_skill, area_of_expertise = words[0], words[1] ## Puts them into a human sounding variable
                relevant_attribute = SKILL_KEY_ABILITIES[multi_area_skill] ## gets a attribute for a skill E.G. spellcraft > intelligence
                attribute_value = self.__dict__[relevant_attribute] ## looks up the exact value of the attribute for the character
                attribute_modifier = Character._calculate_modifier(attribute_value)
                skill_ranks = self.get_skill_ranks(skill) ## Looks up how many ranks you put on your character sheet
                total = skill_ranks+attribute_modifier+misc_modifier ## adds the skill ranks to the attribute modifier
            for skill_category in MULTIAREA_SKILL_CATEGORIES: # grabs stuff like knowledge, perform, profession
                if skill_category in skill:
                    relevant_attribute = SKILL_KEY_ABILITIES[skill_category]  ## gets a attribute for a skill E.G. spellcraft > intelligence
                    break
            else:
                relevant_attribute = SKILL_KEY_ABILITIES[skill] ## gets a attribute for a skill E.G. spellcraft > intelligence
            attribute_value = self.__dict__[relevant_attribute] ## looks up the exact value of the attribute for the character
            attribute_modifier = Character._calculate_modifier(attribute_value)
            skill_ranks = self.get_skill_ranks(skill) ## Looks up how many ranks you put on your character sheet
            total = skill_ranks+attribute_modifier+misc_modifier ## adds the skill ranks to the attribute modifier
        return total

    def get_saving_throw(self, base_save, misc_modifier=0):
        """ returns a full saving throw with a target base save. Add the relevant attribute modifier automatically. """
        relevant_attribute = SAVE_KEY_ABILITIES[base_save] # gets an attribute for a save E.G. fortitude > constitution
        attribute_value = self.__dict__[relevant_attribute] ## looks up the exact value of the attribute for the character
        attribute_modifier = Character._calculate_modifier(attribute_value)
        saving_throw = self.__dict__[base_save]
        saving_throw_total = saving_throw+attribute_modifier+misc_modifier ## adds the skill ranks to the attribute modifier
        return saving_throw_total

    def get_initiative_bonus(self, misc_modifier=0):
        relevant_attribute = "dexterity"
        attribute_value = self.__dict__[relevant_attribute] ## looks up the exact value of the attribute for the character
        attribute_modifier = Character._calculate_modifier(attribute_value)
        initiative_bonus = attribute_modifier+misc_modifier
        return initiative_bonus

    def get_level(self):
        xp = self.xp_points
        for level, xp_threshold in XP_CHART:
            if xp > xp_threshold:
                pass
            elif xp <= xp_threshold:
                return level

    def get_coins(self):
        copper = self.copper_coins      #10 copper to a silver
        silver = self.silver_coins      #10 silver to a gold
        gold = self.gold_coins
        platinum = self.platinum_coins  #10 gold to a platinum
        return gold, silver, copper, platinum

    def get_net_worth(self):
        copper, silver, gold, platinum = self.get_coins()
        net_worth = 0.01*copper+0.1*silver+gold+10*platinum
        return net_worth

    def set_saving_throws_from_class_levels(self):
        pass

    def get_base_feat_count(self):
        level = self.get_level()
        if level%3: ## get the remainder after divide by 3
            remainder = level%3  # Remove the remainder
            level = level-remainder
        return level/3+1

    def get_max_class_skill_ranks(self):
        level = self.get_level()
        return level+3

    def get_max_cross_class_skill_ranks(self):
        level = self.get_level()
        if (level+3)%2:
            remainder = (level+3)%2
            level = level - remainder
        return (level+3)/2

    def validate_all_skills(self):
        # Validates all skills that are usable untrained. To be used after a character is filled in.
        # or just before.
        ### CURRENTLY BREAKS WHEN IT TRIES TO VALIDATE CRAFT KNOWLEDGE PROFESSION PERFORM
        skills = self.__dict__.keys() ## a list of all skills available
        skills_usable = SKILL_USABLE_UNTRAINED.keys()
        for skill in skills: ## finds all skills on the character sheet
            for multiskill in MULTIAREA_SKILLS: ## for things like "knowledge" "craft, "profession"
                if multiskill in skill: ## checks if a multi-area skill is detected
                    pass ## skips these values for validation
                elif multiskill not in skill:
                    if skill in skills_usable:
                        if self.__dict__[skill] >= 0: ## already has ranks, don't change it
                            pass
                        elif self.__dict__[skill] == -1: ## invalid detected
                            self.__dict__[skill] = 0


def test_1(): ## Runs a known working character and sees if the methods work
    paige_file = "characters/paige.txt"
    chara = Character()
    chara.load(paige_file)
    print("Tumble total is ", chara.get_skill_total("tumble", misc_modifier=0))
    print("Fortitude save total is ", chara.get_saving_throw("base_fortitude", misc_modifier=0))
    print("Reflex save total is ", chara.get_saving_throw("base_reflex", misc_modifier=0))
    print("Melee attack bonus is ", chara.get_melee_attack_bonus(misc_modifier=0))
    print("Ranged attack bonus is ", chara.get_ranged_attack_bonus(misc_modifier=0))
    print("Initiative bonus is ", chara.get_initiative_bonus(misc_modifier=0))
    print("Current level is ", chara.get_level())
    gold, silver, copper, platinum = chara.get_coins()
    character_net_worth = chara.get_net_worth()
    print("%s has %i gold, %i silver and %i copper pieces for a total of %i gold."
          % (chara.display_name, gold, silver, copper, character_net_worth))
    print("Base spell save is ", chara.get_spell_save("charisma"))
    print("Knowledge(Arcana) total is ", chara.get_skill_total("knowledge_arcana", misc_modifier=0))

def test_2(): ## Runs a basic character sheet and see if it shows up
    c = Character()
    print(c.get_character_sheet(show_all=True))

def test_3(): ## Test the character cheet save functionality
    b = Character()
    b.gold_coins = 1000000
    b.xp_points = 36000
    b.save("bobby.txt")

def test_4(): ## Test the loading functionality from a save file
    b = Character()
    b.load("characters/bobby.txt")
    print(b.get_character_sheet(show_all=True))

def test_5(): ## Test adding in an imp
    i = Character()
    i.load("npcs/imp.txt")
    print(i.get_character_sheet())

def test_6(): ## attempting to use the character class tables from character.py
    c = Character()
    c.load("characters/noob.txt")
    character_class = c.character_class
    print(character_class)

def test_7(): ## testing multiclass functionality
    c = Character()
    c.load("characters/paige.txt")
    print(c.get_saving_throw("fortitude"))

def test_8(): ## make a blank character
    c = Character()
    c.save("characters/blank.txt", show_all=True)

def test_9(): ## trying to validate all of ulfric's skills
    u = Character()
    u.load("characters/ulfric.txt")
    print(u.get_character_sheet(show_all=True))

def test_10(): ## Runs a test for character sheet and get profile on a known valid character
    paige_file = "characters/paige.txt"
    chara = Character()
    chara.load(paige_file)
    #chara.get_character_sheet()
    print(chara.get_character_sheet())
    print(chara.get_profile())

def test_11():
    paige_file = "characters/paige.txt"
    chara = Character()
    chara.load(paige_file)
    print(chara.get_character_sheet())

if __name__ == "__main__":
    test_8() # el blanko nino
    print ("test completed")