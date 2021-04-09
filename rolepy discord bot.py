import discord
import os
import random

from TOKEN import * ## You will need to go into the file and add your own token.

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        user = str(message.author)
        await message.channel.send('Hello, ' + user)

    if message.content.startswith('$rolld3'):
        user = str(message.author)
        d3_result = random.randint(1,3)
        await message.channel.send(user + ' rolled a ' + str(d3_result) + ' on a d3')

    if message.content.startswith('$rolld4'):
        user = str(message.author)
        d4_result = random.randint(1,4)
        await message.channel.send(user + ' rolled a ' + str(d4_result) + ' on a d4')

    if message.content.startswith('$rolld6'):
        user = str(message.author)
        d6_result = random.randint(1,6)
        await message.channel.send(user + ' rolled a ' + str(d6_result) + ' on a d6')

    if message.content.startswith('$rolld8'):
        user = str(message.author)
        d8_result = random.randint(1,8)
        await message.channel.send(user + ' rolled a ' + str(d8_result) + ' on a d8')

    if message.content.startswith('$rolld12'):
        user = str(message.author)
        d12_result = random.randint(1,12)
        await message.channel.send(user + ' rolled a ' + str(d12_result) + ' on a d12')

    if message.content.startswith('$rolld20'):
        user = str(message.author)
        d20_result = random.randint(1,20)
        await message.channel.send(user + ' rolled a ' + str(d20_result) + ' on a d20')

    if message.content.startswith('$rolld1000'):
        user = str(message.author)
        d1000_result = random.randint(1,1000)
        await message.channel.send(user + ' rolled a ' + str(d1000_result) + ' on a d1000')

    elif message.content.startswith('$rolld100'):
        user = str(message.author)
        d100_result = random.randint(1,100)
        await message.channel.send(user + ' rolled a ' + str(d100_result) + ' on a d100')

    elif message.content.startswith('$rolld10'):
        user = str(message.author)
        d10_result = random.randint(1,10)
        await message.channel.send(user + ' rolled a ' + str(d10_result) + ' on a d10')

    if message.content == '$help':
        await message.author.send("Need some help using the Roleplay Bot?\n" +
        "Here's a list of available commands. More to come.\n" +
        "$help\n" +
        "$rolld3\n"+"$rolld4\n $rolld6\n $rolld8\n $rolld10\n $rolld12\n $rolld20\n"+"$rolld100\n"+"$rolld1000\n")

client.run(TOKEN)
