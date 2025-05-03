import asyncio
import atexit

import discord

from DM_helper import *  # Module for running the game, lets us keep track of characters
from NPC import *  # non-player character information
from TOKEN import TOKEN
from help_messages import *

# from card_games import play_poker_game

ADMINS = ['StabbyStabby#1327', 'alanwongis#3590']

### START THE ENGINES ###
intents = discord.Intents.all()
discord.Intents.all()

## Used for whispering in-game information to the players so that only they see it.

# intents.members = True # what does this do bro

client = discord.Client(intents=intents)  # What

## LOAD VIRTUAL DM ASSISTANT

dm = DM_helper()  ## <--- Helps with rolls, characters, enemies and loot!

dm.load_last_session()  ## <--- Loads up all the information from last time.


## This block detects how many suggestions are already found and updates the suggestion counter
# path, dirs, files = next(os.walk("suggestionbox/"))  # walk through the directory waka waka
# file_count = len(files)  # spits out the len of the journey
# print(" suggestions found: %i" % (file_count))
# suggestions = file_count

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


async def do_coinflip(message):
    result = coinflip()
    response = "%s flips a coin! Result is %s." % (message.author, result)
    return response, message.channel


async def do_roll(message):
    username = "%s#%s" % (message.author.name, message.author.discriminator)
    command_line = message.content  # E.g. !roll3d8
    dice_total, num_dice, results, dice_type, modifier = parse_dice_command(command_line)  # Pulls the
    response = "%s rolled a %i on a %i%s. Results: %s%s" % (username,
                                                            dice_total,
                                                            num_dice,
                                                            dice_type,
                                                            results,
                                                            modifier)
    return response, message.channel


async def do_tableflip(message):
    username = ("%s#%s") % (message.author.name, message.author.discriminator)
    response = (username + " grabs the table by the edges, flipping it over like"
                           " an absolute savage and ruining everything!"
                           " Paper, dice and doritos crash into the ground!")
    return response, message.channel


async def do_unfliptable(message):
    username = ("%s#%s") % (message.author.name, message.author.discriminator)
    response = (username + " sheepishly returns the table to an upright position,"
                           " collecting up the dice and brushing Dorito crumbs off"
                           " the now orange-dusted character sheets.")
    return response, message.channel


async def do_breaktable(message):
    username = ("%s#%s") % (message.author.name, message.author.discriminator)
    result = rolld(2)
    print(result)
    if (result == 1):
        await message.channel.send(
            username + " dropkicks his foot straight through the table, splintering it into two seperate halves!")
    if (result == 2):
        await message.channel.send(
            username + " hammers their fist down upon  the innocent table in an unbridled display of nerd rage. It cracks directly in half!")


async def do_sunglassesfingerguns(message):
    username = ("%s#%s") % (message.author.name, message.author.discriminator)
    response = ("%s is looking too damn cool with their sunglasses and fingerguns."
                " Watch out, here comes %s!" % (username, username))
    return response, message.channel


async def do_kickinthedoor(message):
    username = ("%s#%s") % (message.author.name, message.author.discriminator)
    result = rolld(2)
    print(result)
    if (result == 1):
        await message.channel.send(
            username + " delivers a swift kick to the door, but the sturdy door doesn't budge. Their foot crumples as the force of the blow reverberates back through their leg. You hop up and down on one foot for 1d4 rounds in agony.")
    if (result == 2):
        await message.channel.send(
            username + " delivers a hearty kick to the door. The door flies off its hinges under the weight of their mighty boot.")
    return "", message.channel


async def do_greet(message):
    channel = message.channel
    await channel.send('Say hello!')

    def check(m):
        return m.content == 'hello' and m.channel == channel

    try:
        msg = await client.wait_for('message', timeout=30.0, check=check)
        await channel.send('Hello {.author}!'.format(msg))
    except asyncio.TimeoutError:
        await message.author.send("I waited for you to say hello... </3")
    return "", message.author


async def do_hello(message):
    msg = "Hello, welcome to The Joey DnD RP Server, %s." % (message.author)
    await message.author.send(msg, file=discord.File('images/BaldursGate2Enhanced.jpg'))
    return "", message.author


async def do_help(message):
    # if message.content == '!help login':
    #     response = (HELP_LOGIN_MESSAGE)
    # if message.content == '!help whois':
    #     response = (HELP_WHOIS_MESSAGE)
    if message.content == ('!help'):
        response = (HELP_GENERAL_MESSAGE)
    return response, message.author


