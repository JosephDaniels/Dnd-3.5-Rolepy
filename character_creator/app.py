import os
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import json
import re

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from character import Character
from ui.character_editor import Character_Editor_Window
from ui.roll_or_pointbuy import Roll_or_Point_Buy_Prompt

CHARACTER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "characters"))
SAFE_FILENAME_PATTERN = re.compile(r'^[\w\- ]+$')

class Character_Helper_App(tk.Frame):
    def __init__(self, master, frame):
        super().__init__(master)
        self.master = master
        self.frame = frame
        self.character_editor_window = None
        self.create_widgets()

    def create_widgets(self):
        message = tk.Label(self.frame, text="Welcome to the D&D Character Helper!")
        message.grid(column=1, row=0, pady=10)

        tk.Button(self.frame, text="New Character", command=self.do_new_character).grid(column=1, row=1)
        tk.Button(self.frame, text="Existing Character", command=self.open_character_editor_prompt).grid(column=1, row=2)
        tk.Button(self.frame, text="Quit", command=self.master.destroy).grid(column=1, row=3, pady=10)

    def do_new_character(self):
        character = Character()
        self.character_editor_window = Character_Editor_Window(self.master, character)

    def open_character_editor_prompt(self):
        picker = tk.Toplevel(self.master)
        picker.title("Select a Character")

        tk.Label(picker, text="Choose a character to edit:").pack(pady=5)

        listbox = tk.Listbox(picker, width=40)
        listbox.pack(padx=10, pady=5)

        preview_label = tk.Label(picker, text="")
        preview_label.pack(pady=5)

        buttons_frame = tk.Frame(picker)
        buttons_frame.pack(pady=5)

        try:
            self.character_files = []
            for file in os.listdir(CHARACTER_DIR):
                file_path = os.path.join(CHARACTER_DIR, file)
                if not os.path.isfile(file_path) or not file.endswith(".json"):
                    continue
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        preview = f"{data.get('name', 'Unknown')} | Age: {data.get('age', '?')} | Gender: {data.get('gender', 'Unknown')} | Race: {data.get('race', 'Unknown')} | Class: {', '.join(data.get('character_class', [])) or 'None'}"
                except Exception as e:
                    preview = f"⚠ Error loading preview: {str(e)}"
                name = os.path.splitext(file)[0]
                listbox.insert(tk.END, name)
                self.character_files.append((name, preview))
        except FileNotFoundError:
            messagebox.showerror("Missing Folder", f"The folder '{CHARACTER_DIR}' doesn't exist.")
            picker.destroy()
            return

        def on_select(event):
            selection = listbox.curselection()
            if selection:
                idx = selection[0]
                preview_label.config(text=f"Preview: {self.character_files[idx][1]}")
            else:
                preview_label.config(text="")

        def load_selected_character():
            selected = listbox.curselection()
            if not selected:
                messagebox.showwarning("No Selection", "Please select a character first.")
                return
            char_name = listbox.get(selected[0])
            if not SAFE_FILENAME_PATTERN.match(char_name):
                messagebox.showerror("Invalid Name", f"The filename '{char_name}' contains invalid characters.")
                return
            filepath = os.path.join(CHARACTER_DIR, f"{char_name}.json")
            try:
                character = Character.from_json(filepath)
                self.character_editor_window = Character_Editor_Window(self.master, character)
                picker.destroy()
            except Exception as e:
                messagebox.showerror("Load Error", f"Could not load character:\n{e}")

        def delete_selected_character():
            selected = listbox.curselection()
            if not selected:
                messagebox.showwarning("No Selection", "Please select a character to delete.")
                return
            char_name = listbox.get(selected[0])
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{char_name}'?")
            if confirm:
                filepath = os.path.join(CHARACTER_DIR, f"{char_name}.json")
                try:
                    os.remove(filepath)
                    listbox.delete(selected[0])
                    preview_label.config(text="")
                    messagebox.showinfo("Deleted", f"{char_name} has been deleted.")
                except Exception as e:
                    messagebox.showerror("Delete Error", f"Could not delete character:\n{e}")

        listbox.bind("<<ListboxSelect>>", on_select)

        tk.Button(buttons_frame, text="Load", command=load_selected_character).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Delete", command=delete_selected_character).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Cancel", command=picker.destroy).pack(side=tk.LEFT, padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    frame = ttk.Frame(root, padding=10)
    frame.grid()
    app = Character_Helper_App(root, frame)
    root.mainloop()
