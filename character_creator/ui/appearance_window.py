import tkinter as tk
from tkinter import messagebox
from ui.character_editor_window import CharacterEditorWindow
from ui.ideals_window import IdealsWindow

class AppearanceWindow(tk.Toplevel):
    def __init__(self, master, character):
        super().__init__(master)
        self.master = master
        self.character = character
        self.identity = character.identity
        self.title("Appearance")
        self.geometry("500x600")
        self.configure(bg="#1e1e1e")

        self.fields = {
            "Eye Colour": tk.StringVar(value=self.identity.eye_colour),
            "Hair Colour": tk.StringVar(value=self.identity.hair_colour),
            "Skin Colour": tk.StringVar(value=self.identity.skin_colour),
            "Height": tk.StringVar(value=self.identity.height),
            "Weight": tk.StringVar(value=self.identity.weight),
            "Build": tk.StringVar(value=self.identity.build),
            "Notable Marks": tk.StringVar(value=self.identity.notable_marks),
            "Description": tk.StringVar(value=self.identity.description)
        }

        for label_text, var in self.fields.items():
            frame = tk.Frame(self, bg="#1e1e1e")
            frame.pack(pady=4, padx=10, fill=tk.X)
            tk.Label(frame, text=label_text, width=18, anchor="w", bg="#1e1e1e", fg="white").pack(side=tk.LEFT)

            if label_text in ["Eye Colour", "Hair Colour", "Skin Colour", "Build"]:
                options = []
                if label_text == "Eye Colour":
                    options = [
                        "Blue", "Green", "Hazel", "Brown", "Black", "Gray", "Amber",
                        "Red", "Violet", "Yellow", "Gold", "Silver", "White", "Pink",
                        "Heterochromia", "Glowing", "Multicolour"
                    ]
                elif label_text == "Hair Colour":
                    options = [
                        "Black", "Brown", "Blonde", "Red", "Gray", "White", "Bald",
                        "Auburn", "Silver", "Blue", "Green", "Pink", "Purple", "Orange",
                        "Streaked", "Glowing", "Multicolour"
                    ]
                elif label_text == "Skin Colour":
                    options = [
                        "Pale", "Fair", "Tan", "Olive", "Brown", "Dark", "Ebony",
                        "Albino", "Gray", "Green", "Blue", "Purple", "Red", "Scaled",
                        "Furred", "Metallic", "Translucent"
                    ]
                elif label_text == "Build":
                    options = [
                        "Slim", "Average", "Muscular", "Stocky", "Curvy", "Lean",
                        "Petite", "Lanky", "Heavyset", "Broad", "Athletic", "Gaunt",
                        "Bulky", "Amorphous", "Otherworldly"
                    ]

                dropdown = tk.OptionMenu(frame, var, *options)
                dropdown.config(width=37)
                dropdown.pack(side=tk.LEFT)
            else:
                tk.Entry(frame, textvariable=var, width=40).pack(side=tk.LEFT)

        tk.Button(self, text="Continue to Ideals", command=self.finish).pack(pady=20)

    def finish(self):
        self.identity.eye_colour = self.fields["Eye Colour"].get()
        self.identity.hair_colour = self.fields["Hair Colour"].get()
        self.identity.skin_colour = self.fields["Skin Colour"].get()
        self.identity.height = self.fields["Height"].get()
        self.identity.weight = self.fields["Weight"].get()
        self.identity.build = self.fields["Build"].get()
        self.identity.notable_marks = self.fields["Notable Marks"].get()
        self.identity.description = self.fields["Description"].get()

        self.destroy()
        IdealsWindow(self.master, self.character)
