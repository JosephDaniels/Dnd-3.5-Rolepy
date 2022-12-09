import asyncio
import discord
from discord.ext import commands

import os, atexit
from datetime import date

import rolepy_dice

from TOKEN import TOKEN

intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def foo(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def echo(ctx, arg):
    response = arg
    await ctx.send(response)

@bot.command()
async def coinflip(ctx):
    result = rolepy_dice.coinflip()
    response = "%s flips a coin! Result is %s." % (ctx.author, result)
    await ctx.send(response)

@bot.command()
async def roll(ctx, arg):

    """
    Rolls multiple dice, and then adds a modifier on at the end.

    For example: "!roll d6" or "!roll 2d6+7"

    I plan on making another command for magic missiles that adds the modifier
    on EVERY dice roll. Not sure what to call that one yet.
    """

    num_dice, rest_of_line = arg.split('d') ## Splits number of dice from dice type
    modifier_sign = +1
    if '+' in rest_of_line:
        dice_type, modifier = rest_of_line.split('+')
    elif '-' in arg:
        modifier_sign = -1
        dice_type, modifier = rest_of_line.split('-')
    else: # modifier equals zero if none specified
        modifier = 0
        dice_type = rest_of_line

    #convert the parsed parts into numbers, etc.
    dice_total = 0
    dice_results = []

    if num_dice == "":
        num_dice = 1
    else:
        num_dice = int(num_dice)

    dice_type = int(dice_type)
    modifier_value = int(modifier*modifier_sign)

    ## Do all of the actual dice rolls
    for dice in range(num_dice):
        dice_results.append(rolepy_dice.rolld(dice_type))

    dice_total = sum(dice_results) + modifier_value  ## add results together
    if dice_total <= 0: # make sure the total never goes lower than 1
        dice_total = 1

    ## Formatting the modifier as feedback to the player
    if modifier_value == 0:
        modifier = ""
    else:
        modifier = "%+d" % modifier_value

    dice_type = "d"+str(dice_type) ## add the d back in
    results = str([d for d in dice_results])
    response = "%s rolled a %i on a %i%s. Results: %s%s" % (ctx.author,
                                                            dice_total,
                                                            num_dice,
                                                            dice_type,
                                                            results,
                                                            modifier)
    await ctx.send(response)

def main_loop():
    ## This is the part where we do stuff
    print ("Help I'm Alive")
    #client.run(TOKEN)
    bot.run(TOKEN)

if __name__ == "__main__":
    main_loop()