""" A character creator made with TKinter.

It's purpose is to make DND 3.5 Character creation easier.

Made by Jordan Vo with help from Alan Wong. Please do not redistribute."""

WELCOME_MESSAGE = " Hi there!\n" \
                  "Welcome to DM Joey's DND3.5E Character Creator.\n" \
                  "DND of course standing for Demons and Daggers.\n" \
                  "Please select an option below."

# HEY THIS IS THE OFFICIAL LIBRARY STUFF!! NO TOUCHY!!! NO TOUCHY!
import random
import os
from functools import partial
from datetime import date
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# My own libraries, go ahead and improve them!
from character import Character
from race import *

## Label followed by the internal key name
PLAYER_PROFILE_DETAILS = [("Player Name", "player_name"),
                          ("Discord Username", "discord_username")]
## Label, Internal name, type of this you want to have eg. entry or textboxes or dropdown
CHARACTER_PROFILE_ENTRIES = [("Character Full Name: ", "display_name"),
                             ("Age: ","age"),
                             ("Gender: ","gender"),
                             ("Eye Colour: ","eye_colour"),
                             ("Hair Colour: ","hair_colour"),
                             ("Skin Colour: ","skin_colour"),
                             ("Height: ","height"),
                             ("Weight: ","weight")
                             ]

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

#This is how many points you get to use with point buy. Referenced by the drop down menu
POWER_LEVEL_OPTIONS_LIST = {"Low-Power" : 15,
                            "Challenging" : 22,
                            "Adventurer" : 25,
                            "Heroic" : 32,
                            "Super-Heroic" : 50,
                            "Legendary" : 80}

player_character = None  # Initializes to a character upon operation

