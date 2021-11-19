""" A character creator made with TKinter.

It's purpose is to make DnD 3.5 Character creation easier."""

WELCOME_MESSAGE = " Hi there! Welcome to DM Joey's Dungeons and Dragon's 3.5 Edition Character Creator!\n" \
                  "Please select an option from down below."

import random

from functools import partial

import tkinter as tk

from tkinter import ttk
root = tk.Tk()
frame = ttk.Frame(root, padding=10)
frame.grid()

CHARACTER_PROFILE_ENTRIES = ["Full Name","Race","Age","Gender",
                             "Eye Colour","Hair Colour","Skin Colour",
                             "Height", "Weight"]

CHARACTER_ATTRIBUTE_ENTRIES = ["strength","dexterity","constitution","intelligence","wisdom","charisma"]

## Points by how much they cost to purchase at a given level
POINT_BUY_COST = { 1 : 1,
                   2 : 1,
                   3 : 1,
                   4 : 1,
                   5 : 1,
                   6 : 1,
                   7 : 1,
                   8 : 1,
                   9 : 1,
                   10: 1,
                   11: 1,
                   12: 1,
                   13: 1,
                   14: 1,
                   15: 2,
                   16: 2,
                   17: 3,
                   18: 3 }

POWER_LEVEL_OPTIONS_LIST = {"Low-Power" : 15,
                            "Challenging" : 22,
                            "Adventurer" : 25,
                            "Heroic" : 28,
                            "Super-Heroic" : 32,
                            "Legendary" : 40}


