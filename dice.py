import random


"""

This script is an extension of the random module that lets you invoke
specific dice and then re-roll them.

It's basically to clean up some code in other modules, it was intended
for use with the Rolepy system, which is a DnD 3.5 system that uses
Discord for interfacing and interacting with the players.

With the new update, it now has the ability to roll d10s in the WoD system.
"""

def handle_multiple_dice(command):
    '''
Rolls multiple dice, and then adds a modifier on at the end.

I plan on making another command for magic missiles that adds the modifier
on EVERY dice roll. Not sure what to call that one yet.

    '''
    results = []
    undigested_command = command.strip("!") ## Remove leading exclamation
    if '+' in command:
        cmd , modifier = undigested_command.split('+')
        cmd = cmd.strip("roll") ## Remove roll remporarily
        num_dice, dice_type = cmd.split('d') ## Splits number dice and dice type
        for dice in range(int(num_dice)):
            command = ("rolld"+dice_type+"()")
            result = eval(command)[0]
            result = result
            results.append(result)
        dice_total = sum(results)+int(modifier) ## add results together
        modifier = "+"+modifier ## add a plus to show integer
        dice_type = "d"+dice_type ## add the d back in
        return dice_total, num_dice, results, dice_type, modifier
    elif '-' in command:
        cmd , modifier = undigested_command.split('-')
        cmd = cmd.strip("roll") ## Remove roll remporarily
        num_dice, dice_type = cmd.split('d') ## Splits number dice and dice type
        for dice in range(int(num_dice)):
            command = ("rolld"+dice_type+"()")
            result = eval(command)[0]
            results.append(result)
        dice_total = sum(results)-int(modifier)
        modifier = "-"+modifier ## add a minus to show integer
        dice_type = "d"+dice_type ## add the d back in
        return dice_total, num_dice, results, dice_type, modifier
    else: ## Simple dice roll
        cmd = undigested_command
        cmd = cmd.strip("roll") ## Remove roll remporarily
        num_dice, dice_type = cmd.split('d') ## Splits number dice and dice type
        for dice in range(int(num_dice)):
            command = ("rolld"+dice_type+"()")
            result = eval(command)[0]
            results.append(result)
        dice_total = sum(results)
        dice_type = "d"+dice_type ## add the d back in
        return dice_total, num_dice, results, dice_type

def handle_dice_command(command):
    command = command.strip("!")
    if '+' in command:
        cmd = command.split('+')
        dice_result, dice_type = eval(cmd[0] + "()")
        modifier = cmd[1]
        dice_total = dice_result+int(modifier)
        modifier = "+"+modifier
        return dice_result, dice_total, dice_type, modifier
    elif '-' in command:
        cmd = command.split('-')
        dice_result, dice_type = eval(cmd[0] + "()")
        modifier = cmd[1]
        dice_total = dice_result-int(modifier)
        modifier = "-"+modifier
        return dice_result, dice_total, dice_type, modifier
    else: ## Simple dice roll
        dice_result, dice_type = eval(command + "()")
        return dice_result, dice_type

def coinflip():
    result = random.randint(1,2)
    if result == 1:
        return ("Heads")
    elif result == 2:
        return ("Tails")

def rolld2():
    dice_type = "d2"
    return random.randint(1,2), dice_type

def rolld3():
    dice_type = "d3"
    return random.randint(1,3), dice_type

def rolld4():
    dice_type = "d4"
    return random.randint(1,4), dice_type

def rolld6():
    dice_type = "d6"
    return random.randint(1,6), dice_type

def rolld8():
    dice_type = "d8"
    return random.randint(1,8), dice_type

def rolld10():
    dice_type = "d10"
    return random.randint(1,10), dice_type

def rolld12():
    dice_type = "d12"
    return random.randint(1,12), dice_type

def rolld16():
    dice_type = "d16"
    return random.randint(1,16), dice_type

def rolld20():
    dice_type = "d20"
    return random.randint(1,20), dice_type

def rolld24():
    dice_type = "d24"
    return random.randint(1,20), dice_type

def rolld100():
    dice_type = "d100"
    return random.randint(1,100), dice_type

def rolld1000():
    dice_type = "d1000"
    return random.randint(1,1000), dice_type

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
    print(handle_multiple_dice("roll3d8+1"))
