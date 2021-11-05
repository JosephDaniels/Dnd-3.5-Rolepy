class DM_helper(object):
    def __init__(self):
        self.combat_active = False
        self.characters = [] ## a list of character objects
        self.initiatives = {} ## characters associated with their current initiatives

    def add_character(self, character):
        self.characters.append(character)

    def load_character(self, character_name):
        for character in self.characters:
            if character == character_name:
                

def test():
    g = DM_helper()

if __name__ == "__main__":
    test()
