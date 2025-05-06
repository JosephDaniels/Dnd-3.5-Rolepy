import tkinter as tk
from ui.pointbuy_window import Point_Buy_Window
from ui.roll_attributes_window import Roll_Attributes_Window
from ui.appearance_window import AppearanceWindow

class Roll_or_Point_Buy_Prompt(tk.Toplevel):
    def __init__(self, master, character):
        super().__init__(master)
        self.character = character
        self.master = master
        self.title("Choose Stat Generation Method")
        self.configure(bg="#1e1e1e")
        self.create_widgets()

    def create_widgets(self):
        row = 0
        info = ("How would you like to generate your character's attributes?\n"
                "\nPoint Buy: Choose where to assign your points.\n"
                "Roll for Stats: Roll 4d6, drop the lowest. Random and chaotic.")

        tk.Label(self, text=info, justify="left", bg="#1e1e1e", fg="white", wraplength=400).grid(column=0, row=row, columnspan=2, pady=15, padx=15)
        row += 1

        tk.Button(self, text='Point Buy', width=20, command=self.open_point_buy_window).grid(column=0, row=row, padx=20, pady=10)
        tk.Button(self, text='Roll for Stats', width=20, command=self.open_roll_attributes_window).grid(column=1, row=row, padx=20, pady=10)

    def open_point_buy_window(self):
        self.destroy()
        Point_Buy_Window(self.master, self.character, on_complete=lambda: self.open_appearance_window())

    def open_roll_attributes_window(self):
        self.destroy()
        Roll_Attributes_Window(self.master, self.character)

    def open_appearance_window(self):
        AppearanceWindow(self.master, self.character)
