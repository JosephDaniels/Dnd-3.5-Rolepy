import discord
import os

from dice import *

from TOKEN import * ## You will need to go into the file and add your own token.

characters = ["Joey"]

logged_in_userlist = {}

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        user = str(message.author)
        await message.channel.send('Hello, ' + user)

    if message.content.startswith('!login'):
        user = str(message.author)
        command, character_name = message.content.split(" ")
        if character_name in characters:
            ## NEEDS MORE AUTHENTICATION
            if character_name not in logged_in_userlist.values(): ## Not already logged in
                logged_in_userlist[user] = character_name
                print ("Successfully logged " + user + " in as the character " + character_name) 
            elif character_name in logged_in_userlist.values():
                print ("You are already logged in as " + character_name)

    if message.content.startswith('!logout'):
        user = str(message.author)
        print (logged_in_userlist.keys())
        if user in logged_in_userlist.keys():
            character_name = logged_in_userlist[user]
            logged_in_userlist.pop(user)
            print(user + ", your character " + character_name + " has been logged out.")
        elif user not in logged_in_userlist.keys():
            print (user+ ", you're not logged in!")
        else:
            print ("Something bad happened")

    if message.content.startswith('!rolld3'):
        user = str(message.author)
        await message.channel.send(user + ' rolled a ' + str(rolld3()) + ' on a d3')

    if message.content.startswith('!rolld4'):
        user = str(message.author)
        await message.channel.send(user + ' rolled a ' + str(rolld4()) + ' on a d4')

    if message.content.startswith('!rolld6'):
        user = str(message.author)
        await message.channel.send(user + ' rolled a ' + str(rolld6()) + ' on a d6')

    if message.content.startswith('!rolld8'):
        user = str(message.author)
        await message.channel.send(user + ' rolled a ' + str(rolld8()) + ' on a d8')

    if message.content.startswith('!rolld12'):
        user = str(message.author)
        await message.channel.send(user + ' rolled a ' + str(rolld12()) + ' on a d12')

    if message.content.startswith('!rolld16'):
        user = str(message.author)
        await message.channel.send(user + ' rolled a ' + str(rolld16()) + ' on a d16')

    if message.content.startswith('!rolld20'):
        user = str(message.author)
        await message.channel.send(user + ' rolled a ' + str(rolld20()) + ' on a d20')

    if message.content.startswith('!rolld24'):
        user = str(message.author)
        await message.channel.send(user + ' rolled a ' + str(rolld24()) + ' on a d24')

    if message.content.startswith('!rolld1000'):
        user = str(message.author)
        await message.channel.send(user + ' rolled a ' + str(rolld1000()) + ' on a d1000')

    elif message.content.startswith('!rolld100'):
        user = str(message.author)
        await message.channel.send(user + ' rolled a ' + str(rolld100()) + ' on a d100')

    elif message.content.startswith('!rolld10'):
        user = str(message.author)
        await message.channel.send(user + ' rolled a ' + str(rolld10()) + ' on a d10')

    if message.content == '!help':
        await message.author.send("Need some help using the Roleplay Bot?\n" +
        "Here's a list of available commands. More to come.\n" +
        "!help\n" +
        "!rolld3\n"+"!rolld4\n !rolld6\n !rolld8\n !rolld10\n !rolld12\n !rolld20\n"+"!rolld100\n"+"!rolld1000\n")

client.run(TOKEN)
