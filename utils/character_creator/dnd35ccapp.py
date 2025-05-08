import tkinter as tk
from ui.new_character_window import NewCharacterWindow

class Dnd35CharacterCreatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("D&D 3.5 Character Creator")
        self.geometry("600x400")
        self.configure(bg="#121212")

        tk.Label(self, text="D&D 3.5e Character Creator", font=("Helvetica", 18), bg="#121212", fg="white").pack(pady=20)

        tk.Button(self, text="New Character", command=self.create_new_character, width=20, height=2).pack(pady=10)
        tk.Button(self, text="Load Character", command=self.load_character, width=20, height=2).pack(pady=10)
        tk.Button(self, text="Exit", command=self.quit, width=20, height=2).pack(pady=10)

    def create_new_character(self):
        NewCharacterWindow(self)

    def load_character(self):
        from tkinter import filedialog, messagebox
        from src.character.charactersheet import Character
        from ui.character_editor_window import CharacterEditorWindow

        file_path = filedialog.askopenfilename(
            initialdir="character_sheets",
            title="Select Character File",
            filetypes=[("JSON Files", "*.json")]
        )

        if not file_path:
            return

        try:
            character = Character.from_json(file_path)
            CharacterEditorWindow(self, character)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load character: {e}")

if __name__ == "__main__":
    app = Dnd35CharacterCreatorApp()
    app.mainloop()
