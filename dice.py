import random


"""

This script is an extension of the random module that lets you invoke
specific dice and then re-roll them.

It's basically to clean up some code in other modules, it was intended
for use with the Rolepy system, which is a DnD 3.5 system that uses
Discord for interfacing and interacting with the players.


"""

def coin_flip():
    result = random.randint(1,2)
    if result == 1:
        print ("Heads")
    elif result == 2:
        print ("Tails")

def rolld3():
    return random.randint(1,3)

def rolld4():
    return random.randint(1,4)

def rolld6():
    return random.randint(1,6)

def rolld8():
    return random.randint(1,8)

def rolld10():
    return random.randint(1,10)

def rolld12():
    return random.randint(1,12)

def rolld16():
    return random.randint(1,16)

def rolld20():
    return random.randint(1,20)

def rolld24():
    return random.randint(1,20)

def rolld100():
    return random.randint(1,100)

def rolld1000():
    return random.randint(1,1000)
    
