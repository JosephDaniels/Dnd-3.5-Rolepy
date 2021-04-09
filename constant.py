TITLE_INFO = ["name", "character_class", "race"]

ATTRIBUTES = [
    "strength",
    "dexterity",
    "constitution",
    "intelligence",
    "wisdom",
    "charisma"
    ]

STATS = ["max_hp", "current_hp", "experience", "gold", "attack", "armor"] ## All of these are integers.

CHARACTER_DETAILS = ["gender", "weight", "height", "skin", "eyes", "hair", "age", "build"]

DND_RACES = {
    "Human":"The most ambitious creatures, they are the most varied in their niches. The most adaptive of the races.",
    "Half-Elf":"A race of people born unto a Elf and a Human, beings of this race find little comfort in either culture. They are universally accepted, but may spend their entire life wandering for a place they belong",
    "Elf":"The most artistic and graceful of the races. They are the masters of magic and music.",
    "Dwarf":"Short, gruff and tough like boulders. A Dwarf's iron will is matched with a stout body.",
    "Half-Orc":"Broad headed and thick, these beasts are the toughest of the outland races. They are vicious and hardy.",
    "Gnome":"Born mischievious and clever, these small yet larger than life creatures are marvellous wizards and engineers.",
    "Halfling":"Grown in the outlands, these wily tricksters are very keen and quick. They are always ready with a quick retort or dart throw"
    }

DND_CLASSES = {
    "Plague Doctor":"Disease and Death follow him as naturally as healing and life.",
    "Warrior":"Combat and weaponry are his primary focuses. He is strong and hardy.",
    "Wizard":"Casting spells for both offensive and defensive purposes. He spends too much time with his nose in books, and is weak and pale.",
    "Rogue":"He lives to bend the rules. Sneaking around, theiving and backstabbing, he is always on the run, and is lithe and wiry.",
    "Shaman":"He lives in the forests, commanding the animals and trees to his will. He is wise and hardy.",
    "Witch Doctor":"He conjures up danger with his voodoo dolls.",
    }

WIZARD_SKILLS = [
    "Speech",
    "Science",
    "Appraise",
    "Spellcraft",
    "Perception"
    ]

WIZARD_SPELLS = {
    "Magic Missile":"Does (1-4) pure damage +1(1-4)/(2 caster levels)",
    "Protect":"Adds +1 to an individual's defence score for 10 rounds(+1 per caster level)",
    "Observer Wards":"Allows you to place down defensive wards to act as an early warning system for enemies.",
                }

ROGUE_SKILLS = [
    "Stealth",
    "Larceny",
    "Disable device",
    "Gamble",
    "Bluff",
    "Appraise",
    "Perception",
    "Search"
    ]

CURRENCY = {
    "astral_crystal":1000,
    "platinum":10,
    "electrum":1.5,
    "gold":1,
    "silver":0.1,
    "copper":0.01,
    "seashells":0.001
    }


SKILLS = {
    "Swim":"STR based skill. When swim checks are made this skill has the potential to improve speed.",
    "Climb":"STR based skill. When climb checks are made this skill has the potential to improve speed.",
    "Stealth":"DEX based skill. Stealth improves your ability to avoid detection when hiding.",
    "Survival":"WIS based skill. Survival improves your ability to track, and survive.",
    "Larceny":"DEX based skill. Allows you to pick locks and pockets and break into structures, crack safes, etc.",
    "Disable device":"INT based skill. Allows you to disarm and dissassemble traps and other objects.",

    "Barter":"CHA/WIS based skill. Allows you to get better deals in shops and in trades with NPCs.",
    "Speech":"CHA based skill. Improves eloquence of speech and relations with NPCs.",
    "Gamble":"WIS based skill. You know when to fold 'em, and you're luckier in any gambling situation.",
    "Socialize":"CHA based skill. This skill determines how much NPCs like you and how easy or difficult it is to make friends.",
    "Intimidate":"CHA based skill. This skill determines how threatening NPCs find you, and how likely you are to scare them on attempt.",
    "Bluff":"CHA based skill. This skill determines how likely NPCs are to believe you if lying.",

    "Science":"INT based skill. Improves your item synthesis abilities, and ability to work with computers.",
    "Repair":"INT based skill. Allows you to repair and upkeep weapons and items in your inventory.",
    "Heal":"CON based skill. Your natural ability to regenerate hp over time and from health items.",
    "Surgery":"WIS based skill. Your ability to provide medical care and treat serious injuries eg. broken limbs.",
    "Appraise":"INT based skill. Your ability to discern base value and mundane details about found objects.",
    "Spellcraft":"WIS based skill. Your ability to discern magical details about found objects and to use magical devices.",
    "Perception":"WIS based skill. Your ability to notice and percieve nearby enemies. Improves player LOS distance.",
    "Search":"WIS based skill. Your ability to uncover and discover hidden objects while actively looking."
}


    
