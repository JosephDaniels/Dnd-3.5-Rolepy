from character import *
from dnd35_class import *
from dice import *

DND35PH_CLASSES = ["bard","barbarian","cleric","druid","fighter","monk","paladin","ranger","rogue","sorcerer","wizard"] ## All the base classes from the DND 3.5e Player's handbook

class DM_helper(object):
    def __init__(self, debug = True):
        debug = debug ## special variable for debugging purposes, change it to false if you don't want a lot of print statements.
        ## Anyone who's not a player character is controlled by the DM system.
        self.characters = {} ## a list of character objects indexed by names
        self.dnd_class_tables = {} ## all dnd classes indexed by their names

        self.player_characters = [] ## names of the player characters.
        
        # for combat
        self.in_combat = False # in combat state or not
        self.combatants = []   # all players and npcs in the current battle
        self.battle_order = [] ## after intiative phase, holds a sorted list of tuples of (combatant, initiative value)
        self.current_round = -1 ## The current round of combat, used for keeping of duration. defaults to -1 if no combat started.
        self.current_combatant = -1 #  used to track the current combatant

      
        self.load_dnd_classes()

    def load_dnd_classes(self):
        for classname in DND35PH_CLASSES:
            self.dnd_class_tables[classname] = Dnd_class(classname)

    def add_character(self, character):
        self.characters[character.name] = character

    def get_character(self,character_name=""):
        return self.characters[character_name]

    ##Combat interface

    def refresh_combat(self):
        # readies for a new battle by clearing the combatant and initiative lists
        self.combatants = []   # all players and npcs in the current battle
        self.battle_order = [] ## after intiative phase, holds a sorted list of tuples of (combatant, initiative value)
        self.current_round = -1 ## The current round of combat, used for keeping of duration. defaults to -1 if no combat started.
        self.current_combatant = -1 #  used to track the current combatant
    
    def add_to_combat(self, char_or_npc):
        self.combat_order.append(char_or_npc)

    def remove_from_combat(self,character_name=""):
        ## Used when someone retreats from the battle successfully and basically is a coward
        pos = 0
        while pos < len(self.battle_order):
            initiative, character = self.battle_order[pos]
            if character_name == character.name:
                self.battle_order.pop(pos)
                if self.current_combatant >= len(self.battle_order):
                    self.current_combatant = 0
    
    def dump_battle_order(self):
        ## test function
        for initiative, participant in self.battle_order:
            print(initiative, participant.name)

    def whose_turn_isit(self):
        return self.battle_order[self.current_combatant][1].name

    def ready_next_turn(self):
        # this is the phase which asks the current player their choice
        pass
    
    def do_next_turn(self):
        # this is where you as the DM confirm the turn and execute
        self.current_combatant+=1
        if self.current_combatant>=len(self.battle_order):
            self.current_combatant=0
            self.current_round+=1

    # this is a DM exclusive command to direct npcs to attack a specific player during combat
    def command_to_fight(self, npc, player):
        pass
    
    def set_distance(self, distance):
        ## sets distance between two enemies
        pass

    

    def do_attack(self, attacker, target, attack_type = "melee"): # defaults to melee attack. change to "ranged" to reference ranged attack bonus.
        dice_result, dicetype = rolld20()
        if attack_type == "melee":
            bab = attacker.get_melee_attack_bonus() ## We need to grab the class base attack bonus and add their strength modifier
        elif attack_type == "ranged":
            bab = attacker.get_ranged_attack_bonus() ## We need to grab the class base attack bonus and add their dexterity modifier
        else:
            raise Error("this should never occur. Attack type was neither melee or ranged. Are you testing magic??")
        roll_total = bab+dice_result
        if roll_total > target.armor_class:
            print ("%s hit %s with a total of %i. (AC=%i) [Natural %s+%i]" % (attacker.name,
                                                                              target.name,
                                                                              roll_total,
                                                                              target.armor_class,
                                                                              dice_result,
                                                                              bab))
            return True ## Attack successful, proceed to damage
        else:
            print("%s missed their attack on %s with a total of %i. (AC=%i) [natural %i + %i]" %
                  (attacker.name, roll_total, target.armor_class, dice_result,bab))
            return False
        
    def deal_damage(self,attacker,victim,damage):
        victim.current_health-=damage
        if victim.current_health <= 0: ## Target is dying
            victim.dying = True
            if victim.current_health <= -10:
                victim.dead = True
                victim.dying = False
        print("%s did %i damage to %s. They have %i hitpoints left." % (attacker.name,
                                                                        damage,
                                                                        victim.name,
                                                                        victim.current_health))
        if victim.dying == True:
            print("%s is now dying." % victim.name)
            
        if victim.dead == True:
            print("%s took too much damage and is now dead." % victim.name)
            

    def do_defensive_action(self, defender):
        _effective_armor_class = defender.armor_class+2
        _effective_attack_bonus = defender.total_attack_bonus-4
        return (_effective_armor_class, _effective_attack_bonus)

    def end_combat(self):
        if len(self.battle_order) > 1:
            self.combat_active = False
        self.current_combatant = -1
        self.refresh_combat()

    

    
    def _test_combat(self, combatants):
        """
The purpose of this function is to quickly add a lot of combatants to the same combat.
It will take their characters, use their initiative bonus and roll initiative for each character automatically.
"""
        self.current_combatant = 0
        self.current_round = 1
        temp_list=[]
        print ("Combat begins! Roll initiative!")
        for combatant in combatants:
            initiative_bonus = combatant.get_initiative_bonus(misc_modifier=0)
            print ("%s rolls for initiative! [+%i initiative bonus]" % (combatant.name, initiative_bonus))
            dice_result, dice_type = rolld20()
            initiative_result = dice_result+initiative_bonus
            print ("%s rolled %i. [natural %i + %i init bonus]" % (combatant.name, initiative_result,
                                                                   dice_result, initiative_bonus))
            temp_list.append((initiative_result, combatant))  ## Combatant name associated with a 
            temp_list.sort()
            temp_list.reverse()
        self.battle_order = temp_list
        self.combat_active = True

    