class Character_Creation_Window(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master  # Giving us a reference to the root window
        self.character = character  # This is passed into the current window,
        # and it modifies the character on your behalf.
        self.available_attribute_points = 0  # Affected by POWER_LEVEL_OPTIONS_LIST
        self.available_attribute_points_stringvar = tk.StringVar()
        self.attribute_data = {}  # strength = 10, dexterity = 12, intelligence = 11 etc

        # UI stuff for the attribute window
        self.attribute_labels = []
        self.attribute_entries = []
        self.attribute_buttons = []
        self.attribute_stringvars = {}
        self.modifier_data = {}
        self.modifier_stringvars = {}

        for key in CHARACTER_ATTRIBUTE_ENTRIES:
            self.attribute_stringvars[key] = tk.StringVar()

        for key in CHARACTER_ATTRIBUTE_ENTRIES:
            self.modifier_stringvars[key] = tk.StringVar()

    def _calculate_modifier(self, value):
        if value%2 == 1: ## Test if the attribute divides nicely
            value = value-1 ## If not, remove one to make it even
        modifier = int((value-10)/2) ## Attribute-1/2 is modifier formula
        return modifier

    def update_modifier_data(self):
        for entry in CHARACTER_ATTRIBUTE_ENTRIES:
            self.modifier_data[entry] = self._calculate_modifier(self.attribute_data[entry])

    def get_attribute_data_from_stringvars(self):
        """ Used when you want to update the stringvars based on new attribute data"""
        for key in self.attribute_data.keys():
            # update stringvars based on the attribute data
            self.attribute_stringvars[key].set(str(self.attribute_data[key]))

    def set_attribute_data_from_stringvars(self):
        """ Used when you want to retrieve data thats current inside an entry stringvar"""
        for entry in CHARACTER_ATTRIBUTE_ENTRIES:
            self.attribute_data[entry] = int(self.attribute_stringvars[entry].get())

    def _convert_attributes_for_display(self):
        """iterates through all the actual values,
         and sticks them into the stringvars for display."""

        ## HANDLE ATTRIBUTES
        self.get_attribute_data_from_stringvars()

        for key in self.attribute_data.keys():
            # update stringvars based on the attribute data
            self.attribute_stringvars[key].set(str(self.attribute_data[key]))

        ## HANDLE AVAILABLE POINTS COUNTER
        self.available_attribute_points_stringvar.set(str(self.available_attribute_points))

        ## HANDLE MODIFIERS
        self._convert_modifiers_for_display()

    def _convert_modifiers_for_display(self):
        ## HANDLE THE MODIFIERS
        for key in self.modifier_data.keys():
            _modifier = self.modifier_data[key]
            if _modifier>=0:
                _modifier = "+"+str(_modifier)
            else:
                _modifier = self.modifier_data[key]
            self.modifier_stringvars[key].set(_modifier)

    def open_profile_window(self):
        self.profile_window = Profile_Creation_Window(self.master) ## passes root as master

    def do_accept_attributes(self):
        print ("Please override me! (Accept attributes)")
        pass

    def do_cancel_attributes(self):
        print ("Please Override me! (Cancel attributes)")
        pass

class Point_Buy_Window(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def reset_attributes_and_modifiers(self):
        for name in CHARACTER_ATTRIBUTE_ENTRIES:
            self.attribute_data[name] = 8
        self.update_modifier_data()

    def up_attribute_point(self, name):
        print ("Hit up attribute point")
        current_val = self.attribute_data[name]
        if current_val<18:
            point_cost = POINT_BUY_COST[current_val + 1]
            if point_cost <= self.available_attribute_points:
                self.attribute_data[name]+=1
                self.available_attribute_points-=point_cost
                self.update_modifier_data()
                self._convert_attributes_for_display()
            else:
                print ("wasn't able to add another point to %s. (costs %i points.)" % (name, point_cost))

    def down_attribute_point(self, name):
        print("Hit down attribute point")
        current_val = self.attribute_data[name]
        if current_val > 1:  # there's a point to remove
            point_cost = POINT_BUY_COST[current_val] # how much to refund
            self.attribute_data[name]-=1
            self.available_attribute_points+=point_cost
        else:
            print ("wasn't able to remove a point from %s" % (name))
        self.update_modifier_data()
        self._convert_attributes_for_display()

    def do_power_level_option(self, option):
        for name in CHARACTER_ATTRIBUTE_ENTRIES:
            self.attribute_data[name] = 8
        power_level_name = option
        power_level_points = POWER_LEVEL_OPTIONS_LIST[power_level_name]
        self.available_attribute_points = power_level_points
        self._convert_attributes_for_display()

    def create_widgets(self):
        row = 0

        self.reset_attributes_and_modifiers()
        self._convert_attributes_for_display()

        ## GUI SETUP

        point_buy_message = "Hi there!\n" \
                            "Plus and minus buttons add or remove points.\n" \
                            "Pay attention to the available points left.\n" \
                            "Higher Attributes will cost more to improve."

        point_buy_info_message = tk.Label(self, text=point_buy_message)
        point_buy_info_message.grid(column=0, row=row)
        row = row+1

        #attribute_column_label = tk.Label(self, text="Attributes")
        #point_buy_info_message.grid(column=1, row=row)

        #attribute_column_label = tk.Label(self, text="Modifiers")
        #point_buy_info_message.grid(column=2, row=row)

        power_level_stringvar = tk.StringVar(self)
        power_level_stringvar.set("Power Level Options")
        self.power_level_menu = tk.OptionMenu(self,
                                      power_level_stringvar,
                                      command = self.do_power_level_option,
                                      *POWER_LEVEL_OPTIONS_LIST.keys())
        self.power_level_menu.grid(column=0,row=row)

        row = row + 1

        self.attribute_labels = []
        self.attribute_entries = []
        self.attribute_buttons = []

        for name in CHARACTER_ATTRIBUTE_ENTRIES:
            new_label = tk.Label(self, text=name.capitalize())
            new_label.grid(column=0, row=row)

            new_entry = tk.Entry(self,
                                 textvariable=self.attribute_stringvars[name])
            new_entry.grid(column=1, row=row)

            self.attribute_labels.append(new_label)
            self.attribute_entries.append(new_entry)

            #  Modifier
            if self.attribute_data == {}: ## Nothing has been rolled yet
                _modifier = 0
            modifier_entry = tk.Entry(self,
                                      textvariable=self.modifier_stringvars[name])
            modifier_entry.grid(column=2, row=row)
            #row = row + 1

            positive_button = tk.Button(self,
                                        text="+",
                                        command = partial(self.up_attribute_point, name))
            positive_button.grid(column=3, row=row)

            negative_button = tk.Button(self,
                                        text="-",
                                        command = partial(self.down_attribute_point, name))
            negative_button.grid(column=4, row=row)

            self.attribute_buttons.append(positive_button)
            self.attribute_buttons.append(negative_button)
            row = row + 1

        available_point_label = tk.Label(self,
                                              text='Available Points:')
        available_point_label.grid(column=0, row=row)

        available_points_entry = tk.Entry(self,
                                               textvariable=self.available_attribute_points_stringvar)
        available_points_entry.grid(column=1, row=row)
        row = row + 1


        accept_attributes_button = tk.Button(self,
                                                  text='Accept All',
                                                  command=self.do_accept_attributes)
        accept_attributes_button.grid(column=1, row=row)
        row = row + 1

        cancel_attributes_button = tk.Button(self,
                                                  text='Cancel',
                                                  command=self.do_cancel_attributes)
        cancel_attributes_button.grid(column=1, row=row)
        row = row + 1

    def do_accept_attributes(self):
        answer = messagebox.askyesno("Do you accept?", "Do you accept these stats?")
        if answer:
            # gives master a easy reference to this object
            self.master.attribute_window = self
            # gets all the attribute data from the current window
            self.master._set_attribute_data_from_window()
            self.destroy()
        elif answer == False:
            print("Ooh should've saved those stats, they were good!")
        else:  # cancel
            print("You cancelled me!! oppressor!!")

    def do_cancel_attributes(self):
        print ("Attribute window cancelled.")
        self.destroy()

class Roll_Attributes_Window(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

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
            self.modifier_data[entry] = self._calculate_modifier(self.attribute_data[entry])
            dice_results = []
        self._convert_attributes_for_display()

    def create_widgets(self):
        new_character_message = "Hi there! Please press the button below to roll\n" \
                                "up your stats. (Roll 4d4 and drop the lowest)"

        row = 0

        info_message = tk.Label(self, text=new_character_message)
        info_message.grid(column=0, row=row)
        row = row + 1

        self.attribute_labels = []
        self.attribute_entries = []

        for name in CHARACTER_ATTRIBUTE_ENTRIES:
            self.attribute_stringvars[name] = tk.StringVar()
            # ATTRIBUTE NAME e.g. Strength
            new_label = tk.Label(self, text=name.capitalize())
            new_label.grid(column=0, row=row)
            # ATTRIBUTE VALUE e.g. 12
            new_entry = tk.Entry(self,
                                 textvariable=self.attribute_stringvars[name])
            new_entry.grid(column=1, row=row)
            #  Modifier
            if self.attribute_data == {}: ## Nothing has been rolled yet
                _modifier = 0
            modifier_entry = tk.Entry(self,
                                      textvariable=self.modifier_stringvars[name])
            modifier_entry.grid(column=2, row=row)
            row = row + 1

            self.attribute_labels.append(new_label)
            self.attribute_entries.append(new_entry)

        roll_attributes_button = tk.Button(self,
                                                text='Re-Roll Attributes',
                                                command=self.do_roll_attributes)
        roll_attributes_button.grid(column=1, row=row)
        row = row + 1

        accept_attributes_button = tk.Button(self,
                                                  text='Accept All',
                                                  # Reference parent object Character_Creation_Window command
                                                  command=self.do_accept_attributes)
        accept_attributes_button.grid(column=1, row=row)
        row = row + 1

        cancel_attributes_button = tk.Button(self,
                                                  text='Cancel',
                                                  # Reference parent object Character_Creation_Window command
                                                  command=self.do_cancel_attributes)
        cancel_attributes_button.grid(column=1, row=row)
        row = row + 1

    def do_accept_attributes(self):
        answer = messagebox.askyesno("Do you accept?", "Do you accept these stats?")
        if answer:
            # gives master a easy reference to this object
            self.master.attribute_window = self
            # gets all the attribute data from the current window
            self.master._set_attribute_data_from_window()
            self.destroy()
        elif answer == False:
            print("Ooh should've saved those stats, they were good!")
        else:  # cancel
            print("You cancelled me!! oppressor!!")

    def do_cancel_attributes(self):
        print ("Attribute window cancelled.")
        self.destroy()

class Character_Editor_Window(tk.Toplevel):
    def __init__(self, master, character,charname="",):
        # character is a Character object

        # This window will modify this object
        # with what the player enters into this
        # window once they clicks the "Save"
        # button at the end.

        super().__init__(master)
        self.master = master

        ## Profile Data
        self.player_profile_details_stringvars = {}

        self.character_profile_stringvars = {}

        for label, name in PLAYER_PROFILE_DETAILS:
            self.player_profile_details_stringvars[name] = tk.StringVar()

        for label, name in CHARACTER_PROFILE_ENTRIES: # Encompasses
            self.character_profile_stringvars[name] = tk.StringVar()

        self.create_widgets()

    def _convert_profile_for_display(self):
        for label, name in CHARACTER_PROFILE_ENTRIES:
            self.profile_data[name] = str(self.profile_entry_stringvars[name].get())

    def reset_data(self):
        self.profile_entries = []
        self.profile_stringvars = {}
        self.profile_data = {}
        for label, key in CHARACTER_PROFILE_ENTRIES:
            self.profile_stringvars[label] = tk.StringVar()

    def open_attribute_window(self):
        self.master.attribute_window = Choose_Attributes_Window(self.master)

    def do_accept_character_profile(self):
        ## NOT CORRECT
        answer = messagebox.askyesno("Do you accept?", "Do you accept these character details?")

        if answer:
            # # gives master a easy reference to this object
            # self.master.profile_window = self
            # # gets all the attribute data from the current window
            # self.master._set_profile_data_from_window()
            # self.destroy()
            # self.open_attribute_window()

            for string_var_name in self.player_profile_details_stringvars.keys():
                self.character.__dict__[string_var_name] = self.player_profile_details_stringvars[string_var_name].get()

            for string_var_name in self.character_profile_stringvars.keys():
                self.character.__dict__[string_var_name] = self.character_profile_stringvars[string_var_name].get()

            # Handle Special case of pulling Race Data from Drop down
            self.character.race = self.race_menu_stringvar.get()

            print (self.character.dump_info())

        elif answer == False:
            print ("Ooh should've saved those stats, they were good!")
        else:  #cancel
            print ("You cancelled me!! oppressor!!")

    def do_cancel_character_profile(self):
        self.destroy()

    def do_update(self):
        try:
            self.set_attribute_data_from_stringvars()
            self.update_modifier_data()
            self._convert_attributes_for_display()
        except ValueError:
            print ("Was not able to update. (invalid literal for int() with base 10: '')")

    def do_race_option(self, option):
        # self.profile_data['race'] = option
        race_benefits = RACE_BENEFITS[option]
        print (race_benefits)

    def create_widgets(self):
        row = 0

        for label, name in PLAYER_PROFILE_DETAILS:
            new_label = tk.Label(self, text=label)
            new_label.grid(column=0, row=row)

            new_entry = tk.Entry(self,
                                 textvariable=self.player_profile_details_stringvars[name])
            new_entry.grid(column=1, row=row)
            row = row + 1

        for label, name in CHARACTER_PROFILE_ENTRIES:
            new_label = tk.Label(self, text=label)
            new_label.grid(column=0, row=row)

            new_entry = tk.Entry(self,
                                 textvariable=self.character_profile_stringvars[name])
            new_entry.grid(column=1, row=row)
            row = row + 1

        # self.accept_player_info_button = tk.Button(self,
        #                                            text='Update',
        #                                            command=self.do_update)
        #
        # self.accept_player_info_button.grid(column=1, row=row)
        # row = row + 1

        new_label = tk.Label(self, text="Race:")
        new_label.grid(column=0, row=row)

        self.race_menu_stringvar = tk.StringVar(self)
        self.race_menu_stringvar.set("Please select a race")
        self.question_menu = tk.OptionMenu(self,
                                      self.race_menu_stringvar,
                                      command = self.do_race_option,
                                      *ALL_CHARACTER_RACES)
        self.question_menu.grid(column=1,row=row)
        row=row+1

        self.accept_player_info_button = tk.Button(self,
                                                   text='Accept All',
                                                   command=self.do_accept_character_profile)
        self.accept_player_info_button.grid(column=1, row=row)
        row = row + 1

        self.cancel_player_info_button = tk.Button(self,
                                                   text='Cancel',
                                                   command=self.do_cancel_character_profile)
        self.cancel_player_info_button.grid(column=1, row=row)
        row = row + 1

        row = 0

        # CREATE UNALTERED ATTRIBUTES
        # for name in CHARACTER_ATTRIBUTE_ENTRIES:
        #     new_label = tk.Label(self, text=name.capitalize())
        #     new_label.grid(column=2, row=row)
        #     # ATTRIBUTE VALUE e.g. 12
        #     new_entry = tk.Entry(self,
        #                          textvariable=self.attribute_stringvars[name])
        #     new_entry.grid(column=3, row=row)
        #     #  Modifier
        #     if self.attribute_data == {}:  ## Nothing has been rolled yet
        #         _modifier = 0
        #     modifier_entry = tk.Entry(self,
        #                               textvariable=self.modifier_stringvars[name])
        #     modifier_entry.grid(column=4, row=row)
        #     row = row + 1

        #CREATE ALTERED ATTRIBUTES
        # Shows attributes after they are altered by your race bonus
        # row = 0
        # for name in CHARACTER_ATTRIBUTE_ENTRIES:
        #     # ATTRIBUTE VALUE e.g. 12
        #     new_entry = tk.Entry(self,
        #                          textvariable=self.attribute_stringvars[name])
        #     new_entry.grid(column=6, row=row)
        #     #  Modifier
        #     if self.attribute_data == {}:  ## Nothing has been rolled yet
        #         _modifier = 0
        #     modifier_entry = tk.Entry(self,
        #                               textvariable=self.modifier_stringvars[name])
        #     modifier_entry.grid(column=7, row=row)
        #     row = row + 1

    def get_profile(self):
        _data = []
        for line in profile_data:
            _data.append(charsheet_lines)
        return _data

    def do_character_save(self):
        self._convert_profile_for_display()
        # gives master a easy reference to this object
        self.master.profile_window = self
        # gets all the attribute data from the current window
        self.master._set_profile_data_from_window()
        # actually do the saving
        self.master.do_save()

class Roll_or_Point_Buy_Prompt(tk.Toplevel):
    def __init__(self, master, character):
        super().__init__(master)
        self.character = character
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        row = 0

        roll_or_point_buy_message = "How would you like to make your character?\n" \
                                    "Classic style means you randomly make your character.\n" \
                                    "Point buy means you choose where your points go."

        roll_or_point_buy_label = tk.Label(self, text=roll_or_point_buy_message)
        roll_or_point_buy_label.grid(column=0, row=row)
        row = row+1

        point_buy_button = tk.Button(self,
                                          text='Point Buy',
                                          command=self.open_point_buy_window)
        point_buy_button.grid(column=0, row=row)
        row = row+1

        classic_button = tk.Button(self,
                                          text='Classic',
                                          command=self.open_roll_attributes_window)
        classic_button.grid(column=0, row=row)
        row = row+1

    def open_point_buy_window(self):
        self.master.point_buy_window = Point_Buy_Window(self.master, self.character)
        self.destroy()

    def open_roll_attributes_window(self):
        self.master.attribute_window = Roll_Attributes_Window(self.master)
        self.destroy()

class Character_Helper_App(tk.Frame):
    def __init__(self, master, frame):
        super().__init__(master)
        self.master = master
        self.frame = frame

        ## Holder variables
        self.roll_or_point_buy_prompt = None

        ## Important Data
        self.profile_window = None
        self.profile_data = {}  # populated by get_profile_data()

        self.attribute_window = None
        self.attribute_data = {}  # populated by get_attribute_data()

        self.create_widgets()

    def open_new_character_editor_prompt(self):
        answer = messagebox.askyesno("Make Blank Character?", "Edit blank character sheet?")
        if answer:
            c = Character()
            self.character_editor = Character_Editor_Window(self, c)
        elif answer == False:
            pass
            # self.entry_window = Entry_Window(self, message = "What is your character's name?")  # Prompt window to get their character's name

    def create_widgets(self):
        message = tk.Label(self.frame, text=WELCOME_MESSAGE).grid(column=1, row=0)
        new_chara_button = tk.Button(self.frame, text="New Character", command=self.do_new_character).grid(column=1, row=3)
        character_editor_button = tk.Button(self.frame, text="Existing Character", command=self.open_new_character_editor_prompt).grid(column=1, row=4)
        quit_button = tk.Button(self.frame, text="Quit", command=self.master.destroy).grid(column=1, row=6)

    def do_new_character(self):
        global player_character
        answer = tk.simpledialog.askstring("New Character Name", "What is your new character's name?")
        if answer:
            # Answer Input Sanitization
            answer = answer.strip()  # Remove whitespace
            answer = answer.strip("_")  # Remove leading and trailing underscores
            answer = (answer.translate({ord(i): None for i in '~.,?!@#$%^&*()-=+{}[]|'}))
            existing_files = os.listdir("characters/")
            print (existing_files)
            filename = answer
            # Filename Input Sanitization
            filename = filename.lower() # Remove the capital letter
            filename = filename.replace(" ", "_") # Change spaces to underscores
            print ("Filename:",filename)
            print("Character name:",answer)
            # INPUT VALIDATION CHECK 2 MAKE SURE IT DOESNT CLOBBER OTHER CHARACTERS
            if filename in existing_files:
                print ("Exploded1!!!!")
                tk.messagebox.showinfo("Screw you!!!", "That character name is already in use.")
            else:
                new_file = open("characters/"+filename+".txt", "w", encoding="latin-1")
                blank_file = open("characters/blank.txt")
                ## Copy the blank.txt into that new filename
                new_file.write(blank_file.read())
                blank_file.close()
                new_file.close()
                ## Finally open the new character
                player_character = Character(filename)
                roll_or_point_buy_prompt = Roll_or_Point_Buy_Prompt(self, player_character)

    def open_character_editor(self):
        print ("Opening the character editor!")
        self.character_editor = Character_Editor_Window(self)

    def _set_attribute_data_from_window(self, debug = False):
        self.attribute_data = self.attribute_window.attribute_data
        if debug == True:
            print (attribute_data)

    def _set_profile_data_from_window(self, debug = False):
        self.profile_data = self.profile_window.profile_data
        if debug == True:
            print (profile_data)

    def do_save(self):
        # Called by character or profile window instances shutting down
        #populate teh data
        data = {}
        _lines = []
        if self.attribute_window:
            self._set_attribute_data_from_window()  # populates attribute_data
        if self.profile_window:  # Not equal to None
            self._set_profile_data_from_window() # populates profile_data
            ## cuts off the first name and lowercases it
            username = self.profile_data["display_name"].split(" ")[0].lower()
            self.profile_data["username"] = username

        data = {**self.profile_data, **self.attribute_data}

        for key in data.keys():
            _lines.append('%s = %s' % (key, data[key]))
        data = "\n".join(_lines)
        filename = self.profile_data['username']+".txt"
        filename = "characters/"+filename
        f = open(filename, mode='w+')
        f.write(data)
        f.close()
        print ("Character %s was saved." % (self.profile_data["username"]))

def test_1():  # testing one component to see if it works
    root = tk.Tk()
    myapp = Point_Buy_Window(root)
    myapp.mainloop()

def test_2():  # testing the whole thing together
    root = tk.Tk()
    frame = ttk.Frame(root, padding=10)
    frame.grid()
    myapp = Character_Helper_App(root, frame)
    myapp.mainloop()

if __name__ == "__main__":
    test_2()