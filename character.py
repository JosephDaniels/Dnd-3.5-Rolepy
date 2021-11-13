#from dnd35_class import * ## This is Dnd 3.5e SRD Players handbook classes

## Just a bunch of skills related to abilities not much to see here

SKILL_KEY_ABILITIES = { ## All skills and their related abilities
    "appraise"          :   "intelligence",
    "balance"           :   "dexterity",
    "bluff"             :   "charisma",
    "climb"             :   "strength",
    "concentration"     :   "constitution",
    "craft"             :   "intelligence",
    "decipher_script"   :   "intelligence",
    "diplomacy"         :   "charisma",
    "disable_device"    :   "intelligence",
    "disguise"          :   "charisma",
    "escape_artist"     :   "dexterity",
    "forgery"           :   "intelligence",
    "gather_information":   "charisma",
    "handle_animal"     :   "charisma",
    "heal"              :   "wisdom",
    "hide"              :   "dexterity",
    "intimidate"        :   "charisma",
    "jump"              :   "strength",
    "knowledge"         :   "intelligence",
    "listen"            :   "wisdom",
    "move_silently"     :   "dexterity",
    "open_lock"         :   "dexterity",
    "perform"           :   "charisma",
    "profession"        :   "wisdom",
    "ride"              :   "dexterity",
    "search"            :   "intelligence",
    "sense_motive"      :   "wisdom",
    "sleight_of_hand"   :   "dexterity",
    "spellcraft"        :   "intelligence",
    "spot"              :   "wisdom",
    "survival"          :   "wisdom",
    "swim"              :   "strength",
    "tumble"            :   "dexterity",
    "use_magic_device"  :   "charisma",
    "use_rope"          :   "dexterity"
    }

SKILL_USABLE_UNTRAINED = { ## all skills; are they usable untrained or not?
    ## True if usable untrained. False if not. 
    "appraise"          :   True,
    "balance"           :   True,
    "bluff"             :   True,
    "climb"             :   True,
    "concentration"     :   True,
    "craft"             :   True,
    "decipher_script"   :   False,
    "diplomacy"         :   True,
    "disable_device"    :   False,
    "disguise"          :   True,
    "escape_artist"     :   True,
    "forgery"           :   True,
    "gather_information":   True,
    "handle_animal"     :   False,
    "heal"              :   True,
    "hide"              :   True,
    "intimidate"        :   True,
    "jump"              :   True,
    "knowledge"         :   False,
    "listen"            :   True,
    "move_silently"     :   True,
    "open_lock"         :   False,
    "perform"           :   False,
    "profession"        :   False,
    "ride"              :   True,
    "search"            :   True,
    "sense_motive"      :   True,
    "sleight_of_hand"   :   False,
    "spellcraft"        :   False,
    "spot"              :   True,
    "survival"          :   True,
    "swim"              :   True,
    "tumble"            :   False,
    "use_magic_device"  :   True,
    "use_rope"          :   True
    }



## Every level associated with the experience needed to get there.
## It can easily be calculated with a formula but I have found
## that life is easier when you type things like this out properly.

XP_CHART = (
    (1 ,    0),
    (2 ,    1000),
    (3 ,    3000),
    (4 ,    6000),
    (5 ,    10000),
    (6 ,    15000),
    (7 ,    21000),
    (8 ,    28000),
    (9 ,    36000),
    (10,    45000),
    (11,    55000),
    (12,    66000),
    (13,    78000),
    (14,    91000),
    (15,    105000),
    (16,    120000),
    (17,    136000),
    (18,    153000),
    (19,    171000),
    (20,    190000)
    )

SAVE_KEY_ABILITIES = {
    "base_fortitude"    :   "constitution",
    "base_reflex"       :   "dexterity",
    "base_will"         :   "wisdom"
    }

