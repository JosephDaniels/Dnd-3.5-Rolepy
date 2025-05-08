import tkinter as tk
from tkinter import messagebox
from ui.appearance_window import AppearanceWindow
import random

class Roll_Attributes_Window(tk.Toplevel):
    def __init__(self, master, character):
        super().__init__(master)
        self.master = master
        self.character = character
        self.title("Roll for Attributes")
        self.geometry("400x400")
        self.configure(bg="#1e1e1e")

        self.stats = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
        self.values = []
        self.stat_vars = {}

        tk.Label(self, text="Rolled Values:", font=("Helvetica", 12), bg="#1e1e1e", fg="white").pack(pady=10)
        self.values_frame = tk.Frame(self, bg="#1e1e1e")
        self.values_frame.pack()

        self.assign_frame = tk.Frame(self, bg="#1e1e1e")
        self.assign_frame.pack(pady=10)

        self.roll_button = tk.Button(self, text="Roll Stats", command=self.roll_stats)
        self.roll_button.pack(pady=10)

        self.confirm_button = tk.Button(self, text="Confirm", command=self.confirm)
        self.confirm_button.pack(pady=10)

        for stat in self.stats:
            row = tk.Frame(self.assign_frame, bg="#1e1e1e")
            row.pack(pady=2)
            tk.Label(row, text=stat + ":", width=12, anchor="w", bg="#1e1e1e", fg="white").pack(side=tk.LEFT)
            var = tk.StringVar()
            dropdown = tk.OptionMenu(row, var, "")
            dropdown.config(width=4)
            dropdown.pack(side=tk.LEFT)
            self.stat_vars[stat] = (var, dropdown)

    def roll_stats(self):
        self.values = [self.roll_4d6_drop_lowest() for _ in range(6)]

        for widget in self.values_frame.winfo_children():
            widget.destroy()
        for val in self.values:
            tk.Label(self.values_frame, text=str(val), font=("Helvetica", 12), width=4, bg="#2e2e2e", fg="white").pack(side=tk.LEFT, padx=4)

        for stat, (var, dropdown) in self.stat_vars.items():
            menu = dropdown["menu"]
            menu.delete(0, 'end')
            for v in self.values:
                menu.add_command(label=v, command=lambda value=v, s=stat: self.stat_vars[s][0].set(value))
            var.set("")

    def roll_4d6_drop_lowest(self):
        rolls = sorted([random.randint(1, 6) for _ in range(4)])
        return sum(rolls[1:])

    def confirm(self):
        assigned_values = [var.get() for var, _ in self.stat_vars.values()]
        if "" in assigned_values:
            messagebox.showerror("Incomplete", "Please assign all values.")
            return

        remaining_pool = self.values[:]
        for val in assigned_values:
            if int(val) in remaining_pool:
                remaining_pool.remove(int(val))
            else:
                messagebox.showerror("Invalid Assignment", f"You assigned {val} more times than it was rolled.")
                return

        for stat, (var, _) in self.stat_vars.items():
            setattr(self.character, stat.lower(), int(var.get()))

        self.destroy()
        AppearanceWindow(self.master, self.character)
