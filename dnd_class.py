import csv

bard_progression_file = "character_class_progression_bard.csv"
barbarian_progression_file = "character_class_progression_barbarian.csv"
cleric_progression_file = "character_class_progression_cleric.csv"
fighter_progression_file = "character_class_progression_fighter.csv"
rogue_progression_file = "character_class_progression_rogue.csv"
wizard_progression_file = "character_class_progression_wizard.csv"

HITDIE_DICTIONARY = {
    "barbarian" : "d12",
    "bard" : "d6",
    "cleric" : "d8",
    "fighter" : "d10",
    "rogue" : "d6",
    "wizard" : "d4"
    }

SKILLPOINTS_DICTIONARY = {
    "barbarian" : "4",
    "bard" : "6",
    "cleric" : "2",
    "fighter" : "2",
    "rogue" : "8",
    "wizard" : "2"
    }

def return_class_csv(class_name, show_all = False):
    filename = ("character_class_progression_"+class_name+".csv")
    with open('dnd_classes/'+filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile,dialect='excel')
        if show_all == True:
            for row in reader:
                print(row['level'],row['base_attack_bonus'],row['base_fortitude'],row['base_reflex'],row['base_will'],row['special'])
        else:
            for row in reader:
                print(row['level'],row['base_attack_bonus'])

            

class Dnd_class(object):
    def __init__(self,dnd_classname=""):
        if dnd_classname == "":
            raise Error()
        else: ## detected some sort of dnd class name
            self.table = {
                } ## nested table within a table. Indexed first by level then by parameter 
            ## So let's load it up
            filename = ("character_class_progression_"+dnd_classname+".csv")
            with open('dnd_classes/'+filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile,dialect='excel')
                for row in reader:
                    level_num = int(row['level'])
                    self.table[level_num] = row

    def get(self, level, parameter_name):
        return self.table[level][parameter_name]

def test(): ## initial csv test
    return_class_csv("cleric")

def test_2(): ## make an object that holds our class information and retrieve it
    cleric_cls = Dnd_class("cleric")
    level = 10
    print(cleric_cls.get(level,'base_attack_bonus'))
    print(cleric_cls.get(level,'base_fortitude'))
    print(cleric_cls.get(level,'base_reflex'))

if __name__ == "__main__":
    test_2()
