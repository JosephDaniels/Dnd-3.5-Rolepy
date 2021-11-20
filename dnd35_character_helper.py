""" A character creator made with TKinter.

It's purpose is to make DnD 3.5 Character creation easier."""

WELCOME_MESSAGE = " Hi there! Welcome to DM Joey's Dungeons and Dragon's 3.5 Edition Character Creator!\n" \
                  "Please select an option from down below."

import random

from functools import partial

from character import Character

import tkinter as tk
from tkinter import ttk, messagebox

## Label followed by the internal key name
CHARACTER_PROFILE_ENTRIES = [("Full Name","display_name"),
                             ("Race","race"),
                             ("Age","age"),
                             ("Gender","gender"),
                             ("Eye Colour","eye_colour"),
                             ("Hair Colour","hair_colour"),
                             ("Skin Colour","skin_colour"),
                             ("Height","height"),
                             ("Weight","weight")
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

POWER_LEVEL_OPTIONS_LIST = {"Low-Power" : 15,
                            "Challenging" : 22,
                            "Adventurer" : 25,
                            "Heroic" : 28,
                            "Super-Heroic" : 32,
                            "Legendary" : 40}

class Character_Creation_Window(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        # self.pack()
        # init internal data
        self.available_attribute_points = 0
        self.attribute_data = {}  # strength = 10, dexterity = 12, intelligence = 11 etc

        # UI stuff for the attribute window
        self.attribute_labels = []
        self.attribute_entries = []
        self.attribute_buttons = []
        self.attribute_stringvars = {}
        self.available_attribute_points_stringvar = tk.StringVar()

        for key in CHARACTER_ATTRIBUTE_ENTRIES:
            self.attribute_stringvars[key] = tk.StringVar()

        self.create_widgets()  # make the UI

    def _convert_attributes_for_display(self):
        ## iterates through all the actual values and stick them into the stringvars for display
        for key in self.attribute_data.keys():
            self.attribute_stringvars[key].set(str(self.attribute_data[key]))
        self.available_attribute_points_stringvar.set(str(self.available_attribute_points))

    def open_profile_window(self):
        profile_window = Profile_Creation_Window(self.master) ## passes root as master

    def do_accept_attributes(self):
        answer = messagebox.askyesno("Do you accept?", "Do you accept these stats?")
        if answer:
            print ("You're stuck sucka")
            for key in self.attribute_data.keys():
                print (key, self.attribute_data[key])
            self.destroy()
            self.open_profile_window()
        elif answer == False:
            print ("Ooh should've saved those stats, they were good!")
        else:  #cancel
            print ("You cancelled me!! oppressor!!")

    def do_cancel_attributes(self):
        self.roll_attribute_window.destroy()

    def get_character_attributes(self):
        for attrib_tuple in self.attribute_data:
            return attrib_tuple

    def do_character_save(self):
        self.master.do_save(self)
        self.destroy()

class Profile_Creation_Window(tk.Toplevel):
    def __init__(self,master):
        super().__init__(master)
        self.master = master  # root window

        self.master.profile_window = self

        # actual data for the character
        self.profile_data = {}  # display_name = "dude", hair_colour = black" etc

        # UI stuff for the profile window
        self.profile_labels = []
        self.profile_entries = []
        self.profile_stringvars = {}

        for label, key in CHARACTER_PROFILE_ENTRIES:
            self.profile_stringvars[label] = tk.StringVar()

        self.create_widgets()

    def _convert_profile_for_display(self):
        ## iterates through all the actual values and stick them into the stringvars for display
        for key in self.profile_data.keys():
            self.profile_stringvars[key].set(str(self.profile_data[key]))

    def clear_data(self):
        self.profile_entries = []
        self.profile_stringvars = {}
        self.profile_data = {}
        for label, key in CHARACTER_PROFILE_ENTRIES:
            self.profile_stringvars[label] = tk.StringVar()

    def do_accept_character_profile(self):
        answer = messagebox.askyesno("Do you accept?", "Is everything to your satisfaction?")
        if answer:
            for label, key in CHARACTER_PROFILE_ENTRIES:
                self.profile_data[key] = self.profile_stringvars[label].get()
            ## cuts off the first name and lowercases it
            username = self.profile_data["display_name"].split(" ")[0].lower()
            self.profile_data["username"] = username

            ## Actually do some sort of saving
            self.do_character_save()
            ## For now we're going to save, in the future we continue with profile creation

        elif answer == False:
            answer = messagebox.askyesno("Save Changes?", "Would you like to save your changes so far? \n"
                                                          "You need at least a name to save.")
            if answer:
                self.do_character_save()
            elif answer == False:
                self.destroy()
                self.clear_data()

    def do_cancel_character_profile(self):
        print("Are you sure you want to quit? [insert save prompt here]")
        pass

    def create_widgets(self):
        new_character_message_2 = "Please fill out the personal character identity information fields below."

        row = 0

        self.info_message_2 = tk.Label(self,
                                       text = new_character_message_2)
        self.info_message_2.grid(column=0, row = row)
        row = row + 1

        for label, key in CHARACTER_PROFILE_ENTRIES:
            new_label = tk.Label(self, text=label)
            new_label.grid(column=0, row=row)

            new_entry = tk.Entry(self,
                                 textvariable = self.profile_stringvars[label])
            new_entry.grid(column=1, row=row)
            self.profile_labels.append(new_label)
            self.profile_entries.append(new_entry)
            row = row + 1
        self._convert_profile_for_display()

        self.accept_player_info_button = tk.Button(self,
                                                   text='Accept All',
                                                   command=self.do_accept_character_profile)
        self.accept_player_info_button.grid(column=1, row=row)
        row = row + 1

    def get_profile(self):
        charsheet_lines = []
        for dataline in self.profile_data:
            charsheet_lines.append(charsheet_lines)
        return charsheet_lines

    def do_character_save(self):
        self.master.profile_window = self
        self.master.do_save()
        self.destroy()

class Point_Buy_Window(Character_Creation_Window):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.roll_or_point_buy_prompt.destroy()  # closes the previous window

    def do_accept_point_buy_attributes(self):
        for key in self.attribute_data.keys():
            print(key, self.attribute_data[key])
        self.destroy()
        self.do_accept_attributes() ## Callback inside of the base class object

    def do_cancel_point_buy_attributes(self):
        self.destroy()

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
        for name in CHARACTER_ATTRIBUTE_ENTRIES:
            self.attribute_data[name] = 8
        power_level_name = option
        power_level_points = POWER_LEVEL_OPTIONS_LIST[power_level_name]
        self.available_attribute_points = power_level_points
        self._convert_attributes_for_display()

    def create_widgets(self):
        print("creating widgets")
        self.available_attribute_points = 0
        row = 0

        for name in CHARACTER_ATTRIBUTE_ENTRIES:
            self.attribute_data[name] = 8
        self._convert_attributes_for_display()

        ## GUI SETUP

        point_buy_message = "Hi there! Press the plus and minus buttons to add or remove points.\n" \
                            "Please pay attention to the available points.\n" \
                            "Higher Attributes cost more to improve."

        self.point_buy_info_message = tk.Label(self, text=point_buy_message)
        self.point_buy_info_message.grid(column=0, row=row)
        row = row+1

        self.power_level_stringvar = tk.StringVar(self)
        self.power_level_stringvar.set("Select a power level Option")


        question_menu = tk.OptionMenu(self,
                                      self.power_level_stringvar,
                                      command = self.do_power_level_option,
                                      *POWER_LEVEL_OPTIONS_LIST.keys())
        question_menu.grid(column=0,row=row)
        row = row + 1

        self.attribute_labels = []
        self.attribute_entries = []

        for n, name in enumerate(CHARACTER_ATTRIBUTE_ENTRIES):
            new_label = tk.Label(self, text=name.capitalize())
            new_label.grid(column=0, row=row)

            new_entry = tk.Entry(self,
                                 textvariable=self.attribute_stringvars[name])
            new_entry.grid(column=1, row=row)

            self.attribute_labels.append(new_label)
            self.attribute_entries.append(new_entry)

            positive_button = tk.Button(self,
                                        text="+",
                                        command = partial(self.up_attribute_point, name))
            positive_button.grid(column=2, row=row)

            negative_button = tk.Button(self,
                                        text="-",
                                        command = partial(self.down_attribute_point, name))
            negative_button.grid(column=3, row=row)

            self.attribute_buttons.append(positive_button)
            self.attribute_buttons.append(negative_button)
            row = row + 1

        self.available_point_label = tk.Label(self,
                                              text='Available Points:')
        self.available_point_label.grid(column=0, row=row)
        row = row + 1

        self.available_points_entry = tk.Entry(self,
                                               textvariable=self.available_attribute_points_stringvar)
        self.available_points_entry.grid(column=1, row=row)
        row = row + 1


        self.accept_attributes_button = tk.Button(self,
                                                  text='Accept All',
                                                  command=self.do_accept_point_buy_attributes)
        self.accept_attributes_button.grid(column=1, row=row)
        row = row + 1

        self.cancel_attributes_button = tk.Button(self,
                                                  text='Cancel',
                                                  command=self.do_cancel_point_buy_attributes)
        self.cancel_attributes_button.grid(column=1, row=row)
        row = row + 1

class Roll_Attributes_Window(Character_Creation_Window):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.roll_or_point_buy_prompt.destroy()  # closes the previous window

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

    def create_widgets(self):
        new_character_message = "Hi there! Please press the button below to roll\n" \
                                "up your stats. (Roll 4d4 and drop the lowest)"

        row = 0

        self.info_message = tk.Label(self, text=new_character_message)
        self.info_message.grid(column=0, row=row)
        row = row + 1

        self.attribute_labels = []
        self.attribute_entries = []

        for name in CHARACTER_ATTRIBUTE_ENTRIES:
            self.attribute_stringvars[name] = tk.StringVar()

            new_label = tk.Label(self, text=name.capitalize())
            new_label.grid(column=0, row=row)

            new_entry = tk.Entry(self,
                                 textvariable=self.attribute_stringvars[name])
            new_entry.grid(column=1, row=row)
            row = row + 1

            self.attribute_labels.append(new_label)
            self.attribute_entries.append(new_entry)

            # new_entry.config(state='readonly')

        self.roll_attributes_button = tk.Button(self,
                                                text='Re-Roll Attributes',
                                                command=self.do_roll_attributes)
        self.roll_attributes_button.grid(column=1, row=row)
        row = row + 1

        self.accept_attributes_button = tk.Button(self,
                                                  text='Accept All',
                                                  command=self.do_accept_attributes)
        self.accept_attributes_button.grid(column=1, row=row)
        row = row + 1

        self.cancel_attributes_button = tk.Button(self,
                                                  text='Cancel',
                                                  command=self.do_cancel_attributes)
        self.cancel_attributes_button.grid(column=1, row=row)
        row = row + 1

class Character_Helper_App(tk.Frame):
    def __init__(self, master, frame):
        super().__init__(master)
        self.master = master
        self.frame = frame
        self.message = tk.Label(self.frame, text=WELCOME_MESSAGE).grid(column=1, row=0)
        self.new_chara_button = tk.Button(self.frame, text="New Character", command=self.make_new_character).grid(column=1, row=3)
        self.character_editor_button = tk.Button(self.frame, text="Character Editor", command=self.open_character_editor).grid(column=1, row=4)
        self.quit_button = tk.Button(self.frame, text="Quit", command=master.destroy).grid(column=1, row=6)

        ## Holder variables
        self.profile_window = None
        self.profile_data = {}  # populated by get_profile_data()
        self.attribute_window = None
        self.attribute_data = {}  # populated by get_attribute_data()

    def make_new_character(self):
        self.do_roll_or_point_buy_prompt()

    def do_roll_or_point_buy_prompt(self):
        self.roll_or_point_buy_prompt = tk.Toplevel(self)

        row = 0

        roll_or_point_buy_message = "How would you like to make your character?\n" \
                                    "Classic style means you randomly make your character.\n" \
                                    "Point buy means you choose where your points go."

        self.roll_or_point_buy_label = tk.Label(self.roll_or_point_buy_prompt, text=roll_or_point_buy_message)
        self.roll_or_point_buy_label.grid(column=0, row=row)
        row = row+1

        self.point_buy_button = tk.Button(self.roll_or_point_buy_prompt,
                                          text='Point Buy',
                                          command=self.open_point_buy_window)
        self.point_buy_button.grid(column=0, row=row)
        row = row+1

        self.classic_button = tk.Button(self.roll_or_point_buy_prompt,
                                          text='Classic',
                                          command=self.open_roll_attributes_window)
        self.classic_button.grid(column=0, row=row)
        row = row+1

    def open_character_editor(self):
        print ("This would open the character editor but its currently broken.")
        pass

    def open_point_buy_window(self):
        point_buy_window = Point_Buy_Window(self)

    def open_roll_attributes_window(self):
        roll_attributes_window = Roll_Attributes_Window(self)
        self.attribute_window = roll_attributes_window

    def get_attribute_data(self):
        self.attribute_data =  self.attribute_window.attribute_data

    def get_profile_data(self):
        self.profile_data = self.profile_window.profile_data

    def do_save(self):
    # Called by character or profile window instances shutting down
        #populate teh data
        data = {}
        if self.attribute_window:
            self.get_attribute_data()  # populates self.attribute_data
        if self.profile_window:  # Not equal to None
            self.get_profile_data()  # populates self.profile_data

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