import random

VALID_DICE = [2,3,4,6,8,10,12,16,20,24,30,100,1000]


"""

This script is an extension of the random module that lets you invoke
specific dice and then re-roll them.

It's basically to clean up some code in other modules, it was intended
for use with the Rolepy system, which is a DnD 3.5 system that uses
Discord for interfacing and interacting with the players.

With the new update, it now has the ability to roll d10s in the WoD system.
"""

def parse_dice_command(command_line): ## for example rolld6 or roll2d6
    '''
Rolls multiple dice, and then adds a modifier on at the end.

I plan on making another command for magic missiles that adds the modifier
on EVERY dice roll. Not sure what to call that one yet.

    '''
    command_line = command_line.strip("!roll") ## Remove leading exclamation
    num_dice, rest_of_line = command_line.split('d') ## Splits number dice and dice type
    if '+' in rest_of_line:
        modifier_type = +1
        dice_type, modifier = rest_of_line.split('+')
    elif '-' in command_line:
        modifier_type = -1
        dice_type, modifier = rest_of_line.split('-')
    else: # modifier equals zero if none specified
        modifier = 0
    #convert the parsed parts into numbers, etc.
    if num_dice == "":
        num_dice = 1
    else:
        num_dice = int(num_dice)
    dice_type, modifier = int(dice_type), int(modifier)
    ## Do the actual dice rolls
    results = [] ## Results of all dice rolled
    for dice in range(num_dice):
        results.append(rolld(dice_type))
    print (results)
    dice_total = sum(results)+modifier ## add results together
    modifier = modifier_type*modifier ## shows the correct sign and significance
    ## Formattin the modifier as feedback to the player
    if modifier_type == +1:
        modifier = "+"+str(modifier)
    elif modifier_type == -1:
        modifier = "-"+str(modifier)
    else:
        modifier = ""
    dice_type = "d"+str(dice_type) ## add the d back in
    return dice_total, num_dice, results, dice_type, modifier

def coinflip():
    result = random.randint(1,2)
    if result == 1:
        return ("Heads")
    elif result == 2:
        return ("Tails")

def rolld(n):
    if not n in VALID_DICE:
        raise Error("tried to roll a invalid dice. I'm crashing now lol")
    else:
        return random.randint(1,n)

def roll_wod_dice(dice_pool, eight_again=False, nine_again=False):
    
    success_values = [8,9,10]
    successes = 0
    rolled_dice = []
    bonus_dice = 0 # Special variable holding dice to be re-rolled
    rerolls = 0 # The resulting rerolls that occurred
    
    for dice in range(dice_pool): # for each dice in the dice pool
        dice_result = random.randint(1, 10) # roll a dice
        rolled_dice.append(dice_result) # save that dice result
        if dice_result in success_values: ## Rolled 8, 9 or 10
            successes+=1 ## Gains a success
            if dice_result == 10:
                bonus_dice+=1
            elif eight_again == True: ## any success gives a bonus dice
                bonus_dice+=1
            elif (nine_again == True) and (dice_result >= 9):
                bonus_dice+=1

    while bonus_dice > 0:
        dice_result = random.randint(1, 10)
        rolled_dice.append(dice_result)
        if dice_result in success_values: ## Rolled 8, 9 or 10
            successes+=1
            if dice_result == 10:
                bonus_dice+=1
            elif eight_again == True: ## any success gives a bonus dice
                bonus_dice+=1
            elif (nine_again == True) and (dice_result >= 9):
                bonus_dice+=1
        bonus_dice -= 1
        rerolls += 1
        
    return rolled_dice, successes, rerolls
            
if __name__ == "__main__":
    print(parse_dice_command("roll3d8+1"))