class Attribute_Line(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_text = ""
        self.entry_value = 0


class Character_Helper_App(tk.Frame):
    def __init__(self, master):

        # actual data for the character
        self.available_attribute_points = 0
        self.attribute_data = {}  # strength = 10, dexterity = 12, intelligence = 11 etc
        self.profile_data = {}  # display_name = "dude", hair_colour = black" etc

        # UI stuff for the attribute window
        self.attribute_labels = []
        self.attribute_entries = []
        self.attribute_buttons = []
        self.attribute_stringvars = {}
        self.available_attribute_points_stringvar = tk.StringVar()

        ## Variables
        for key in CHARACTER_ATTRIBUTE_ENTRIES:
            self.attribute_stringvars[key] = tk.StringVar()

        # UI stuff for the profile window
        self.profile_labels = []
        self.profile_entries = []
        self.profile_stringvars = {}

        super().__init__(master)
        self.message = tk.Label(frame, text=WELCOME_MESSAGE).grid(column=1, row=0)
        self.new_chara_button = tk.Button(frame, text="New Character", command=self.make_new_character).grid(column=1, row=3)
        self.character_editor_button = tk.Button(frame, text="Character Editor", command=self.open_character_editor).grid(column=1, row=4)
        self.quit_button = tk.Button(frame, text="Quit", command=root.destroy).grid(column=1, row=6)

    def _convert_attributes_for_display(self):
        ## iterates through all the actual values and stick them into the stringvars for display
        for key in self.attribute_data.keys():
            self.attribute_stringvars[key].set(str(self.attribute_data[key]))
        self.available_attribute_points_stringvar.set(str(self.available_attribute_points))

    def _convert_profile_for_display(self):
        ## iterates through all the actual values and stick them into the stringvars for display
        for key in self.profile_data.keys():
            self.profile_stringvars[key].set(str(self.profile_data[key]))

    def do_roll_attributes(self):
        dice_results = []

        for entry in CHARACTER_ATTRIBUTE_ENTRIES:
            entry = entry.lower()
            for dice in range(4):
                result = random.randint(1,6)
                dice_results.append(result)
            dice_results.sort()
            dice_results.pop(0)
            total = sum(dice_results)
            self.attribute_data[entry] = total
            dice_results = []
            self._convert_attributes_for_display()

    def do_accept_attributes(self):
        for key in self.attribute_data.keys():
            print (key, self.attribute_data[key])
        self.roll_attribute_window.destroy()

    def do_cancel_attributes(self):
        self.roll_attribute_window.destroy()

    def open_new_character_window(self):
        self.roll_or_point_buy_prompt.destroy()  # closes the previous window

        self.roll_attribute_window = tk.Toplevel(self)

        new_character_message = "Hi there! Please press the button below to roll\n" \
                                "up your stats. (Roll 4d4 and drop the lowest)"

        self.info_message = tk.Label(self.roll_attribute_window, text=new_character_message)
        self.info_message.grid(column=0, row=0)

        self.attribute_labels = []
        self.attribute_entries = []

        for n, name in enumerate(CHARACTER_ATTRIBUTE_ENTRIES):
            self.attribute_stringvars[name] = tk.StringVar()

            new_label = tk.Label(self.roll_attribute_window, text=name.capitalize())
            new_label.grid(column=0, row=n+1)

            new_entry = tk.Entry(self.roll_attribute_window,
                                 textvariable=self.attribute_stringvars[name])
            new_entry.grid(column=1, row=n+1)

            self.attribute_labels.append(new_label)
            self.attribute_entries.append(new_entry)

            #new_entry.config(state='readonly')

        self.roll_attributes_button = tk.Button(self.roll_attribute_window,
                                                text='Re-Roll Attributes',
                                                command=self.do_roll_attributes)
        self.roll_attributes_button.grid(column=1, row=n+2)

        self.accept_attributes_button = tk.Button(self.roll_attribute_window,
                                                  text='Accept All',
                                                  command=self.do_accept_attributes)
        self.accept_attributes_button.grid(column=1, row=n+3)

        self.cancel_attributes_button = tk.Button(self.roll_attribute_window,
                                                  text='Cancel',
                                                  command=self.do_cancel_attributes)
        self.cancel_attributes_button.grid(column=1, row=n+4)

    def do_personal_data_entry(self):
        self.player_info_window = tk.Toplevel(self)

        new_character_message_2 = "Please fill out the personal character identity information fields below."

        self.info_message_2 = tk.Label(self.player_info_window, text = new_character_message_2)
        self.info_message_2.grid(column=0, row = 0)

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

    def do_accept_point_buy_attributes(self):
        pass

    def do_cancel_point_buy_attributes(self):
        pass

    def up_attribute_point(self, name):
        print ("Hit up attribute point")
        current_val = self.attribute_data[name]
        if current_val<18:
            point_cost = POINT_BUY_COST[current_val + 1]
            if point_cost <= self.available_attribute_points:
                self.attribute_data[name]+=1
                self.available_attribute_points-=point_cost
            else:
                print ("wasn't able to add another point to %s. (costs %i points.)" % (name, point_cost))
            self._convert_attributes_for_display()

    def down_attribute_point(self, name):
        print("Hit down attribute point")
        current_val = self.attribute_data[name]
        if current_val > 1:  # there's a point to remove
            point_cost = POINT_BUY_COST[current_val] # how much to refund
            self.attribute_data[name]-=1
            self.available_attribute_points+=point_cost
        else:
            print ("wasn't able to remove a point from %s" % (name))
        self._convert_attributes_for_display()

    def do_power_level_option(self, option):
        power_level_name = option
        power_level_points = POWER_LEVEL_OPTIONS_LIST[power_level_name]
        self.available_attribute_points = power_level_points
        self._convert_attributes_for_display()

    def open_point_buy_window(self):

        ## SETUP

        self.roll_or_point_buy_prompt.destroy()  # closes the previous window

        self.available_attribute_points = 25

        row = 0

        for name in CHARACTER_ATTRIBUTE_ENTRIES:
            self.attribute_data[name] = 8
        self._convert_attributes_for_display()

        self.point_buy_window = tk.Toplevel(self)

        ## GUI SETUP

        point_buy_message = "Hi there! Press the plus and minus buttons to add or remove points.\n" \
                            "Please pay attention to the available points.\n" \
                            "Higher Attributes cost more to improve."

        self.point_buy_info_message = tk.Label(self.point_buy_window, text=point_buy_message)
        self.point_buy_info_message.grid(column=0, row=row)
        row = row+1

        self.power_level_stringvar = tk.StringVar(self.point_buy_window)
        self.power_level_stringvar.set("Select a power level Option")


        question_menu = tk.OptionMenu(self.point_buy_window,
                                      self.power_level_stringvar,
                                      command = self.do_power_level_option,
                                      *POWER_LEVEL_OPTIONS_LIST.keys())
        question_menu.grid(column=0,row=row)
        row = row + 1

        self.attribute_labels = []
        self.attribute_entries = []

        for n, name in enumerate(CHARACTER_ATTRIBUTE_ENTRIES):
            new_label = tk.Label(self.point_buy_window, text=name.capitalize())
            new_label.grid(column=0, row=row)

            new_entry = tk.Entry(self.point_buy_window,
                                 textvariable=self.attribute_stringvars[name])
            new_entry.grid(column=1, row=row)

            self.attribute_labels.append(new_label)
            self.attribute_entries.append(new_entry)

            positive_button = tk.Button(self.point_buy_window,
                                        text="+",
                                        command = partial(self.up_attribute_point, name))
            positive_button.grid(column=2, row=row)

            negative_button = tk.Button(self.point_buy_window,
                                        text="-",
                                        command = partial(self.down_attribute_point, name))
            negative_button.grid(column=3, row=row)

            self.attribute_buttons.append(positive_button)
            self.attribute_buttons.append(negative_button)
            row = row + 1

        self.available_point_label = tk.Label(self.point_buy_window,
                                              text='Available Points:')
        self.available_point_label.grid(column=0, row=row)
        row = row + 1

        self.available_points_entry = tk.Entry(self.point_buy_window,
                                               textvariable=self.available_attribute_points_stringvar)
        self.available_points_entry.grid(column=1, row=row)
        row = row + 1

        self.roll_attributes_button = tk.Button(self.point_buy_window,
                                                text='Re-Roll Attributes',
                                                command=self.do_roll_attributes)
        self.roll_attributes_button.grid(column=1, row=row)
        row = row + 1

        self.accept_attributes_button = tk.Button(self.point_buy_window,
                                                  text='Accept All',
                                                  command=self.do_accept_point_buy_attributes)
        self.accept_attributes_button.grid(column=1, row=row)
        row = row + 1

        self.cancel_attributes_button = tk.Button(self.point_buy_window,
                                                  text='Cancel',
                                                  command=self.do_cancel_point_buy_attributes)
        self.cancel_attributes_button.grid(column=1, row=row)
        row = row + 1


    def make_new_character(self):
        self.do_roll_or_point_buy_prompt()

    def do_roll_or_point_buy_prompt(self):
        self.roll_or_point_buy_prompt = tk.Toplevel(self)

        roll_or_point_buy_message = "How would you like to make your character?\n" \
                                    "Classic style means roll 4d4 drop the lowest."

        self.roll_or_point_buy_label = tk.Label(self.roll_or_point_buy_prompt, text=roll_or_point_buy_message)
        self.roll_or_point_buy_label.grid(column=0, row=0)

        self.point_buy_button = tk.Button(self.roll_or_point_buy_prompt,
                                          text='Point Buy',
                                          command=self.open_point_buy_window)
        self.point_buy_button.grid(column=0, row=1)

        self.classic_button = tk.Button(self.roll_or_point_buy_prompt,
                                          text='Classic',
                                          command=self.open_new_character_window)
        self.classic_button.grid(column=0, row=2)

    def open_character_editor(self, ):
        pass

myapp = Character_Helper_App(root)
myapp.mainloop()