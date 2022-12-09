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

def main_loop():
    ## This is the part where we do stuff
    print ("Help I'm Alive")
    #client.run(TOKEN)
    bot.run(TOKEN)

if __name__ == "__main__":
    main_loop()