# in the txt file that saves attributes for a character, these will have braces in the file
# eg. knowledge(arcana)
MULTI_AREA_SKILLS = ["knowledge","profession","craft","perform"]

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
    def __init__(self, character_name = "", picture_caption = "",
                 profile_image=None):

        ## CHARACTER INFO
        self.name = "" ## e.g. Single name like "Conan"
        self.display_name = "" ## e.g. long name like "Conan the Barbarian"
        self.discord_username = "" ## The player's discord username such as Villager#1999
        self.character_class= [] ## lowercase character class with associated level e.g. ["fighterLv1","rogueLv2"]
        self.alignment = "" ## Lawful <-> Chaotic and Evil <-> Good E.G. "Lawful Good" or "Chaotic Evil" or "True Neutral"

        ## PROFILE INFO
        self.age = -1
        self.gender = ""
        self.description = ""
        self.public_history = ""  # What other players see when they look at your profile
        self.full_history = ""  # The full back story of your character that only you and the DM know
        self.eye_colour = ""
        self.hair_colour = ""
        self.skin_colour = ""
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
        self.appraise = -1
        self.balance = -1
        self.bluff = -1
        self.climb = -1
        self.concentration = -1
        
        self.craft_alchemy = -1
        self.craft_weaponsmithing = -1
        self.craft_armoursmithing = -1
        self.craft_masonry = -1
        self.craft_carpentry = -1
        self.craft_poison = -1
        self.craft_trap = -1
        self.craft_culinary = -1
        self.craft_musical_composition = -1
        self.craft_written_composition = -1
        
        self.decipher_script = -1
        self.diplomacy = -1
        self.disable_device = -1
        self.disguise = -1
        self.escape_artist = -1
        self.forgery = -1
        self.gather_information = -1
        self.handle_animal = -1
        self.heal = -1
        self.hide = -1
        self.intimidate = -1
        self.jump = -1
        
        self.knowledge_arcana = -1
        self.knowledge_engineering = -1
        self.knowledge_dungeoneering = -1
        self.knowledge_geography = -1
        self.knowledge_history = -1
        self.knowledge_local = -1
        self.knowledge_nature = -1
        self.knowledge_nobility = -1
        self.knowledge_religion = -1
        self.knowledge_the_planes = -1

        self.listen = -1
        self.move_silently = -1
        self.open_lock = -1

        self.perform_act = -1
        self.perform_comedy = -1
        self.perform_dance = -1
        self.perform_keyboard = -1
        self.perform_oratory = -1
        self.perform_percussion = -1
        self.perform_stringed = -1
        self.perform_wind = -1
        self.perform_sing = -1
        
        self.profession_academic = -1
        self.profession_apothecary = -1
        self.profession_celebrity = -1
        self.profession_military = -1
        self.profession_criminal = -1
        self.profession_doctor = -1
        self.profession_entrepreneur = -1
        self.profession_investigator = -1
        self.profession_scavenger = -1
        self.profession_religious = -1
        self.profession_transporter = -1
        self.profession_engineer = -1
        self.profession_alchemist = -1
        self.profession_monster_hunter = -1

        self.ride = -1
        self.search = -1
        self.sense_motive = -1
        self.sleight_of_hand = -1
        
        self.speak_language_abyssal = -1 ## Demon and evil creatures written in Infernal
        self.speak_language_aquan = -1 ## Water based creatures written in elven
        self.speak_language_auran = -1 ## Air based creatures written in draconic
        self.speak_language_celestial = -1 ## Good outsiders written in celestial
        self.speak_language_common = -1
        self.speak_language_draconic = -1 # Kobolds, Troglodytes, Lizardfolk and Dragons
        self.speak_language_druidic = -1 # Druids ONLY!!!
        self.speak_language_dwarven = -1
        self.speak_language_elven = -1
        self.speak_language_giant = -1 # Ogres and giants
        self.speak_language_gnome = -1
        self.speak_language_goblin = -1 # Goblins, hobgoblins and bugbears
        self.speak_language_gnoll = -1
        self.speak_language_halfling = -1
        self.speak_language_ignan = -1 #Fire based creatures written in infernal
        self.speak_language_orcish = -1 #Written in Orcish
        self.speak_language_sylvan = -1 #Dryads, brownies, leprechauns written in elven
        self.speak_language_terran = -1 #Xorns and earth based creatures written in dwarven
        self.speak_language_undercommon = -1 #Drow written in elven

        self.spellcraft = -1
        self.spot = -1
        self.survival = -1
        self.swim = -1
        self.tumble = -1
        self.use_magic_device = -1
        self.use_rope = -1

        self.feats = [] ## feats will get added to this list
        self.special_abilities = [] ## special class abilities are added to this list

        if character_name:
            filename = "characters/%s.txt" % (character_name) ## always the same
            self.load(filename)

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
                parsed_classes =  []
                char_classes= value.split(",") # split on comma, will give each class and their associated level
                for raw_char_st in char_classes: ## Alan put this line it handles the full character string such as "fighterLv3" or "rogueLv2"
                    char_class_name, level = raw_char_st.split("Lv") # split between class name and level
                    try: level = int(level) # Tries to convert to a 
                    except: print("didn't manage to convert ["+level+"] to an int.")
                    parsed_classes.append( (char_class_name, level) )
                value = parsed_classes
            if "(" in key: # detected that the user typed something like knowledge(arcana)
                main_key, sub_key = key.strip(")").split("(")
                if main_key in MULTI_AREA_SKILLS:
                    main_key, sub_key = key.strip(")").split("(")
                    key = main_key+"_"+sub_key ## constructs the key e.g. knowledge_arcana
            else:   
                try:    value = int(value) ## tries to convert to a number
                except: pass ## doesn't matter, stays a string
            profile[key] = value
        self.__dict__.update(profile)

    def get_profile(self):
        """ Returns a string that tells you public information about the character."""
        picture_status = ""
        if self.profile_image == None:
            picture_status = "TBD"
        response = "Name: %s\n Age: %i\n Gender: %s\n" \
                   " Eyes: %s\n" \
                   " Hair: %s\n" \
                   " Skin: %s\n" \
                   " Description: %s\n" \
                   " History: %s\n" \
                   " %s " %\
                   (self.display_name, self.age, self.gender,
                    self.eye_colour, self.hair_colour, self.skin_colour,
                    self.description, self.public_history, self.picture_caption)
        image_file = "images/"+self.profile_image
        return response, image_file

    def get_character_sheet(self, show_all = False):
        lines = []
        for key in self.__dict__.keys(): ## Goes through all the attributes of the character
            value = self.__dict__[key]
            #Depending on the type we'll format it correctly
            if type(value) == Data:
                pass
            elif type(value) == str:
                lines.append('%s = "%s"' % (key, value))
            elif value == -1: ## Non-valid value
                if show_all == True:
                    lines.append("%s = %s" % (key, value))
            else:
                lines.append("%s = %s" % (key, value))
        return "\n".join(lines)

    @staticmethod
    def calculate_modifier(value):
        if value%2 == 1: ## Test if the attribute divides nicely
            value = value-1 ## If not, remove one to make it even
        modifier = int((value-10)/2) ## Attribute-1/2 is modifier formula
        return modifier

    def get_melee_attack_bonus(self,misc_modifier=0):
        relevant_attribute = "strength"
        attribute_value = self.__dict__[relevant_attribute] ## looks up the exact value of the attribute for the character
        attribute_modifier = Character.calculate_modifier(attribute_value)
        attack_value = self.base_attack_bonus+attribute_modifier+misc_modifier
        return attack_value

    def get_ranged_attack_bonus(self,misc_modifier=0):
        relevant_attribute = "dexterity"
        attribute_value = self.__dict__[relevant_attribute] ## looks up the exact value of the attribute for the character
        attribute_modifier = Character.calculate_modifier(attribute_value)
        attack_value = self.base_attack_bonus+attribute_modifier+misc_modifier
        return attack_value

    def get_spell_save(self, casting_attribute, spell_level=0,misc_modifier=0):
        attribute_value = self.__dict__[casting_attribute] ## looks up the exact value of the attribute for the character
        attribute_modifier = Character.calculate_modifier(attribute_value)
        spell_save = 10+attribute_modifier+spell_level+misc_modifier
        return spell_save

    def get_skill_ranks(self, skill):
        if self.__dict__[skill] == -1:
            print("Character doesn't have that skill. skill[%s]" % skill)
        else:
            skill_ranks = self.__dict__[skill] ##Looks up the number of ranks you have in a certain skill
            return skill_ranks

    def get_skill_total(self, skill, misc_modifier=0):
        total = 0
        if self.__dict__[skill] == -1:
            print("Character %s doesn't have that skill. skill[%s]" % (self.name, skill))
        else:
            if "(" in skill: ## Detects a skill like knowledge, craft, profession, perform
                words = skill.strip(")") ## Removes the trailing bracket knowledge(arcana) -> knowledge(arcana
                words = words.split("(") ## Splits the argument between the first bracket e.g. "knowledge", "arcana"
                multi_area_skill, area_of_expertise = words[0], words[1] ## Puts them into a human sounding variable
                relevant_attribute = SKILL_KEY_ABILITIES[multi_area_skill] ## gets a attribute for a skill E.G. spellcraft > intelligence
                attribute_value = self.__dict__[relevant_attribute] ## looks up the exact value of the attribute for the character
                attribute_modifier = Character.calculate_modifier(attribute_value)
                skill_ranks = self.get_skill_ranks(skill) ## Looks up how many ranks you put on your character sheet
                total = skill_ranks+attribute_modifier+misc_modifier ## adds the skill ranks to the attribute modifier
            else:
                relevant_attribute = SKILL_KEY_ABILITIES[skill] ## gets a attribute for a skill E.G. spellcraft > intelligence
                attribute_value = self.__dict__[relevant_attribute] ## looks up the exact value of the attribute for the character
                attribute_modifier = Character.calculate_modifier(attribute_value)
                skill_ranks = self.get_skill_ranks(skill) ## Looks up how many ranks you put on your character sheet
                total = skill_ranks+attribute_modifier+misc_modifier ## adds the skill ranks to the attribute modifier
        return total

    def get_saving_throw(self, base_save, misc_modifier=0):
        """ returns a full saving throw with a target base save. Add the relevant attribute modifier automatically. """
        relevant_attribute = SAVE_KEY_ABILITIES[base_save] # gets an attribute for a save E.G. fortitude > constitution
        attribute_value = self.__dict__[relevant_attribute] ## looks up the exact value of the attribute for the character
        attribute_modifier = Character.calculate_modifier(attribute_value)
        saving_throw = self.__dict__[base_save]
        saving_throw_total = saving_throw+attribute_modifier+misc_modifier ## adds the skill ranks to the attribute modifier
        return saving_throw_total

    def get_initiative_bonus(self, misc_modifier=0):
        relevant_attribute = "dexterity"
        attribute_value = self.__dict__[relevant_attribute] ## looks up the exact value of the attribute for the character
        attribute_modifier = Character.calculate_modifier(attribute_value)
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
        copper = self.copper_coins  #10 copper to a silver
        silver = self.silver_coins  #10 silver to a gold
        gold = self.gold_coins      #10 gold to a platinum
        return gold, silver, copper

    def get_net_worth(self):
        copper = self.copper_coins  #10 copper to a silver
        silver = self.silver_coins  #10 silver to a gold
        gold = self.gold_coins      #10 gold to a platinum
        platinum = self.platinum_coins
        net_worth = 0.01*copper+0.1*silver+gold+10*platinum
        return net_worth

    def set_saving_throws_from_class_levels(self):
        pass

    def get_base_feat_count(self):
        level = self.get_level()
        return level/3+1

    def get_max_class_skill_ranks(self):
        level = self.get_level()
        return level+3

    def get_max_cross_class_skill_ranks(self):
        level = self.get_level()
        return (level+3)/2

    def validate_all_skills(self):
        # Validates all skills that are usable untrained. To be used after a character is filled in.
        # or just before.
        ### CURRENTLY BREAKS WHEN IT TRIES TO VALIDATE CRAFT KNOWLEDGE PROFESSION PERFORM
        skills = self.__dict__.keys() ## a list of all skills available
        skills_usable = SKILL_USABLE_UNTRAINED.keys()
        for skill in skills: ## finds all skills on the character sheet
            for multiskill in MULTI_AREA_SKILLS: ## for things like "knowledge" "craft, "profession"
                if multiskill in skill: ## checks if a multi-area skill is detected
                    pass ## skips these values for validation
                elif multiskill not in skill:
                    if skill in skills_usable:
                        if self.__dict__[skill] >= 0: ## already has ranks, don't change it
                            pass
                        elif self.__dict__[skill] == -1: ## invalid detected
                            self.__dict__[skill] = 0
                else:
                    print ("this should never happen!!!")

    
