import tkinter as tk
from tkinter import messagebox
from models.identity import CharacterIdentity
from ui.character_editor_window import CharacterEditorWindow

class IdealsWindow(tk.Toplevel):
    def __init__(self, master, character):
        super().__init__(master)
        self.master = master
        self.character = character
        self.identity = character.identity
        self.title("Personality & Ideals")
        self.geometry("600x700")
        self.configure(bg="#1e1e1e")

        self.fields = {
            "Personality Traits": [tk.StringVar() for _ in range(3)],
            "Ideals": tk.StringVar(value=self.identity.ideals),
            "Bonds": tk.StringVar(value=self.identity.bonds),
            "Flaws": tk.StringVar(value=self.identity.flaws),
            "Background": tk.StringVar(value=self.identity.background),
            "Alignment": tk.StringVar(value=self.identity.alignment),
            "Faith": tk.StringVar(value=self.identity.faith),
            "Homeland": tk.StringVar(value=self.identity.homeland)
        }

        for label_text, var in self.fields.items():
            frame = tk.Frame(self, bg="#1e1e1e")
            frame.pack(pady=4, padx=10, fill=tk.X)
            tk.Label(frame, text=label_text, width=20, anchor="w", bg="#1e1e1e", fg="white").pack(side=tk.LEFT)

            if label_text == "Personality Traits":
                for i, trait_var in enumerate(var):
                    dropdown = tk.OptionMenu(frame, trait_var, *CharacterIdentity.PERSONALITY_TRAITS)
                    dropdown.config(width=15)
                    dropdown.pack(side=tk.LEFT, padx=2)
            elif label_text == "Ideals":
                tk.OptionMenu(frame, var, *CharacterIdentity.IDEALS).pack(side=tk.LEFT)
            elif label_text == "Bonds":
                tk.OptionMenu(frame, var, *CharacterIdentity.BONDS).pack(side=tk.LEFT)
            elif label_text == "Flaws":
                tk.OptionMenu(frame, var, *CharacterIdentity.FLAWS).pack(side=tk.LEFT)
            elif label_text == "Background":
                tk.OptionMenu(frame, var, *CharacterIdentity.BACKGROUNDS).pack(side=tk.LEFT)
            else:
                tk.Entry(frame, textvariable=var, width=45).pack(side=tk.LEFT)

        tk.Button(self, text="Finish Character", command=self.finish).pack(pady=20)

    def finish(self):
        self.identity.personality_traits = ", ".join(var.get() for var in self.fields["Personality Traits"])
        self.identity.ideals = self.fields["Ideals"].get()
        self.identity.bonds = self.fields["Bonds"].get()
        self.identity.flaws = self.fields["Flaws"].get()
        self.identity.background = self.fields["Background"].get()
        self.identity.alignment = self.fields["Alignment"].get()
        self.identity.faith = self.fields["Faith"].get()
        self.identity.homeland = self.fields["Homeland"].get()

        self.destroy()
        CharacterEditorWindow(self.master, self.character)
