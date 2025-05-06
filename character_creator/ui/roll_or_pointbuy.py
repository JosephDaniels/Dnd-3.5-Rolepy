import tkinter as tk
from ui.attribute_window import Point_Buy_Window, Roll_Attributes_Window

class Roll_or_Point_Buy_Prompt(tk.Toplevel):
    def __init__(self, master, character):
        super().__init__(master)
        self.character = character
        self.master = master
        self.title("Choose Stat Generation Method")
        self.create_widgets()

    def create_widgets(self):
        row = 0
        info = ("How would you like to generate your character's attributes?\n"
                "Point Buy lets you choose where points go.\n"
                "Classic Roll randomly rolls 4d6 and drops the lowest.")

        tk.Label(self, text=info, justify="left").grid(column=0, row=row, columnspan=2, pady=10)
        row += 1

        tk.Button(self, text='Point Buy', width=20, command=self.open_point_buy_window).grid(column=0, row=row, padx=5, pady=5)
        tk.Button(self, text='Classic Roll', width=20, command=self.open_roll_attributes_window).grid(column=1, row=row, padx=5, pady=5)

    def open_point_buy_window(self):
        self.master.attribute_window = Point_Buy_Window(self.master, self.character)
        self.destroy()

    def open_roll_attributes_window(self):
        self.master.attribute_window = Roll_Attributes_Window(self.master, self.character)
        self.destroy()
