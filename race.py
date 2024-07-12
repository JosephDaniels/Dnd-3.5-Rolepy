STANDARD_CHARACTER_RACES = ['human', 'dwarf', 'half orc', 'gnome', 'halfling',
                            'high elf']  # the standard elf is technically a moon elf.

ELVEN_RACES = ['moon elf', 'sun elf', 'night elf', 'wood elf', 'blood elf']

NONSTANDARD_CHARACTER_RACES = ['dragonborn', 'tiefling', 'tabaxi']

EVIL_CHARACTER_RACES = ['drow', 'orc', 'goblin', 'gnoll', 'kobold', 'demon', 'vampire']

ALL_NONEVIL_CHARACTER_RACES = STANDARD_CHARACTER_RACES + ELVEN_RACES + NONSTANDARD_CHARACTER_RACES

ALL_CHARACTER_RACES = STANDARD_CHARACTER_RACES + \
                      ELVEN_RACES + \
                      NONSTANDARD_CHARACTER_RACES + \
                      EVIL_CHARACTER_RACES

RACE_BENEFITS = {
    "human": ("human_bonus_feat",
              "skill_points_per_level+1",
              "skill_points_at_first_level+4"),
    "dwarf": ("bonus_language_dwarven",
              "constitution+2",
              "charisma-2",
              "darkvision",
              "stonecunning",
              "weapon_proficiency_dwarven_waraxe",
              "weapon_proficiency_dwarven_urgrosh",
              "dwarven_stability",
              "poison_resistance+2",
              "saving_throw_vs_spells+2",
              "attack_bonus_vs_orcs+1",
              "attack_bonus_vs_goblins+1",
              "dodge_bonus_vs_giants+4",
              "appraise_stone+2",
              "appraise_metal+2",),
    "half orc": ("bonus_lanuage_orcish",
                 "strength+2",
                 "intelligence-2",
                 "charisma-2",
                 "darkvision",
                 "orc blood"),
    "gnome": ("bonus_language_gnomish",
              "constitution+2",
              "strength-2",
              "small",
              "low_light_vision",
              "saving_throw_vs_illusions+2",
              "weapon_proficiency_gnome_hooked_hammer",
              "illusion_spell_save_DC+1",
              "attack_bonus_vs_goblins+1",
              "attack_bonus_vs_kobolds+1",
              "dodge_bonus_vs_giants+4",
              "listen_bonus+2",
              "craft_alchemy_bonus+2",
              "speak_with_animals_once_per_day"),
    "half-elf": ("bonus_language_elven",
                 "sleep_effect_immunity",
                 "low_light_vision",
                 "listen_bonus+1",
                 "spot_bonus+1",
                 "search_bonus+1",
                 "diplomacy_bonus+2",
                 "diplomacy_bonus+2",
                 "elven_blood"),
    "halfling": ("bonus_language_halfling",
                 "small",
                 "climb_bonus+2",
                 "jump_bonus+2",
                 "move_silently_bonus+2",
                 "saving_throw_bonus+1",
                 "bonus_vs_fear+2",
                 "attack_bonus_slings+1",
                 "attack_bonus_thrown_weapons+1",
                 "listen_bonus+2"
                 ),
    "high elf": ("bonus_language_elven",
                 "dexterity+2",
                 "constitution-2",
                 "sleep_effect_immunity",
                 "saving_throw_vs_enchantment+2",
                 "low_light_vision",
                 "weapon_proficiency_longbow",
                 "weapon_proficiency_shortbow",
                 "weapon_proficiency_rapier",
                 "weapon_proficiency_longsword",
                 "listen_bonus+2",
                 "search_bonus+2",
                 "spot_bonus+2",
                 "secret_portal_sense")
}
