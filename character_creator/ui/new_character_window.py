import tkinter as tk
from tkinter import messagebox
from ui.class_race_gender_window import ClassRaceGenderWindow

class NewCharacterWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("New Character Setup")
        self.geometry("450x200")
        self.configure(bg="#1e1e1e")

        self.character_data = {
            "full_name": tk.StringVar()
        }

        self.container = tk.Frame(self, bg="#1e1e1e")
        self.container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.prompt_label = tk.Label(self.container, text="What is your full name, adventurer? (First, Middle, Last)", font=("Helvetica", 12), bg="#1e1e1e", fg="white")
        self.prompt_label.pack(pady=(0, 10))

        self.input_widget = tk.Entry(self.container, textvariable=self.character_data["full_name"])
        self.input_widget.pack()

        self.next_button = tk.Button(self.container, text="Next", command=self.advance)
        self.next_button.pack(pady=20)

    def advance(self):
        name = self.character_data["full_name"].get().strip()
        if not name:
            messagebox.showerror("Error", "You must provide a full name.")
            return

        self.destroy()
        ClassRaceGenderWindow(self.master, name)
