import os
import tkinter as tk
from tkinter import ttk, messagebox
from models.character import Character
from ui.roll_or_pointbuy import Roll_or_Point_Buy_Prompt

class ClassRaceGenderWindow(tk.Toplevel):
    def __init__(self, master, full_name):
        super().__init__(master)
        self.master = master
        self.full_name = full_name
        self.title("Choose Class, Race, and Gender")
        self.geometry("450x300")
        self.configure(bg="#1e1e1e")

        self.class_var = tk.StringVar()
        self.race_var = tk.StringVar()
        self.gender_var = tk.StringVar()

        tk.Label(self, text="Choose your class:", bg="#1e1e1e", fg="white").pack(pady=(10, 0))
        self.class_combo = ttk.Combobox(self, textvariable=self.class_var, values=self.get_class_names(), state="readonly")
        self.class_combo.current(0)
        self.class_combo.pack()

        tk.Label(self, text="Choose your race:", bg="#1e1e1e", fg="white").pack(pady=(10, 0))
        self.race_combo = ttk.Combobox(self, textvariable=self.race_var, values=["Human", "Elf", "Dwarf", "Halfling", "Half-Orc", "Tiefling"], state="readonly")
        self.race_combo.current(0)
        self.race_combo.pack()

        tk.Label(self, text="Choose your gender:", bg="#1e1e1e", fg="white").pack(pady=(10, 0))
        self.gender_combo = ttk.Combobox(self, textvariable=self.gender_var, values=["Male", "Female", "Nonbinary", "Other"], state="readonly")
        self.gender_combo.current(0)
        self.gender_combo.pack()

        tk.Button(self, text="Continue", command=self.finish).pack(pady=20)

    def get_class_names(self):
        class_dir = os.path.join("models", "dnd_classes")
        classes = []
        if os.path.exists(class_dir):
            for file in os.listdir(class_dir):
                if file.endswith(".csv") and "progression" in file:
                    name = file.replace("dnd35srd_character_class_progression_", "").replace(".csv", "").title()
                    classes.append(name)
        return sorted(classes)

    def finish(self):
        class_name = self.class_var.get()
        race = self.race_var.get()
        gender = self.gender_var.get()

        if not class_name:
            messagebox.showerror("Error", "Please choose a class.")
            return

        char = Character(self.full_name)
        char.identity.full_name = self.full_name
        char.identity.race = race
        char.identity.gender = gender

        class_key = class_name.lower()
        try:
            filepath = os.path.join("models", "dnd_classes", f"dnd35srd_character_class_progression_{class_key}.csv")
            char.load_class_progression(class_name, filepath)
            char.add_class_level(class_name)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load class progression: {e}")
            return

        self.destroy()
        Roll_or_Point_Buy_Prompt(self.master, char)
