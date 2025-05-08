MULTIAREA_SKILL_CATEGORIES = ["craft", "knowledge", "profession", "perform"]

SKILL_KEY_ABILITIES = {  ## All skills and their related abilities
    "appraise": "intelligence",
    "balance": "dexterity",
    "bluff": "charisma",
    "climb": "strength",
    "concentration": "constitution",
    "craft": "intelligence",
    "decipher_script": "intelligence",
    "diplomacy": "charisma",
    "disable_device": "intelligence",
    "disguise": "charisma",
    "escape_artist": "dexterity",
    "forgery": "intelligence",
    "gather_information": "charisma",
    "handle_animal": "charisma",
    "heal": "wisdom",
    "hide": "dexterity",
    "intimidate": "charisma",
    "jump": "strength",
    "knowledge": "intelligence",
    "listen": "wisdom",
    "move_silently": "dexterity",
    "open_lock": "dexterity",
    "perform": "charisma",
    "profession": "wisdom",
    "ride": "dexterity",
    "search": "intelligence",
    "sense_motive": "wisdom",
    "sleight_of_hand": "dexterity",
    "spellcraft": "intelligence",
    "spot": "wisdom",
    "survival": "wisdom",
    "swim": "strength",
    "tumble": "dexterity",
    "use_magic_device": "charisma",
    "use_rope": "dexterity"
}

SKILL_USABLE_UNTRAINED = {
    ## all skills; are they usable untrained or not?
    ## True if usable untrained. False if not.
    "appraise": True,
    "balance": True,
    "bluff": True,
    "climb": True,
    "concentration": True,
    "craft": True,
    "decipher_script": False,
    "diplomacy": True,
    "disable_device": False,
    "disguise": True,
    "escape_artist": True,
    "forgery": True,
    "gather_information": True,
    "handle_animal": False,
    "heal": True,
    "hide": True,
    "intimidate": True,
    "jump": True,
    "knowledge": False,
    "listen": True,
    "move_silently": True,
    "open_lock": False,
    "perform": False,
    "profession": False,
    "ride": True,
    "search": True,
    "sense_motive": True,
    "sleight_of_hand": False,
    "spellcraft": False,
    "spot": True,
    "survival": True,
    "swim": True,
    "tumble": False,
    "use_magic_device": True,
    "use_rope": True
}

SKILL_CRAFT = [
    "alchemy",
    "weaponsmithing",
    "armoursmithing",
    "masonry",
    "carpentry",
    "poison",
    "trap",
    "culinary",
    "musical_composition",
    "written_composition"
]

SKILL_KNOWLEDGE = [
    "arcana",
    "engineering",
    "dungeoneering",
    "geography",
    "history",
    "local",
    "nature",
    "nobility",
    "religion",
    "the_planes"
]

SKILL_PERFORM = [
    "act",
    "comedy",
    "dance",
    "keyboard",
    "oratory",
    "percussion",
    "stringed",
    "wind",
    "sing"
]

SKILL_PROFESSION = [
    "academic",
    "apothecary",
    "celebrity",
    "military",
    "criminal",
    "doctor",
    "entrepreneur",
    "investigator",
    "scavenger",
    "religious",
    "transporter",
    "engineer",
    "alchemist",
    "monster_hunter"
]

SKILL_SPEAK_LANGUAGE = [
    "abyssal",  ## Demon and evil creatures written in Infernal
    "aquan",  ## Water based creatures written in elven
    "auran",  ## Air based creatures written in draconic
    "celestial",  ## Good outsiders written in celestial
    "common",  # English
    "draconic",  # Kobolds, Troglodytes, Lizardfolk and Dragons
    "druidic",  # Druids ONLY!!!
    "dwarven",
    "elven",
    "giant",  # Ogres and giants
    "gnome",
    "goblin",  # Goblins, hobgoblins and bugbears
    "gnoll",
    "halfling",
    "ignan",  # Fire based creatures written in infernal
    "orcish",  # Written in Orcish
    "sylvan",  # Dryads, brownies, leprechauns written in elven
    "terran",  # Xorns and earth based creatures written in dwarven
    "undercommon"  # Drow written in elven
]

NON_MULTIAREA_SKILLS = [
    ## ALLL SKILLS EXCEPT CRAFT, PROFESSION, PERFORM AND KNOWLEDGE
    "appraise",
    "balance",
    "bluff",
    "climb",
    "concentration",
    "decipher_script",
    "diplomacy",
    "disable_device",
    "disguise",
    "escape_artist",
    "forgery",
    "gather_information",
    "handle_animal",
    "heal",
    "hide",
    "intimidate",
    "jump",
    "listen",
    "move_silently",
    "open_lock",
    "ride",
    "search",
    "sense_motive",
    "sleight_of_hand",
    "spellcraft",
    "spot",
    "survival",
    "swim",
    "tumble",
    "use_magic_device",
    "use_rope"
]

MULTIAREA_SKILLS = []

str = ""
for category in MULTIAREA_SKILL_CATEGORIES:
    if category == "craft":
        for skill in SKILL_CRAFT:
            str = "%s_%s" % (category, skill)
            MULTIAREA_SKILLS.append(str)
    if category == "knowledge":
        for skill in SKILL_KNOWLEDGE:
            str = "%s_%s" % (category, skill)
            MULTIAREA_SKILLS.append(str)
    if category == "perform":
        for skill in SKILL_PERFORM:
            str = "%s_%s" % (category, skill)
            MULTIAREA_SKILLS.append(str)
    if category == "profession":
        for skill in SKILL_PROFESSION:
            str = "%s_%s" % (category, skill)
            MULTIAREA_SKILLS.append(str)

ALL_STANDARD_SKILLS = NON_MULTIAREA_SKILLS + MULTIAREA_SKILLS


def test_1():
    print(ALL_STANDARD_SKILLS)


if __name__ == "__main__":
    test_1()
