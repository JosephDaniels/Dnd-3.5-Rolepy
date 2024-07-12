from character import *
from rolepy_dice import *


class NPC(Character):
    def __init__(self, npc_name=""):
        Character.__init__(self)
        keys_to_delete = []
        ## First clear out the gufta that we don't need
        for key in __dict__.keys():
            if __dict__[key] == -1:
                ## release all the info we don't need
                ## __dict__.pop(key)
                keys_to_delete.append(key)
        for key in keys_to_delete:
            __dict__.pop(key)
        if npc_name:
            filename = "npcs/%s.txt" % (npc_name)
            load(filename)
        __dict__.pop("player_name")  ## Removes player name

    def __str__(self):
        return "I'm %s" % (name)


def test():  # tries to create a NPC
    g = NPC("goblin")
    print(g.get_character_sheet())


def test_2():  # create a group of NPCS
    result = rolld(6) + rolld(6)
    goblins = []
    for n in range(result):
        goblin_name = "goblin#" + str(n + 1)
        a_goblin = NPC("goblin")
        a_goblin.name = goblin_name
        goblins.append(a_goblin)
    for goblin in goblins:
        print(str(goblin))


if __name__ == "__main__":
    test_2()
