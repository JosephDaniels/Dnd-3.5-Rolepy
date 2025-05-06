from character.character import Character

def calculate_modifier(score):
    return (score - 10) // 2

def test_character():
    print("🔥 Initializing test character...")
    char = Character(name="Testa the Unbreakable")
    char.character_class = ["Barbarian", "Sorcerer"]
    char.identity.update({
        "race": "Half-Orc",
        "age": "25",
        "gender": "Female",
        "eye_colour": "Amber",
        "hair_colour": "White",
        "skin_colour": "Green",
        "height": "6'2\"",
        "weight": "210 lbs",
        "build": "Muscular"
    })

    char.strength = 18
    char.dexterity = 14
    char.constitution = 16
    char.intelligence = 10
    char.wisdom = 8
    char.charisma = 12

    char.feats = ["Power Attack", "Cleave"]
    char.special_abilities = ["Rage", "Darkvision"]
    char.xp = 3200

    char.description = "A fierce warrior with a shadowy past."
    char.public_history = "Known for slaying the Scaled Wyrm of Karthuun."
    char.private_history = "Actually raised by monks who trained her in secret arts."

    print("🎯 Stats and modifiers:")
    for attr in ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']:
        val = getattr(char, attr)
        print(f"  {attr.capitalize()}: {val} (Modifier: {calculate_modifier(val)})")

    print("\n🎭 Identity details:")
    for key, value in char.identity.items():
        print(f"  {key}: {value}")

    print("\n🧰 Feats and Abilities:")
    print("  Feats:", ", ".join(char.feats))
    print("  Abilities:", ", ".join(char.special_abilities))
    print("  XP:", char.xp)

    print("\n💾 Saving character...")
    char.save_to_json()

    print("\n📤 Loading character back from JSON...")
    loaded = Character.from_json("../characters/testa_the_unbreakable.json")

    print("\n✅ Verifying description and history files loaded correctly:")
    print("  Description:", loaded.description)
    print("  Public History:", loaded.public_history)
    print("  Private History:", loaded.private_history)

    print("\n⚠️ Testing edge case: save without name")
    try:
        nameless = Character()
        nameless.save_to_json()
    except ValueError as e:
        print("  Caught error as expected:", e)

    print("\n🧪 All tests passed if no uncaught exceptions occurred!")

if __name__ == "__main__":
    test_character()
