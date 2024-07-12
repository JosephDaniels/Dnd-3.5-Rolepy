import csv

## Dungeon and Dragons 3.5 edition rule information. I used a lot of csv data.

barbarian_progression_file = "dnd35srd_character_class_progression_barbarian.csv"
bard_progression_file = "dnd35srd_character_class_progression_bard.csv"
cleric_progression_file = "dnd35srd_character_class_progression_cleric.csv"
druid_progression_file = "dnd35srd_character_class_progression_druid.csv"
fighter_progression_file = "character_class_progression_fighter.csv"
monk_progression_file = "character_class_progression_monk.csv"
paladin_progression_file = "character_class_progression_paladin.csv"
ranger_progression_file = "character_class_progression_ranger.csv"
rogue_progression_file = "character_class_progression_rogue.csv"
sorcerer_progression_file = "character_class_progression_sorcerer.csv"
wizard_progression_file = "character_class_progression_wizard.csv"

## Prestige classes


CLASS_SKILL_DICTIONARY = {
    "barbarian": ["climb", "craft", "handle_animal",
                  "intimidate", "jump", "listen",
                  "ride", "survival", "swim"],
    "bard": ["appraise", "balance", "bluff", "climb",
             "concentration", "craft", "decipher_script",
             "diplomacy", "disguise", "escape_artist",
             "gather_information", "hide", "jump",
             "knowledge(any)", "listen", "move_silently",
             "perform", "profession", "sense_motive",
             "sleight_of_hand", "speak_language",
             "spellcraft", "swim", "tumble",
             "use_magic_device"],
    "cleric": ["concentration", "craft", "diplomacy",
               "heal", "knowledge(arcana)",
               "knowledge(religion)",
               "knowledge(the_planes)",
               "profession",
               "spellcraft"],
    "druid": ["concentration", "craft", "diplomacy",
              "handle_animal", "heal", "knowledge(nature)",
              "listen", "profession", "ride",
              "spellcraft", "spot", "swim"],
    "fighter": ["climb", "craft", "handle_animal",
                "intimidate", "jump", "ride", "swim"],
    "monk": ["balance", "climb", "concentration", "craft",
             "diplomacy", "escape_artist", "jump",
             "knowledge(arcana)", "knowledge(religion)",
             "listen", "move_silently", "profession",
             "sense_motive", "spot", "swim", "tumble"],
    "paladin": ['concentration', "craft", "diplomacy",
                "diplomacy", "handle_animal", "heal",
                "knowledge(nobility)", "knowledge(religion)",
                "profession", "ride", "sense_motive"],
    "rogue": ["appraise", "balance", "bluff", "climb",
              "craft", "decipher_script", "diplomacy",
              "disable_device", "disguise", "escape_artist",
              "forgery", "gather_information", "hide",
              "intimidate", "jump", "knowledge(local)",
              "listen", "move_silently", "open_lock",
              "perform", "profession", "search",
              "sense_motive", "sleight_of_hand",
              "spellcraft", "spot", "swim", "tumble",
              "use_magic_device", "use_rope"],
    "ranger": ["climb", "concentration", "craft",
               "handle_animal", "heal", "hide", "jump",
               "knowledge(dungeoneering)",
               "knowledge(geography)",
               "knowledge(nature)",
               "listen", "move_silently",
               "profession", "ride", "search",
               "spot", "survival", "swim", "use_rope"],
    "sorcerer": ["bluff", "concentration", "craft",
                 "knowledge(arcana)",
                 "profession", "spellcraft"],
    "wizard": ["concentration", "craft",
               "decipher_script",
               "knowledge(all)",
               "profession",
               "spellcraft"]
}

CLASS_WEAPON_PROFICIENCY_DICTIONARY = {
    "barbarian": ["simple", "martial",
                  "light_armour",
                  "medium_armour",
                  "heavy_armour"],
    "bard": ["simple", "longsword", "rapier",
             "sap", "shortsword", "shortbow",
             "whip"
             ],
    "cleric": ["simple", "martial",
               "light_armour",
               "medium_armour",
               "heavy_armour",
               "shields"],
    "druid": ["club", "dagger", "dart",
              "quarterstaff", "scimitar",
              "sickle", "shortspear",
              "sling", "spear"],
    "fighter": ["simple", "martial",
                "light_armour",
                "medium_armour",
                "heavy_armour",
                "shields",
                "tower_shield"],
    "monk": ["simple", "exotic(kama)", "exotic(nunchaku)",
             "exotic(sai)", "exotic(shuriken)",
             "exotic(siangham)"],
    "paladin": ["simple", "martial",
                "light_armour",
                "medium_armour",
                "heavy_armour",
                "shields"],
    "rogue": "",
    "ranger": ["simple", "martial",
               "light_armour",
               "shields"],
    "sorcerer": ["simple"],
    "wizard": ["club",
               "dagger",
               "heavy_crossbow",
               "light_crossbow",
               "quarterstaff"]
}

HITDIE_DICTIONARY = {
    "barbarian": "d12",
    "bard": "d6",
    "cleric": "d8",
    "druid": "d8",
    "fighter": "d10",
    "monk": "d8",
    "paladin": "d10",
    "rogue": "d6",
    "ranger": "d8",
    "sorcerer": "d4",
    "wizard": "d4"
}

SKILLPOINTS_DICTIONARY = {
    "barbarian": "4",
    "bard": "6",
    "cleric": "2",
    "druid": "4",
    "fighter": "2",
    "monk": "4",
    "paladin": "2",
    "rogue": "8",
    "ranger": "6",
    "sorcerer": "2",
    "wizard": "2"
}


def return_class_csv(class_name, show_all=False):
    filename = ("character_class_progression_" + class_name + ".csv")
    with open('dnd_classes/' + filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, dialect='excel')
        if show_all == True:
            for row in reader:
                print(row['level'], row['base_attack_bonus'], row['base_fortitude'], row['base_reflex'],
                      row['base_will'], row['special'])
        else:
            for row in reader:
                print(row['level'], row['base_attack_bonus'])


class Dnd_class(object):
    def __init__(self, dnd_classname=""):
        if dnd_classname == "":
            print("made an instance of DnD class with no class name!?")
        else:  ## detected some sort of dnd class name
            table = {
            }  ## nested table within a table. Indexed first by level then by parameter
            ## So let's load it up
            filename = ("dnd35srd_character_class_progression_" + dnd_classname + ".csv")
            with open('dnd_classes/' + filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile, dialect='excel')
                for row in reader:
                    level_num = int(row['level'])
                    table[level_num] = row

    def get(self, level, parameter_name):
        return table[level][parameter_name]


def test():  ## initial csv test
    return_class_csv("cleric")


def test_2():  ## make an object that holds our class information and retrieve it
    cleric_cls = Dnd_class("rogue")
    level = 10
    print(cleric_cls.get(level, 'base_attack_bonus'))
    print(cleric_cls.get(level, 'base_fortitude'))
    print(cleric_cls.get(level, 'base_reflex'))


if __name__ == "__main__":
    test_2()
