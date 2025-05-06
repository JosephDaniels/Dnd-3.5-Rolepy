from character.character import Character

# Setup test character
c = Character("Testa Multiclass")
c.load_class_progression("Barbarian", "models/dnd_classes/dnd35srd_character_class_progression_barbarian.csv")
c.load_class_progression("Sorcerer", "models/dnd_classes/dnd35srd_character_class_progression_sorcerer.csv")

# Test leveling
print("\n-- Adding 1 level of Barbarian --")
c.add_class_level("Barbarian")
print("\n-- Adding 2 levels of Sorcerer --")
c.add_class_level("Sorcerer")
c.add_class_level("Sorcerer")

# Output final state
print("\n=== Final Character Summary ===")
print(f"Name: {c.name}")
print(f"Classes: {c.classes}")
print(f"Level: {c.total_level()}")
print(f"Special Abilities: {c.special_abilities}")
