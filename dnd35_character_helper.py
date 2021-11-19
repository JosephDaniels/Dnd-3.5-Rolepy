""" A character creator made with TKinter.

It's purpose is to make DnD 3.5 Character creation easier."""

WELCOME_MESSAGE = " Hi there! Welcome to DM Joey's Dungeons and Dragon's 3.5 Edition Character Creator!\n" \
                  "Please select an option from down below."

import random

import tkinter as tk
from tkinter import ttk
root = tk.Tk()
frame = ttk.Frame(root, padding=10)
frame.grid()

CHARACTER_PROFILE_ENTRIES = ["Full Name","Race","Age","Gender",
                             "Eye Colour","Hair Colour","Skin Colour",
                             "Height", "Weight"]

CHARACTER_ATTRIBUTE_ENTRIES = ["Strength","Dexterity","Constitution","Intelligence","Wisdom","Charisma"]

class Character_Helper_App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.message = tk.Label(frame, text=WELCOME_MESSAGE).grid(column=1, row=0)
        self.new_chara_button = tk.Button(frame, text="New Character", command=self.make_new_character).grid(column=1, row=3)
        self.character_editor_button = tk.Button(frame, text="Character Editor", command=self.open_character_editor).grid(column=1, row=4)
        self.quit_button = tk.Button(frame, text="Quit", command=root.destroy).grid(column=1, row=6)

    def print_contents(self, event):
        print("Hi. The current entry content is:",
              self.contents.get())

    def make_new_character(self):
        self.roll_up_a_new_character()

    def accept_character_attributes(self):
        self.roll_attribute_window.destroy()

    def do_roll_attributes(self):
        dice_results = []
        for entry in CHARACTER_ATTRIBUTE_ENTRIES:
            for dice in range(4):
                result = random.randint(1,6)
                dice_results.append(result)
            dice_results.sort()
            dice_results.pop(0)
            total = sum(dice_results)
            self.__dict__[entry].set(total)
            dice_results = []

    def roll_up_a_new_character(self):
        self.roll_attribute_window = tk.Toplevel(self)

        new_character_message = "Hi there! Please press the button below to roll\n" \
                                "up your stats. (Roll 4d4 and drop the lowest)"

        self.info_message = tk.Label(self.roll_attribute_window, text=new_character_message)
        self.info_message.grid(column=0, row=0)

        self.attribute_labels = []
        self.attribute_entries = []

        for n, name in enumerate(CHARACTER_ATTRIBUTE_ENTRIES):
            self.__dict__[name] = tk.StringVar()
            new_label = tk.Label(self.roll_attribute_window, text=name)
            new_label.grid(column=0, row=n+1)
            new_entry = tk.Entry(self.roll_attribute_window, textvariable=self.__dict__[name])
            new_entry.grid(column=1, row=n+1)
            #new_entry.config(state='readonly')
            self.attribute_labels.append(new_label)
            self.attribute_entries.append(new_entry)

        self.roll_attributes_button = tk.Button(self.roll_attribute_window,
                                                text='Re-Roll Attributes',
                                                command=self.do_roll_attributes)
        self.roll_attributes_button.grid(column=1, row=n+2)

        self.accept_attributes_button = tk.Button(self.roll_attribute_window,
                                                  text='Accept All',
                                                  command=self.accept_character_attributes)
        self.accept_attributes_button.grid(column=1, row=n+3)

        self.cancel_attributes_button = tk.Button(self.roll_attribute_window,
                                                  text='Cancel',
                                                  command=self.accept_character_attributes)
        self.cancel_attributes_button.grid(column=1, row=n+4)

    def do_personal_data_entry(self):
        self.player_info_window = tk.Toplevel(self)

        new_character_message_2 = "Please fill out the personal character identity information fields below."

        self.info_message_2 = tk.Label(self.player_info_window, text = new_character_message_2)
        self.info_message_2.grid(column=0, row = 0)

        self.profile_labels = []
        self.profile_entries = []

        for n, name in enumerate(CHARACTER_PROFILE_ENTRIES):
            new_label = tk.Label(self.player_info_window, text=name)
            new_label.grid(column=0, row=n + 1)
            new_entry = tk.Entry(self.player_info_window)
            new_entry.grid(column=1, row=n + 1)
            new_entry.config(state='readonly')
            self.profile_labels.append(new_label)
            self.profile_entries.append(new_entry)

        self.accept_player_info_button = tk.Button(self.player_info_window, text='Accept All', command=self.accept_character_info)
        self.accept_player_info_button.grid(column=1, row=n+1)

    def accept_character_info(self):
        username = self.character_name_entry.get()
        print (username)


    def open_character_editor(self, ):
        pass

myapp = Character_Helper_App(root)
myapp.mainloop()