async def do_suggest(message):
    username = "%s#%s" % (message.author.name, message.author.discriminator)
    global suggestions  ## This is the global text file
    await message.author.send("Please type your message to be added to the suggestion box. You have 5 minutes.")
    try:
        msg = await client.wait_for('message', timeout=300.0, check=None)
    except asyncio.TimeoutError:
        await message.author.send("Sorry but your suggestion has timed out. (5 Minutes Elapsed)")
        msg = None
    if msg != None:
        suggestions += 1
        data = msg.content
        today = date.today()
        data = data + " -- Suggestion written by %s on %s." % (username, today)
        filename = "suggestionbox/suggestion%i.txt" % (suggestions)
        f = open(filename, mode='w+')
        f.write(data)
        f.close()
        print("Suggestion#%i just got saved. Thanks %s!" % (suggestions, username))
        await message.author.send("Thanks! Received suggestion#%i: '%s'" % (suggestions, msg.content))
    return "", message.author


async def do_login(message):
    nick = None
    response = ""

    username = "%s#%s" % (message.author.name, message.author.discriminator)
    command_line = message.content  # E.g. !login Vsevellar

    try:
        command_line = command_line.split(" ")  # splits the argument into two pieces IE login character
        target_character = command_line[1]  # target character is the second side of the argument
    except ValueError:  # means that the command failed to parse
        response = "Failed to login."
        return response, message.channel

        if target_character not in VALID_CHARACTERS[username]:  # checks if the target character is valid for the user
            response = "You cannot login as %s, %s is not your character." % (target_character, target_character)

        # Exception, you're already logged in. In the future I'm going to swap your character for you.
        if username in dm.logged_in_as.keys():  # Already logged in
            response = "%s, you are already logged in as %s." % (username,
                                                                 target_character)

        else:  # Truly log their character in and load them in the system
            response = "Successfully logged %s in as the character %s." % (username, target_character)
            character = Character(target_character)  # Loads a character file based off of name
            # nick = character_sheet.username  # for changing their name in discord
            dm.logged_in_as[username] = character  # Associates a given username with a character sheet
            dm.add_character(character)
            print(character)
            print("%s has logged in as %s." % (username, target_character))

    # if nick != None:  # change their nickname
    #     if username in ADMINS:
    #         print ("tried to change your name but you are too powerful, %s" % (username))
    #     else:
    #         await message.author.edit(nick=nick)

    return response, message.channel


async def do_logout(message):
    member = message.author
    username = "%s#%s" % (member.name, member.discriminator)
    if username in dm.logged_in_as.keys():  # checks if the username is in the logged_in_as dictionary keys ie Bobby#2451
        character = dm.logged_in_as[username]  # retrieves the the character obj they are logged in as
        print(dm.logged_in_as)
        response = "%s, your character %s has been logged out." % (username, character.username)
        dm.logged_in_as.pop(username)  # remove them from the logged in
        # await message.author.edit(nick=username)  # restore username, doesn't work currently
    else:
        response = "You're not logged in!"
    return response, message.channel


async def do_whois(message):
    username = ("%s#%s") % (message.author.name, message.author.discriminator)
    char_sheet = dm.logged_in_as[username]  ## Finds your character sheet from your discord username
    profile, image_file = char_sheet.get_full_profile()  # This is their FULL profile
    await message.author.send(profile, file=discord.File(image_file))
    return "", message.channel


async def do_whoami(message):
    username = ("%s#%s") % (message.author.name, message.author.discriminator)
    char_sheet = dm.logged_in_as[username]  ## Finds your character sheet from your discord username
    response, image_file = char_sheet.get_full_profile()  # This is their FULL profile
    await message.author.send(response, file=discord.File(image_file))


async def do_character(message):
    username = ("%s#%s") % (message.author.name, message.author.discriminator)
    character = dm.logged_in_as[username]  ## Finds your character sheet from your discord username
    response = character  # This is their FULL profile
    await message.author.send(response)


async def do_gold(message):
    username = ("%s#%s") % (message.author.name, message.author.discriminator)
    # await message.author.send('Aw fooey u gots no gold =[')
    await message.author.send('Sweet! You have all the riches =]')


async def do_showlogins(message):
    user_characters = []
    for key in dm.logged_in_as.keys():  ## grabs all users who are logged in
        user_characters.append((key, dm.logged_in_as[key].display_name))  ## appends their current character to a list
    if user_characters == []:
        msg = "Noone is logged in at the moment."
    else:  # players on the list
        msg = "Characters currently logged in: "
        for username, charname in user_characters:
            msg = "%s\n%s as %s\n" % (msg, username, charname)
    return msg, message.author

    return response, message.author

