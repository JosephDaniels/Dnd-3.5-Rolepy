import tkinter as tk
from tkinter import messagebox
from character import Character  # ✅

CHARACTER_ATTRIBUTE_ENTRIES = [
    "strength", "dexterity", "constitution",
    "intelligence", "wisdom", "charisma"
]

POINT_BUY_COST = {
    8: 0, 9: 1, 10: 2, 11: 3, 12: 4,
    13: 5, 14: 6, 15: 8, 16: 10, 17: 13, 18: 16
}

POWER_LEVEL_OPTIONS_LIST = {
    "Low-Power": 15,
    "Adventurer": 25,
    "Heroic": 32,
    "Super-Heroic": 50
}

class Point_Buy_Window(tk.Toplevel):
    def __init__(self, master, character: Character):
        super().__init__(master)
        self.character = character
        self.title("Point Buy Attributes")
        self.available_points = 25
        self.attribute_values = {attr: 8 for attr in CHARACTER_ATTRIBUTE_ENTRIES}

        self.vars = {attr: tk.StringVar(value="8") for attr in CHARACTER_ATTRIBUTE_ENTRIES}
        self.point_var = tk.StringVar(value=str(self.available_points))

        self.create_widgets()

    def create_widgets(self):
        row = 0

        tk.Label(self, text="Choose Power Level").grid(row=row, column=0, columnspan=2)
        row += 1

        power_var = tk.StringVar(value="Adventurer")
        power_menu = tk.OptionMenu(self, power_var, *POWER_LEVEL_OPTIONS_LIST.keys(),
                                   command=self.set_power_level)
        power_menu.grid(row=row, column=0, columnspan=2)
        row += 1

        for attr in CHARACTER_ATTRIBUTE_ENTRIES:
            tk.Label(self, text=attr.capitalize()).grid(row=row, column=0)

            tk.Entry(self, textvariable=self.vars[attr], width=5).grid(row=row, column=1)

            tk.Button(self, text="+", command=lambda a=attr: self.modify_stat(a, 1)).grid(row=row, column=2)
            tk.Button(self, text="-", command=lambda a=attr: self.modify_stat(a, -1)).grid(row=row, column=3)
            row += 1

        tk.Label(self, text="Points Remaining:").grid(row=row, column=0)
        tk.Entry(self, textvariable=self.point_var, width=5).grid(row=row, column=1)
        row += 1

        tk.Button(self, text="Accept", command=self.accept).grid(row=row, column=0)
        tk.Button(self, text="Cancel", command=self.destroy).grid(row=row, column=1)

    def set_power_level(self, option):
        self.available_points = POWER_LEVEL_OPTIONS_LIST[option]
        self.point_var.set(str(self.available_points))
        for attr in CHARACTER_ATTRIBUTE_ENTRIES:
            self.attribute_values[attr] = 8
            self.vars[attr].set("8")

    def cost_for(self, value):
        return POINT_BUY_COST.get(value, 999)

    def modify_stat(self, attr, delta):
        current = self.attribute_values[attr]
        new_val = current + delta
        if new_val < 8 or new_val > 18:
            return

        current_cost = self.cost_for(current)
        new_cost = self.cost_for(new_val)
        diff = new_cost - current_cost

        if diff <= self.available_points:
            self.attribute_values[attr] = new_val
            self.available_points -= diff
            self.vars[attr].set(str(new_val))
            self.point_var.set(str(self.available_points))

    def accept(self):
        for attr in CHARACTER_ATTRIBUTE_ENTRIES:
            setattr(self.character, attr, self.attribute_values[attr])
        self.character.save_to_json()
        self.destroy()


class Roll_Attributes_Window(tk.Toplevel):
    def __init__(self, master, character: Character):
        super().__init__(master)
        self.character = character
        self.title("Roll Attributes")

        self.vars = {attr: tk.StringVar(value="0") for attr in CHARACTER_ATTRIBUTE_ENTRIES}

        self.create_widgets()

    def create_widgets(self):
        row = 0

        for attr in CHARACTER_ATTRIBUTE_ENTRIES:
            tk.Label(self, text=attr.capitalize()).grid(row=row, column=0)
            tk.Entry(self, textvariable=self.vars[attr], width=5).grid(row=row, column=1)
            row += 1

        tk.Button(self, text="Roll Stats", command=self.roll_stats).grid(row=row, column=0)
        tk.Button(self, text="Accept", command=self.accept).grid(row=row, column=1)
        tk.Button(self, text="Cancel", command=self.destroy).grid(row=row, column=2)

    def roll_stats(self):
        import random
        for attr in CHARACTER_ATTRIBUTE_ENTRIES:
            rolls = sorted([random.randint(1, 6) for _ in range(4)])[1:]  # drop lowest
            self.vars[attr].set(str(sum(rolls)))

    def accept(self):
        for attr in CHARACTER_ATTRIBUTE_ENTRIES:
            setattr(self.character, attr, int(self.vars[attr].get()))
        self.character.save_to_json()
        self.destroy()
