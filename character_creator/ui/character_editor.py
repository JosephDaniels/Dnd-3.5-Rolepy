import tkinter as tk
from tkinter import messagebox, scrolledtext
import os
from character import Character

class Character_Editor_Window(tk.Toplevel):
    def __init__(self, master, character: Character):
        super().__init__(master)
        self.character = character
        self.original_filename = character.name.lower().replace(" ", "_") + ".json"
        self.title(f"Editing {self.character.name}")

        self.field_vars = {
            "Name": tk.StringVar(value=character.name),
            "Race": tk.StringVar(value=character.race),
            "Class": tk.StringVar(value=", ".join(character.character_class)),
            "Age": tk.StringVar(value=str(character.character_identity.get("age", ""))),
            "Gender": tk.StringVar(value=character.character_identity.get("gender", "")),
            "Eye Colour": tk.StringVar(value=character.character_identity.get("eye_colour", "")),
            "Hair Colour": tk.StringVar(value=character.character_identity.get("hair_colour", "")),
            "Skin Colour": tk.StringVar(value=character.character_identity.get("skin_colour", "")),
            "Height": tk.StringVar(value=character.character_identity.get("height", "")),
            "Weight": tk.StringVar(value=character.character_identity.get("weight", "")),
            "Build": tk.StringVar(value=character.character_identity.get("build", "")),
            "Strength": tk.StringVar(value=str(character.strength)),
            "Dexterity": tk.StringVar(value=str(character.dexterity)),
            "Constitution": tk.StringVar(value=str(character.constitution)),
            "Intelligence": tk.StringVar(value=str(character.intelligence)),
            "Wisdom": tk.StringVar(value=str(character.wisdom)),
            "Charisma": tk.StringVar(value=str(character.charisma))
        }

        self.description_box = scrolledtext.ScrolledText(self, width=60, height=4)
        self.description_box.insert("1.0", character.description)

        self.public_history_box = scrolledtext.ScrolledText(self, width=60, height=4)
        self.public_history_box.insert("1.0", character.public_history)

        self.private_history_box = scrolledtext.ScrolledText(self, width=60, height=4)
        self.private_history_box.insert("1.0", character.private_history)

        row = 0
        for label, var in self.field_vars.items():
            tk.Label(self, text=label).grid(row=row, column=0, sticky="e")
            tk.Entry(self, textvariable=var).grid(row=row, column=1, sticky="w")
            row += 1

        tk.Label(self, text="Description:").grid(row=row, column=0, sticky="ne")
        self.description_box.grid(row=row, column=1)
        row += 1

        tk.Label(self, text="Public History:").grid(row=row, column=0, sticky="ne")
        self.public_history_box.grid(row=row, column=1)
        row += 1

        tk.Label(self, text="Private History:").grid(row=row, column=0, sticky="ne")
        self.private_history_box.grid(row=row, column=1)
        row += 1

        tk.Button(self, text="Save", command=self.save_character).grid(row=row, column=0)
        tk.Button(self, text="Close", command=self.destroy).grid(row=row, column=1)

    def save_character(self):
        new_name = self.field_vars["Name"].get()
        new_filename = new_name.lower().replace(" ", "_") + ".json"

        self.character.name = new_name
        self.character.race = self.field_vars["Race"].get()
        self.character.character_class = [cls.strip() for cls in self.field_vars["Class"].get().split(",") if cls.strip()]

        identity = self.character.character_identity
        identity["age"] = int(self.field_vars["Age"].get()) if self.field_vars["Age"].get().isdigit() else -1
        identity["gender"] = self.field_vars["Gender"].get()
        identity["eye_colour"] = self.field_vars["Eye Colour"].get()
        identity["hair_colour"] = self.field_vars["Hair Colour"].get()
        identity["skin_colour"] = self.field_vars["Skin Colour"].get()
        identity["height"] = self.field_vars["Height"].get()
        identity["weight"] = self.field_vars["Weight"].get()
        identity["build"] = self.field_vars["Build"].get()

        self.character.strength = int(self.field_vars["Strength"].get())
        self.character.dexterity = int(self.field_vars["Dexterity"].get())
        self.character.constitution = int(self.field_vars["Constitution"].get())
        self.character.intelligence = int(self.field_vars["Intelligence"].get())
        self.character.wisdom = int(self.field_vars["Wisdom"].get())
        self.character.charisma = int(self.field_vars["Charisma"].get())

        self.character.description = self.description_box.get("1.0", "end").strip()
        self.character.public_history = self.public_history_box.get("1.0", "end").strip()
        self.character.private_history = self.private_history_box.get("1.0", "end").strip()

        try:
            if new_filename != self.original_filename:
                old_path = os.path.join("characters", self.original_filename)
                if os.path.exists(old_path):
                    os.remove(old_path)
            self.character.save_to_json()
            messagebox.showinfo("Saved", f"{self.character.name} saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Save failed: {e}")