def test_1(): ## Runs a known working character and sees if the methods work
    paige_file = "paige.txt"
    chara = Character()
    profile = chara.load(paige_file)
    chara.get_character_sheet()
    print("Tumble total is ", chara.get_skill_total("tumble", misc_modifier=0))
    print("Fortitude save total is ", chara.get_saving_throw("base_fortitude", misc_modifier=0))
    print("Reflex save total is ", chara.get_saving_throw("base_reflex", misc_modifier=0))
    print("Melee attack bonus is ", chara.get_melee_attack_bonus(misc_modifier=0))
    print("Ranged attack bonus is ", chara.get_ranged_attack_bonus(misc_modifier=0))
    print("Initiative bonus is ", chara.get_initiative_bonus(misc_modifier=0))
    print("Current level is ", chara.get_level())
    gold, silver, copper = chara.get_coins()
    character_net_worth = chara.get_net_worth()
    print("%s has %i gold, %i silver and %i copper pieces for a total of %i gold."
          % (chara.display_name, gold, silver, copper, character_net_worth))
    print("Base spell save is ", chara.get_spell_save("charisma"))
    print("Knowledge(Arcana) total is ", chara.get_skill_total("knowledge(arcana)", misc_modifier=0))

def test_2(): ## Runs a basic character sheet and see if it shows up
    c = Character()
    print(c.get_character_sheet(show_all=True))

def test_3(): ## Test the character cheet save functionality
    b = Character()
    b.name = "Bobby Boy"
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
    u.validate_all_skills()
    print(u.get_character_sheet())

if __name__ == "__main__":
    test_9()
    
