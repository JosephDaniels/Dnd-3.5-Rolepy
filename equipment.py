import csv

## New and improved SRD+ homebrew content
dnd_food_file = "dnd35_food_table.csv"
dnd_improvised_weapons_file = "dnd35_improvised_weapon_table.csv"
dnd_food_file = "dnd35_food_table.csv"

## Stuff pulled straight from the original DnD 3.5e rulebook
dnd_armour_file = "dnd35srd_armour_table.csv"
dnd_clothing_file = "dnd35srd_clothing_table.csv"
dnd_hardness_file = "dnd35srd_item_hardness_table.csv"
dnd_mundane_items_file = "dnd35srd_mundane_items_table.csv"
dnd_weapon_and_shield_hardness_file = "dnd35srd_weapon_and_shield_hardness_table.csv"
dnd_substance_hardness_table = "dnd35srd+_substance_hardness_table


def get_item_csv_from_table(table_name):
    tablename = table_name
    with open('"dnd_tables/' + filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, dialect='excel')
        for row in reader:
            print(row['item_name'],
                  row['proficiency'],
                  row['cost'],
                  row['damage_small'],
                  row['damage_medium'],
                  row['damage_large'],
                  row['critical'],
                  row['range_increment'],
                  row['weight'],
                  row['weapon_type'],
                  row['special'])


class Item(object):
    """
    This is a basic item. It can be manipulated and moved.
    If initiated with some sort of name, it will look it up
    in the local file folder and try to create that item
    based on a typical one from the database.

    If initiated by itself, you can override the default
    instance to do whatever you need it to do.

    Useful functions:
    dump_info()
"""

    def __init__(self, item_name=""):
        if item_name == "":
            print("""Empty item created.
                    Override me at your discretion."""
            item_name = ""  ## Empty if generic, otherwise it will be something like "Great Flaming Axe of Burgeoning Dire-fire+3"
            item_description = ""  ## Will be something that comes up if the player inspects an item. E.G. 'you see a glass bottle...'

    def dump_info(self):
        lines = []
        for key in __dict__.keys():
            value = __dict__[key]
            if value == "":  ## detects an empty string
                value = '""'
            lines.append("%s = %s" % (key, value))
        return lines


class Consumable(Item):
    """
A specialized version of item that's meant to be eaten.
Examples: apples, banana, beer, bread, meat
"""

    def __init__(self, servings=1):
        consumable = consumable  ## True if you can eat it
        servings = servings  ## 0 if there's none left, expects real integer
        healing_value = None  ## E.G. 2d4+1 for an improved alchemical healing potion or 1d8+5 for a cure light wounds potion.
        consumable_benefits = []  ## A list of the various benefits the consumable confers. E.G. blindness, clarity(cure blindness), restore_mana, stabilize, cats_eyes


class Melee_Weapon(Item):
    def __init__(self, item_name="", weapon_type="", damage_type="",
                 can_use_two_handed=False, reach_weapon=False, enhancement_bonus=0):
        item_name = item_name
        weapon_type = weapon_type  ## E.G. sword, bastardsword, waraxe, glaive, spear, club.
        damage_type = damage_type  ## E.G. slashing, piercing, bludgeoning or ballistic
        try:  ## has a name like orc killer+2 or something
            name, enhancement_bonus = item_name.split("+")
            enhancement_bonus = "+" + enhancement_bonus  ## represents a bonus from masterwork quality or magical enhancements, usually applies directly to attack bonus
        except:  ## does not have the weapon bonus in its name
            enhancement_bonus = 0
        can_use_two_handed = can_use_two_handed  ## True if the weapon can be used two-handed for additional damage. (1.5x str modifier in 3.5e)
        reach_weapon = reach_weapon  ## Only change to true if the weapon has reach like a glaive.
        if reach_weapon == True:
            range = weapon_range  ## The distance the weapon can reach. Usually around 5 feet for a medium character using a spear or glaive.


class Ranged_Weapon(Item):
    def __init__(self, item_name="", weapon_type="", damage_type="",
                 can_use_two_handed=False, enhancement_bonus=0):
        item_name = item_name
        weapon_type = weapon_type  ## E.G. longbow, shortbow, sling etc.
        damage_type = damage_type  ## E.G. usually piercing or ballistic
        try:  ## has a name like orc killer bow+2 or something
            name, enhancement_bonus = item_name.split("+")
            enhancement_bonus = enhancement_bonus  ## represents a bonus from masterwork quality or magical enhancements, usually applies directly to attack bonus
        except:  ## does not have the weapon bonus in its name
            enhancement_bonus = 0  ## will have to be set manually if you wish it to be otherwise
        can_use_two_handed = can_use_two_handed  ## True if the weapon can be used two-handed like a longbow.
        range = weapon_range  ## The range increment for the weapon. -2 penalty per increment you are away from your target.


class Equipment(Item):
    def __init__(self, equip_location,
                 equipment_bonus=0):
        equip_location = equip_location  ## Where the equipment goes E.G. Helmet on head, boots on feet, necklace on neck etc.
        equipment_bonus = equipment_bonus  ## represents the bonus the equipment gives when used as a tool. E.G. Using a crowbar to open a door gives +2 on strength checks to pry something open.


class Armour(Equipment):
    def __init__(self, equip_location,
                 armor_bonus=0,
                 armor_check_penalty=0):
        armor_bonus = armor_bonus  ## Zero if the equipment does not provide armor
        armor_check_penalty = armor_check_penalty  ## Will be a negative number. Applies on physical checks like swim and climb.


def test():  ## test automatic enhancement detection based on name
    a = Melee_Weapon(item_name="Longsword of Thunder+2")
    a.item_description = "A manly sword of a thundering nature."
    print(a.dump_info())


def test_2():  ## test a weapon with no bonus
    a = Melee_Weapon(weapon_type="shortsword")
    print(a.dump_info())


def test_3():  ## test an armour piece
    studded_leather = Armour(armor_bonus=3,
                             armor_check_penalty,
                             equip_location="torso")
    print(studded_leather.dump_info())


def test_4():  ## test automatic loading of items from the item database [dnd_
    pass


if __name__ == "__main__":
    test_3()
