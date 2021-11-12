

class Item(object):
    def __init__(self, consumable=False):
        self.item_name = "" ## Empty if generic, otherwise it will be something like "Great Flaming Axe of Burgeoning Dire-fire+3"
        self.item_description = "" ## Will be something that comes up if the player inspects an item. E.G. 'you see a glass bottle...'

    def dump_info(self):
        lines = []
        for key in self.__dict__.keys():
            value = self.__dict__[key]
            if value == "": ## detects an empty string
                value = '""'
            lines.append("%s = %s" % (key,value))
        return lines

class Consumable(Item):
    def __init__(self, servings=1):
        self.consumable = consumable ## True if you can eat it
        self.servings = servings ## 0 if there's none left, expects real integer
        self.healing_value = None ## E.G. 2d4+1 for an improved alchemical healing potion or 1d8+5 for a cure light wounds potion.
        self.consumable_benefits = [] ## A list of the various benefits the consumable confers. E.G. blindness, clarity(cure blindness), restore_mana, stabilize, cats_eyes

class Weapon(Item):
    def __init__(self, item_name = "", weapon_type = "", damage_type = "",
                 can_use_two_handed = False, reach_weapon = False, enhancement_bonus = 0):
        self.item_name = item_name
        self.weapon_type = weapon_type ## E.G. sword, bastardsword, waraxe, glaive, spear, club.
        self.damage_type = damage_type ## E.G. slashing, piercing, bludgeoning or ballistic
        try: ## has a name like orc killer+2 or something
            name, enhancement_bonus = item_name.split("+")
            self.enhancement_bonus = "+"+enhancement_bonus ## represents a bonus from masterwork quality or magical enhancements, usually applies directly to attack bonus
        except: ## does not have the weapon bonus in its name
            self.enhancement_bonus = 0
        self.can_use_two_handed = can_use_two_handed ## True if the weapon can be used two-handed for additional damage. (1.5x str modifier in 3.5e)
        self.reach_weapon = reach_weapon ## Only change to true if the weapon has reach like a glaive.
        self.range = weapon_range ## The distance the weapon can reach. Usually around 5 feet for a medium character using a spear or glaive.

class Equipment(Item):
    def __init__(self, equip_location,
                 equipment_bonus=0):
        self.equip_location = equip_location ## Where the equipment goes E.G. Helmet on head, boots on feet, necklace on neck etc.
        self.equipment_bonus = equipment_bonus ## represents the bonus the equipment gives when used as a tool. E.G. Using a crowbar to open a door gives +2 on strength checks to pry something open.

class Armour(Equipment):
    def __init__(self, equip_location,
                 armor_bonus = 0,
                 armor_check_penalty = 0):
        self.armor_bonus = armor_bonus ## Zero if the equipment does not provide armor
        self.armor_check_penalty = armor_check_penalty ## Will be a negative number. Applies on physical checks like swim and climb.

def test(): ## test automatic enhancement detection based on name
    a = Melee_Weapon(item_name="Longsword of Thunder+2")
    a.item_description = "A manly sword of a thundering nature."
    print(a.dump_info())

def test_2(): ## test a weapon with no bonus
    a = Melee_Weapon(weapon_type="shortsword")
    print(a.dump_info())

def test_3(): ## test an armour piece
    studded_leather = Armour(armor_bonus = 3,
                             armor_check_penalty = -1,
                             equip_location = "torso")
    print(studded_leather.dump_info())

def test_4(): ## test automatic loading of items from the item database [dnd_
    pass

if __name__ == "__main__":
    test_3()
