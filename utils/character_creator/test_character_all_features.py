from src.character.charactersheet import Character

# Setup
char = Character(name="Multitest McGee")
char.strength = 16
char.dexterity = 12
char.constitution = 14
char.intelligence = 10
char.wisdom = 8
char.charisma = 13

char.identity.age = 30
char.identity.gender = "Nonbinary"
char.identity.eye_colour = "Blue"
char.identity.hair_colour = "Black"
char.identity.race = "Half-Elf"
char.identity.height = "5'9\""
char.identity.weight = "150 lbs"
char.identity.build = "Slender"
char.identity.alignment = "Chaotic Good"
char.identity.personality_traits = "Brave and curious"
char.identity.background = "Wanderer"
char.identity.faith = "None"
char.identity.homeland = "Unknown"
char.identity.occupation = "Explorer"
char.identity.languages_spoken = ["Common", "Elvish"]
char.identity.description = "A wanderer with mysterious origins."
char.identity.public_history = "Helped liberate a small village."
char.identity.private_history = "Is searching for their lost sibling."
char.identity.notable_marks = "Scar across right cheek."

# Load class progression (adjust paths as needed)
barbarian_csv = "models/dnd_classes/dnd35srd_character_class_progression_barbarian.csv"
sorcerer_csv = "models/dnd_classes/dnd35srd_character_class_progression_sorcerer.csv"

try:
    char.load_class_progression("Barbarian", barbarian_csv)
    char.load_class_progression("Sorcerer", sorcerer_csv)

    # Add levels
    char.add_class_level("Barbarian")
    char.add_class_level("Sorcerer")
    char.add_class_level("Sorcerer")

    # Save to file
    char.save_to_json()

    # Reload from file
    filepath = f"characters/{char.name.lower().replace(' ', '_')}.json"
    reloaded = Character.from_json(filepath)

    # Tests
    assert reloaded.name == char.name
    assert reloaded.identity.age == 30
    assert reloaded.identity.race == "Half-Elf"
    assert reloaded.classes == {"Barbarian": 1, "Sorcerer": 2}
    assert "fast_movement" in reloaded.special_abilities
    assert "summon_familiar" in reloaded.special_abilities
    assert reloaded.total_level() == 3
    assert reloaded.strength == 16

    print("✅ All tests passed!")

except FileNotFoundError as e:
    print(f"❌ Missing CSV file: {e}")

except AssertionError as e:
    print(f"❌ Test failed: {e}")

except Exception as e:
    print(f"❌ Unexpected error: {e}")
