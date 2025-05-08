# test_identity.py

from identity import CharacterIdentity

def main():
    # 1) Inspect the raw data collections
    print("– PERSONALITY_TRAITS:")
    for name, desc in CharacterIdentity.PERSONALITY_TRAITS[:3]:
        print(f"  • {name}: {desc}")
    print("  ...")

    print("\n– IDEALS:")
    for name, desc in CharacterIdentity.IDEALS[:3]:
        print(f"  • {name}: {desc}")
    print("  ...")

    print("\n– BONDS:")
    for name, desc in CharacterIdentity.BONDS[:3]:
        print(f"  • {name}: {desc}")
    print("  ...")

    print("\n– FLAWS:")
    for name, desc in CharacterIdentity.FLAWS[:3]:
        print(f"  • {name}: {desc}")
    print("  ...")

    print("\n– BACKGROUNDS:")
    for name, desc in CharacterIdentity.BACKGROUNDS[:3]:
        print(f"  • {name}: {desc}")
    print("  ...\n")

    # 2) Instantiate a sample character
    sample = CharacterIdentity(
        name="Arwen Evenstar",
        race="Elf",
        age=2901,
        gender="Female",
        alignment="Neutral Good",
        background="Noble",
        personality_traits=[CharacterIdentity.PERSONALITY_TRAITS[0], CharacterIdentity.PERSONALITY_TRAITS[4]],
        ideals=[CharacterIdentity.IDEALS[1]],      # Freedom
        bonds=[CharacterIdentity.BONDS[0]],        # Family
        flaws=[CharacterIdentity.FLAWS[2]],        # Spoiled
    )

    # 3) Dump its dict form
    print("Sample Character Instance:\n", sample.to_dict())

if __name__ == "__main__":
    main()
