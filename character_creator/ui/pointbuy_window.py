import tkinter as tk
from tkinter import messagebox
from ui.appearance_window import AppearanceWindow

class Point_Buy_Window(tk.Toplevel):
    def __init__(self, master, character, on_complete=None):
        super().__init__(master)
        self.master = master
        self.character = character
        self.on_complete = on_complete
        self.title("Point Buy Attribute Assignment")
        self.geometry("500x400")
        self.configure(bg="#1e1e1e")

        self.points_remaining = 27
        self.stats = {"Strength": 8, "Dexterity": 8, "Constitution": 8, "Intelligence": 8, "Wisdom": 8, "Charisma": 8}
        self.stat_vars = {}

        self.header = tk.Label(self, text=f"Points Remaining: {self.points_remaining}", font=("Helvetica", 14), bg="#1e1e1e", fg="white")
        self.header.pack(pady=10)

        for stat in self.stats:
            frame = tk.Frame(self, bg="#1e1e1e")
            frame.pack(pady=5)

            tk.Label(frame, text=stat + ":", width=12, anchor="w", bg="#1e1e1e", fg="white").pack(side=tk.LEFT)

            minus_btn = tk.Button(frame, text="-", command=lambda s=stat: self.adjust_stat(s, -1), width=2)
            minus_btn.pack(side=tk.LEFT, padx=2)

            var = tk.IntVar(value=self.stats[stat])
            self.stat_vars[stat] = var
            tk.Label(frame, textvariable=var, width=3, bg="#2e2e2e", fg="white").pack(side=tk.LEFT, padx=2)

            plus_btn = tk.Button(frame, text="+", command=lambda s=stat: self.adjust_stat(s, 1), width=2)
            plus_btn.pack(side=tk.LEFT, padx=2)

        tk.Button(self, text="Confirm", command=self.confirm).pack(pady=20)

    def cost(self, score):
        if score <= 13:
            return score - 8
        return 5 + 2 * (score - 14)

    def adjust_stat(self, stat, delta):
        current = self.stat_vars[stat].get()
        new_score = current + delta
        if 8 <= new_score <= 18:
            new_total = sum(self.cost(v.get()) for v in self.stat_vars.values()) + self.cost(new_score) - self.cost(current)
            if new_total <= 27:
                self.stat_vars[stat].set(new_score)
                self.points_remaining = 27 - sum(self.cost(v.get()) for v in self.stat_vars.values())
                self.header.config(text=f"Points Remaining: {self.points_remaining}")

    def confirm(self):
        if self.points_remaining != 0:
            messagebox.showwarning("Unspent Points", "Please use all 27 points before confirming.")
            return

        self.character.strength = self.stat_vars["Strength"].get()
        self.character.dexterity = self.stat_vars["Dexterity"].get()
        self.character.constitution = self.stat_vars["Constitution"].get()
        self.character.intelligence = self.stat_vars["Intelligence"].get()
        self.character.wisdom = self.stat_vars["Wisdom"].get()
        self.character.charisma = self.stat_vars["Charisma"].get()

        self.destroy()
        if self.on_complete:
            self.on_complete()
