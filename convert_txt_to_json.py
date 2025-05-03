import os
from character import Character

CHARACTER_FOLDER = "characters"

def convert_all_txt_to_json():
    files = os.listdir(CHARACTER_FOLDER)
    txt_files = [f for f in files if f.endswith(".txt")]

    if not txt_files:
        print("No .txt files found to convert.")
        return

    print(f"Converting {len(txt_files)} files...")
    for txt_file in txt_files:
        name = txt_file.replace(".txt", "")
        try:
            character = Character.from_txt_file(txt_file)
            character.save_to_json()
            print(f"✔ Converted: {txt_file}")
        except Exception as e:
            print(f"✖ Failed to convert {txt_file}: {e}")

    print("Conversion complete.")

if __name__ == "__main__":
    convert_all_txt_to_json()
