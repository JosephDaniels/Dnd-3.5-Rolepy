import random


"""

This script is an extension of the random module that lets you invoke
specific dice and then re-roll them.

It's basically to clean up some code in other modules, it was intended
for use with the Rolepy system, which is a DnD 3.5 system that uses
Discord for interfacing and interacting with the players.
"""

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

if __name__ == "__main__":
    print(handle_dice_command("rolld20-3"))
