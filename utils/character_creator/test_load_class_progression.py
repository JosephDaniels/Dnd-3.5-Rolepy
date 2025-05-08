import csv
import os

def load_class_progression(filename):
    # No directory gymnastics—just look right here.
    if not os.path.exists(filename):
        print(f"❌ File not found: {filename}")
        return []

    print(f"📄 Loading class from: {os.path.abspath(filename)}")
    levels = []
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            levels.append({
                "level": int(row["level"]),
                "base_attack_bonus": row["base_attack_bonus"],
                "fort": int(row["base_fortitude"]),
                "ref": int(row["base_reflex"]),
                "will": int(row["base_will"]),
                "special": [s.strip() for s in row["special"].split(",")] if row["special"] else []
            })
    return levels

if __name__ == "__main__":
    filename = "models/dnd_classes/dnd35srd_character_class_progression_barbarian.csv"
    levels = load_class_progression(filename)

    if levels:
        print(f"\n✅ Loaded {len(levels)} levels:")
        for lvl in levels:
            print(f"  L{lvl['level']:>2}: BAB {lvl['base_attack_bonus']} | Saves F{lvl['fort']}/R{lvl['ref']}/W{lvl['will']} | Specials: {', '.join(lvl['special'])}")
    else:
        print("❌ No data loaded.")
