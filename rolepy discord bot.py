import discord
import os

from dice import *

import asyncio

from TOKEN import * ## You will need to go into the file and add your own token.

dnd_players = ['StabbyStabby#1327', 'Coruba#1432', 'mystia#2889',
               'Frail Faintheart#5181', 'Magromancer#6352', 'NormL75#0235',
               'baronanansi#2600']

valid_characters = {'StabbyStabby#1327' : ['Vsevellar', 'Zandrius', 'Zandria'],
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

    if message.content.startswith('!greet'):
        await message.channel.send("Hello, welcome to The Joey DnD RP Server," + user)

    if message.content.startswith('!login'):
        if not user in dnd_players:
            await message.channel.send("You are not allowed to play DnD. Please contact DM Joey for permission.")
            return
        try:
            command_line = message.content.split(" ")
            target_character = " ".join(command_line[1:])
        except ValueError:
            await message.channel.send("Failed to login.")
            return
        if target_character in logged_in_as.keys(): ## Already logged in
            await message.channel.send(user+", you are already logged in as " + target_character)
        else:
            if target_character not in valid_characters[user]:
                print (user, target_character)
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

    if message.content.startswith('!rolld'):
        if "+" in message.content or "-" in message.content:
            dice_result, dice_total, dice_type, modifier = handle_dice_command(message.content) ## Pulls the 
            await message.channel.send(user+" rolled "+str(dice_total)+" total on a "+dice_type+" (Natural "+
                                       str(dice_result)+modifier+"="+str(dice_total)+")")
        else:
            dice_result, dice_type = handle_dice_command(message.content)
            await message.channel.send(user+' rolled a '+str(dice_result)+' on a '+dice_type)

    if message.content.startswith('!coinflip'):
        result = coinflip()
        await message.channel.send(user+" flips a coin! Result is "+result)

    if message.content.startswith('!fliptable'):
        await message.channel.send(user+" grabs the table by the edges, flipping it over like an absolute savage and ruining everything! Paper, dice and doritos crash into the ground!")

    if message.content.startswith('!suggestion'):
        await message.author.send("Please type your message to be added to the suggestion box.")
        try:
            msg = await client.wait_for('message', timeout=12.0, check=None)
        except asyncio.TimeoutError:
            await message.author.send("Your suggestion timed out. (60 secs)")
        else:
            await message.author.send("Thanks!")

    if message.content.startswith('!thumb'):
        channel = message.channel
        await channel.send('Send me that 👍 reaction, mate')

        def check(reaction, user):
            return user == message.author and str(reaction.emoji) == '👍'

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await channel.send('👎')
        else:
            await channel.send('👍')
    
    if message.content.startswith('!help'): ## All Help Commands
        if message.content == ('!help login'):
            await message.author.send("Wondering how to 'login'? Type !help followed by your characters first name.\n"
                                       "If your Discord account is associated with that character,"
                                       "You will be logged in and able to access your profile."
                                       "After that, you can type !me to view your logged in character,"
                                       "or you can type !whois [user] to see a character's profile."
                                       "Type '!help character sheet' to learn more about it."
                                      "Please note that your username is CASE SENSITIVE!")
        if message.content.startswith('!help whois'):
            await message.author.send("Wondering how to use 'whois'?: Type !whois followed by a target character's first name.\n"
                                        "This command will bring up a character profile, which is a"
                                      "version of their character sheet that is intended for others"
                                      "to see. This could include their picture, character description,"
                                      "character history and public backstory."
                                      "Please note that the username is CASE SENSITIVE!")
        if message.content == ('!help'):
            await message.author.send("Need some help using the Roleplay Bot?\n" +
            "Here's a list of available commands. More to come.\n"
            "!greet\n"
            "!help\n !help [command]\n !login [user]\n !logout\n"
            "!whois [user]\n !me\n"
            "!rolld3\n !rolld4\n !rolld6\n !rolld8\n !rolld10\n !rolld12\n" 
            "!rolld16\n !rolld20\n !rolld24\n !rolld100\n !rolld1000\n !coinflip\n")

client.run(TOKEN)
