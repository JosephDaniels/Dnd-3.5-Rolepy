import discord
import os

from dice import *

from TOKEN import * ## You will need to go into the file and add your own token.

dnd_players = ['StabbyStabby#1327', 'Coruba#1432', 'mystia#2889',
               'Frail Faintheart#5181', 'Magromancer#6352', 'NormL75#0235']

valid_characters = {'StabbyStabby#1327' : ['Vsevellar', 'Zandrius Selwynn'],
                    'Coruba#1432'       : ['Ulfric'],
                    'mystia#2889'       : ['Chailaine'],
                    'Magromancer#6352'  : ['Cymancer'],
                    'NormL75#0235'      : ['Kaelyn']}

logged_in_as = {}

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    user = str(message.author)

    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello, ' + user)

    if message.content.startswith('!login'):
        if not user in dnd_players:
            await message.channel.send("You are not allowed to play")
            return
        try:
            command_line = message.content.split(" ")
            target_character = " ".join(command_line[1:])
        except ValueError:
            await message.channel.send("Failed to login.")
            return
        if target_character in logged_in_as.keys(): ## Already logged in
            await message.channel.send(user+", you are already logged in as " + target_character)
        else: #Not already logged in
            if target_character not in valid_characters[user]:
                await message.channel.send("You cannot login as "+target_character+", "+target_character+" is not your character.")
            else:
                logged_in_as[user] = target_character
                await message.channel.send("Successfully logged " + user + " in as the character " + target_character) 

    if message.content.startswith('!logout'):
        if user in logged_in_as.keys():
            character_name = logged_in_as[user]
            logged_in_as.pop(user)
            await message.channel.send(user + ", your character " + character_name + " has been logged out.")
        else:
            await message.channel.send ("You're not logged in!")

    if message.content.startswith('!rolld3'):
        await message.channel.send(user + ' rolled a ' + str(rolld3()) + ' on a d3')

    if message.content.startswith('!rolld4'):
        await message.channel.send(user + ' rolled a ' + str(rolld4()) + ' on a d4')

    if message.content.startswith('!rolld6'):
        await message.channel.send(user + ' rolled a ' + str(rolld6()) + ' on a d6')

    if message.content.startswith('!rolld8'):
        await message.channel.send(user + ' rolled a ' + str(rolld8()) + ' on a d8')

    if message.content.startswith('!rolld12'):
        await message.channel.send(user + ' rolled a ' + str(rolld12()) + ' on a d12')

    if message.content.startswith('!rolld16'):
        await message.channel.send(user + ' rolled a ' + str(rolld16()) + ' on a d16')

    if message.content.startswith('!rolld20'):
        await message.channel.send(user + ' rolled a ' + str(rolld20()) + ' on a d20')

    if message.content.startswith('!rolld24'):
        await message.channel.send(user + ' rolled a ' + str(rolld24()) + ' on a d24')

    if message.content.startswith('!rolld1000'):
        await message.channel.send(user + ' rolled a ' + str(rolld1000()) + ' on a d1000')

    elif message.content.startswith('!rolld100'):
        await message.channel.send(user + ' rolled a ' + str(rolld100()) + ' on a d100')

    elif message.content.startswith('!rolld10'):
        await message.channel.send(user + ' rolled a ' + str(rolld10()) + ' on a d10')

    if message.content == '!help':
        await message.author.send("Need some help using the Roleplay Bot?\n" +
        "Here's a list of available commands. More to come.\n" +
        "!help\n !login $user\n !logout\n" +
        "!rolld3\n !rolld4\n !rolld6\n !rolld8\n !rolld10\n !rolld12\n !rolld16\n !rolld20\n"+
        "!rolld24\n !rolld100\n !rolld1000\n")

client.run(TOKEN)
