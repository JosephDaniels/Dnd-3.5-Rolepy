from character import *
from dice import *

class NPC(Character):
    def __init__(self, npc_name = ""):
        Character.__init__(self)
        keys_to_delete = []
        ## First clear out the gufta that we don't need
        for key in self.__dict__.keys():
            if self.__dict__[key] == -1:
                ## release all the info we don't need
                ## self.__dict__.pop(key)
                keys_to_delete.append(key)
        for key in keys_to_delete:
            self.__dict__.pop(key)
        if npc_name:
            filename = "npcs/%s.txt" % (npc_name)
            self.load(filename)
        self.__dict__.pop("player_name") ## Removes player name
        

def test(): # tries to create a NPC
    g = NPC("goblin")
    print(g.get_character_sheet())

def test_2(): #create a group of NPCS
    result = roll("roll2d6")
    goblins = []
    for n in range(result):
        goblin_name = "goblin#"+str(n+1)
        a_goblin = NPC("goblin")
        a_goblin.name = goblin_name
        goblins.append(a_goblin)

if __name__ == "__main__":
    test_2()

