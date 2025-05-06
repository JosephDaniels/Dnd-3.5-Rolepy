import tkinter as tk
from tkinter import messagebox
from models.character import Character


class CharacterEditorWindow(tk.Toplevel):
    def __init__(self, master, character: Character):
        super().__init__(master)
        self.character = character
        self.title(f"Editing {self.character.name}")
        self.geometry("800x600")

        import tkinter.ttk as ttk
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")

        identity_tab = tk.Frame(notebook)
        stats_tab = tk.Frame(notebook)
        backstory_tab = tk.Frame(notebook)

        notebook.add(identity_tab, text="Identity")
        notebook.add(stats_tab, text="Attributes")
        notebook.add(backstory_tab, text="Backstory")

        self.fields = {
            "Name": tk.StringVar(value=self.character.name),
            "Race": tk.StringVar(value=self.character.identity.race),
            "Class": tk.StringVar(value=", ".join(self.character.character_class)),
            "Age": tk.StringVar(value=str(self.character.identity.age)),
            "Gender": tk.StringVar(value=self.character.identity.gender),
            "Eye Colour": tk.StringVar(value=self.character.identity.eye_colour),
            "Hair Colour": tk.StringVar(value=self.character.identity.hair_colour),
            "Skin Colour": tk.StringVar(value=self.character.identity.skin_colour),
            "Height": tk.StringVar(value=self.character.identity.height),
            "Weight": tk.StringVar(value=self.character.identity.weight),
            "Build": tk.StringVar(value=self.character.identity.build),
            "Alignment": tk.StringVar(value=self.character.identity.alignment),
            "Background": tk.StringVar(value=self.character.identity.background),
            "Personality Traits": tk.StringVar(value=self.character.identity.personality_traits),
            "Ideals": tk.StringVar(value=self.character.identity.ideals),
            "Bonds": tk.StringVar(value=self.character.identity.bonds),
            "Flaws": tk.StringVar(value=self.character.identity.flaws),
            "Homeland": tk.StringVar(value=self.character.identity.homeland),
            "Faith": tk.StringVar(value=self.character.identity.faith),
            "Occupation": tk.StringVar(value=self.character.identity.occupation),
            "Languages Spoken": tk.StringVar(value=", ".join(self.character.identity.languages_spoken)),
            "Notable Marks": tk.StringVar(value=self.character.identity.notable_marks),
            "Description": tk.StringVar(value=self.character.identity.description),
            "Public History": tk.StringVar(value=self.character.identity.public_history),
            "Private History": tk.StringVar(value=self.character.identity.private_history),
        }

        self.entries = {}
        def add_fields_to(tab, field_names):
            row = 0
            for label in field_names:
                var = self.fields[label]
                tk.Label(tab, text=label).grid(row=row, column=0, sticky="e", padx=5, pady=2)
                entry = tk.Entry(tab, textvariable=var, width=40)
                entry.grid(row=row, column=1, sticky="w", padx=5, pady=2)
                self.entries[label] = entry
                row += 1

        add_fields_to(identity_tab, [
            "Name", "Race", "Class", "Age", "Gender", "Eye Colour",
            "Hair Colour", "Skin Colour", "Height", "Weight", "Build",
            "Alignment", "Background"
        ])

        add_fields_to(stats_tab, [
            "Personality Traits", "Ideals", "Bonds", "Flaws",
            "Homeland", "Faith", "Occupation", "Languages Spoken"
        ])

        add_fields_to(backstory_tab, [
            "Notable Marks", "Description", "Public History", "Private History"
        ])

        row = len(self.fields) + 2
        self.attributes = {}
        tk.Label(stats_tab, text="Core Attributes", font=("Arial", 10, "bold")).grid(row=row, columnspan=2, pady=(10, 0))
        row += 1
        default_attrs = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
        for attr in default_attrs:
            value = getattr(self.character, attr, 10)
            label = attr.capitalize()
            tk.Label(stats_tab, text=label).grid(row=row, column=0, sticky="e")
            var = tk.IntVar(value=value)
            spinbox = tk.Spinbox(stats_tab, from_=1, to=30, width=5, textvariable=var)
            spinbox.grid(row=row, column=1, sticky="w")
            self.attributes[label] = var
            row += 1

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Save", command=self.save_character).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Close", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def save_character(self):
        self.character.name = self.fields["Name"].get()
        self.character.identity.race = self.fields["Race"].get()
        self.character.character_class = [cls.strip() for cls in self.fields["Class"].get().split(",") if cls.strip()]

        self.character.identity.age = int(self.fields["Age"].get()) if self.fields["Age"].get().isdigit() else -1
        self.character.identity.gender = self.fields["Gender"].get()
        self.character.identity.eye_colour = self.fields["Eye Colour"].get()
        self.character.identity.hair_colour = self.fields["Hair Colour"].get()
        self.character.identity.skin_colour = self.fields["Skin Colour"].get()
        self.character.identity.height = self.fields["Height"].get()
        self.character.identity.weight = self.fields["Weight"].get()
        self.character.identity.build = self.fields["Build"].get()

        # Save attributes
        for attr, var in self.attributes.items():
            value = int(var.get())
            attr_name = attr.lower()
            setattr(self.character, attr_name, value)

        self.character.identity.alignment = self.fields["Alignment"].get()
        self.character.identity.background = self.fields["Background"].get()
        self.character.identity.personality_traits = self.fields["Personality Traits"].get()
        self.character.identity.ideals = self.fields["Ideals"].get()
        self.character.identity.bonds = self.fields["Bonds"].get()
        self.character.identity.flaws = self.fields["Flaws"].get()
        self.character.identity.homeland = self.fields["Homeland"].get()
        self.character.identity.faith = self.fields["Faith"].get()
        self.character.identity.occupation = self.fields["Occupation"].get()
        self.character.identity.languages_spoken = [lang.strip() for lang in self.fields["Languages Spoken"].get().split(",") if lang.strip()]
        self.character.identity.notable_marks = self.fields["Notable Marks"].get()
        self.character.identity.description = self.fields["Description"].get()
        self.character.identity.public_history = self.fields["Public History"].get()
        self.character.identity.private_history = self.fields["Private History"].get()

        try:
            self.character.save_to_json()
            messagebox.showinfo("Success", f"{self.character.name} saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save character: {e}")