async def do_additem(message):
    username = f"{message.author.name}#{message.author.discriminator}"
    if username not in dm.logged_in_as:
        return "You're not logged in!", message.channel

    try:
        _, item, qty = message.content.split(" ", 2)
        qty = int(qty)
    except ValueError:
        return "Usage: !additem <item> <quantity>", message.channel

    character = dm.logged_in_as[username]

    if not hasattr(character, "inventory"):
        character.inventory = {}

    key = item.lower()
    if key in character.inventory:
        original, count = character.inventory[key]
        character.inventory[key] = (original, count + qty)
    else:
        character.inventory[key] = (item, qty)

    return f"Added {qty}x {item} to {character.username}'s inventory.", message.channel
async def combat_commands(message):
    if message.content == ("!begincombat") or message.content == ("!startcombat"):
        ## Start Combat
        ## Switch to combat mode
        pass

    if message.content.startswith('!addcombatant'):
        ## Check if they have DM power
        if not (str(message.author) in ADMINS):
            await message.author.send("Hey!! You're not allowed to add combatants to the initiative. Nice try, chump.")

        else:
            combatant_name = message.content.split(" ")[1].strip()  ## grabs the second element and removes whitespace
            if combatant_name in dm.logged_in_as.values():
                pass
                ## to do, during the login by the user, retrieve all their info
            enemy = NPC(combatant_name)  ## tries to make an npc of the type specified
            dm.add_to_combat(enemy)

    ## GAME COMMANDS

    # if message.content == ("!play poker"):
    #     await do_poker_game(message)


async def do_status(message):
    """ Returns the status of the character you are currently playing. """
    username = "%s#%s" % (message.author.name, message.author.discriminator)
    character = dm.logged_in_as[username]
    response = character.get_status()
    channel = message.channel
    return response, channel


def save_all(dm_instance):
    # This will save all characters currently logged into the system
    filename = "data/logged_in.txt"
    _data = ""
    for key in dm_instance.logged_in_as.keys():
        _data = _data + ("%s = %s\n" % (key, dm_instance.logged_in_as[key].username))
    f = open(filename, mode='w+')
    f.write(_data)
    f.close()


# This is the MEGA lookup table of commands

CHAT_COMMANDS = [  # Execution table that based on the command input, it will throw control to the function

    ### HALP ###
    ("help", do_help),  # Handles vanilla help and help [command]

    # ROLEPLAY

    # DICE
    ("roll", do_roll),  # Handles both normal and wod rolls TODO Seperate out WoD Dice Commands + make a new bot

    # COINS
    ("coinflip", do_coinflip),  # These are all the same but people screw up and call it differently
    ("flipcoin", do_coinflip),
    ("cointoss", do_coinflip),

    # FUN COMMANDS
    ("tableflip", do_tableflip),
    ("fliptable", do_tableflip),
    ("unfliptable", do_unfliptable),
    ("breaktable", do_breaktable),
    ("sunglassesfingerguns", do_sunglassesfingerguns),
    ("kickinthedoor", do_kickinthedoor),

    # TEST COMMANDS
    ("additem", do_additem),
    ("greet", do_greet),
    ("hello", do_hello),
    ("suggest", do_suggest),  ## TODO REQUIRES FEEDBACK AND FIXING

    ## DEPRECATED
    ("login", do_login),  # formats as login [user]
    ("logout", do_logout),

    ##### GAMES #####

    # ROCK PAPER SCISSORS (Does not work lol)
    # ("rockpaperscissors", do_rock_paper_scissors),  ## NEEDS VS BOT FIX
    # ("rps", do_rock_paper_scissors),

    ## Admin Commands
    ("whoisloggedin", do_showlogins),
    ("whoisplaying", do_showlogins),

    # ROLEPLAY COMMANDS
    ("whois", do_whois),  # Shows me their profile. #
    ("whoami", do_whoami),  # Shows my profile. #
    ("me", do_whoami),  # Shorter version. #
    ("character", do_character),  # My Character Sheet #
    ("status", do_status),  # My Vitals. #
    ("gold", do_gold)  # My Precious #

    # COMBAT COMMANDS - Available during combat only
    # TODO MAKE COMBAT WORK #

]


@client.event
async def on_message(message):  # This is the main entry point for the discord bot
    member = message.author
    username = "%s#%s" % (member.name, member.discriminator)

    command_found = False

    if message.content.startswith("!"):
        for chat_command, do_func in CHAT_COMMANDS:
            if message.content.startswith("!" + chat_command):
                response, response_channel = await do_func(
                    message)  # Response channel is either pub channel or personal
                command_found = True
                break
        if not command_found:
            response = ("Sorry, that command didn't work. Command = [%s]" % (message.content))
            response_channel = message.channel
        if response != "":
            await response_channel.send(response)
    else:
        pass


@atexit.register
def goodbye():
    save_all(dm)
    print('All logged in characters have been saved.')


client.run(TOKEN)