def test(): # combat test
    
    dm = DM_helper()
    
    paige_file = "paige.txt"
    paige = Character()
    paige.load(paige_file)
    dm.add_character(paige)
    
    bandit_file = "bandit.txt"
    bandit = Character()
    bandit.load(bandit_file)
    dm.add_character(bandit)

    bandit_2 = Character()
    bandit_2.load(bandit_file)
    bandit_2.name = "bandit_2" ## This is a hack to give unique bandits
    dm.add_character(bandit_2)

    dm.start_combat([paige,bandit,bandit_2])
    dm.dump_battle_order()

    attacker_name = dm.whose_turn_isit()

    ##if attacker_name.dying or attacker_name.dead == True:

    print("It's your turn, " +attacker_name+".")

    while dm.combat_active == True:
        attacker_name = dm.whose_turn_isit() ## returns the name of the current turn holder
        while True:
            try:
                target_name = input("Who is the target?") ## ask for the target of the attack
                ## need to convert the target name into the actual target object
                target = dm.get_character(target_name) ## converts string name to object
                break
            except:
                print("Don't know who that is!! Try again. =]")
        attacker = dm.get_character(attacker_name)
        if dm.do_attack(attacker, target):
            ## Everybody is using a short sword
            damage, dicetype = rolld6()
            damage+=attacker.calculate_modifier(attacker.strength) ## add strength mod
            dm.deal_damage(attacker,target,damage)
        else:
            pass
        print("%s's turn is over!" % attacker.name)
        dm.next_turn()
        print("It's now %s's turn!" % dm.whose_turn_isit())

def test_2(): # 
    pass

if __name__ == "__main__":
    test()
