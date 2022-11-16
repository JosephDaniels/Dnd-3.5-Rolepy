import discord

import asyncio

import os

import atexit

from datetime import date

from TOKEN import TOKEN

print (TOKEN)

from help_messages import *
from rolepy_dice import *  # ALL DICE HELPER THINGS SUCH AS "parse_dice_command" COME FROM HERE

from DM_helper import *  # Module for running the game, lets us keep track of characters
from NPC import *  # non-player character information

# from card_games import play_poker_game

ADMINS = ['StabbyStabby#1327', 'alanwongis#3590']

DND_PLAYERS = ['StabbyStabby#1327',
               'Coruba#1432',
               'mystia#2889',
               'Frail Faintheart#5181',
               'Magromancer#6352',
               'NormL75#0235',
               'baronanansi#2600',
               'alanwongis#3590']

VALID_CHARACTERS = {'StabbyStabby#1327' : ['vsevellar', 'zandrius', 'zandria', 'thaddeus', 'paige'],
                    'Coruba#1432' : ['ulfric', 'barco', 'tebbo'],
                    'mystia#2889' : ['chai', 'manda'],
                    'Magromancer#6352' : ['cymancer'],
                    'NormL75#0235' : ['kaelyn'],
                    'baronanansi#2600' : ['barda'],
                    'alanwongis#3590' : ['bob', 'akbar']}

# START THE ENGINES

intents = discord.Intents.all()
# intents.members = True

client = discord.Client(intents=intents)

dm = DM_helper()

dm.load_last_session()

## This block detects how many suggestions are already found and updates the suggestion counter
# path, dirs, files = next(os.walk("suggestionbox/"))  # walk through the directory waka waka
# file_count = len(files)  # spits out the len of the journey
# print(" suggestions found: %i" % (file_count))
#
# suggestions = file_count

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

def handle_roll_wod(message, eight_again=False, nine_again=False):
    cmd, dice_pool = message.content.split(" ")
    dice_pool = int(dice_pool)
    username = message.author
    dice_results, successes, rerolls =  roll_wod_dice(dice_pool, eight_again, nine_again)

    extra_text = ""
    if eight_again == True:
        extra_text = " with eight-again"
    elif nine_again == True:
        extra_text = " with nine-again"

    if successes == 0:
        return "%s rolled %i dice and failed their roll%s. Dice Results: %s" % (
            username, dice_pool, extra_text, dice_results)
    elif successes > 0:
        if rerolls > 0:
            return "%s rolled %i dice and received %i successes%s. They had %i rerolled dice. Dice Results: %s" % (
            username, dice_pool, successes, extra_text, rerolls, dice_results)
        else:
            return "%s rolled %i dice and had %i successes%s. Dice Results: %s" % (
            username, dice_pool, successes, extra_text, dice_results)

async def do_coinflip(message):
    result = coinflip()
    response = "%s flips a coin! Result is %s." % (message.author, result)
    return response, message.channel

async def do_roll(message):
    username = "%s#%s" % (message.author.name, message.author.discriminator)
    command_line = message.content  # E.g. !roll3d8
    if message.content.startswith("!rollwod"):
        try:
            command, dice_pool = message.content.split(" ")
        except ValueError:
            response = "Sorry that didn't work. Try again."
            return response, message.channel
        if command == "!rollwod":
            response = handle_roll_wod(message, dice_pool)
        elif command == ("!rollwod8again"):
            response = handle_roll_wod(message, dice_pool, eight_again=True)
        elif command == ("!rollwod9again"):
            response = handle_roll_wod(message, dice_pool, nine_again=True)

    elif message.content.startswith('!rollchancedie'):
        dice_result = rolld(10)
        if dice_result == 1:
            response = "%s rolled a chance die and suffered a dramatic failure. [Rolled 1 on a d10]" % (username)
        elif dice_result == 10:
            response = "%s rolled a chance die and managed to succeed. [Rolled 10 on a d10]" % (username)
        else:
            response = "%s rolled a chance die and failed. [Rolled %s on a d10]" % (username, dice_result)

    else: # Handles both single dice and multiple dice
        cmd = message.content
        dice_total, num_dice, results, dice_type, modifier = parse_dice_command(command_line)  # Pulls the
        response = "%s rolled a %i on a %i%s. Results: %s%s" % (username,
                                                                dice_total,
                                                                num_dice,
                                                                dice_type,
                                                                results,
                                                                modifier)
    return response, message.channel

async def do_rock_paper_scissors(message):
    """ Gives a random result, rock, paper or scissors.
        If you give it an argument, it will try to play against you.
        If you win, lose or tie, it will tell you.
        Everything gets returned in the response variable."""
    bonus_message = ""  # victory, tie or loss message
    victory_message = " You win!!!"
    lose_message = " You lose!!!"
    if message == "!rockpaperscissors" or "!rps":  # Solo play
        bot_throw = rock_paper_scissors()  # returns a string = 'rock' 'paper' or 'scissors'

    ### THIS ENTIRE VS AI PART DOESN'T WORK!!!!
    else:  # Against the bot
        print ("against the bot block")
        player_throw = message.content.split(" ")[1].strip()  # should be 'rock' 'paper' or 'scissors'
        bot_throw = rock_paper_scissors()  # should be 'rock' 'paper' or 'scissors'
        if player_throw == bot_throw:  ## detects a tie
            bonus_message = " It's a tie. Thats means we both lose."
        elif player_throw == "rock" and bot_throw == "scissors":
            bonus_message = "Rock breaks scissors." + victory_message
        elif player_throw == "paper" and bot_throw == "rock":
            bonus_message = "Paper covers rock." + victory_message
        elif player_throw == "scissors" and bot_throw == "paper":
            bonus_message = "Scissors cuts paper." + victory_message
        else:
            bonus_message = lose_message
        bonus_message = " (Player threw %s. Bot threw %s.)" % (player_throw, bot_throw)+bonus_message
    response = "%s is playing Rock, Paper, Scissors! Are you ready...?" \
               " Rock! Paper! Scissors. . . %s!!! %s" % (message.author, bot_throw, bonus_message)
    return response, message.channel

async def do_murderdeathkill(message):
    response = "%s was victorious!" % (message.author)
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
    if message.content == '!help login':
        response = (HELP_LOGIN_MESSAGE)
    if message.content == '!help whois':
        response = (HELP_WHOIS_MESSAGE)
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
        suggestions+=1
        data = msg.content
        today = date.today()
        data = data+" -- Suggestion written by %s on %s." % (username, today)
        filename = "suggestionbox/suggestion%i.txt" % (suggestions)
        f = open(filename, mode='w+')
        f.write(data)
        f.close()
        print ("Suggestion#%i just got saved. Thanks %s!" % (suggestions, username))
        await message.author.send("Thanks! Received suggestion#%i: '%s'" % (suggestions, msg.content))
    return "", message.author

async def do_login(message):
    nick = None
    response = ""
    username = "%s#%s" % (message.author.name, message.author.discriminator)
    command_line = message.content  # E.g. !login chai

    try:
        command_line = command_line.split(" ")  # splits the argument into two pieces IE login character
        target_character = command_line[1]  # target character is the second side of the argument
    except ValueError:  # means that the command failed to parse
        response = "Failed to login."
        return response, message.channel

    # Error Check 1 - You're not one of my friends
    if username not in DND_PLAYERS:
        response = "You are not allowed to play DnD. Please contact DM Joey for permission."
    else:
        # Error Check 2 - Don't try to steal my character!!!
        if target_character not in VALID_CHARACTERS[username]:  # checks if the target character is valid for the user
            response = "You cannot login as %s, %s is not your character." % (target_character, target_character)

        # Exception, you're already logged in. In the future I'm going to swap your character for you.
        if username in dm.logged_in_as.keys():  # Already logged in
            response = "%s, you are already logged in as %s." % (username,
                                                                 target_character)

        else:  # Truly log their character in and load them in the system
            response = "Successfully logged %s in as the character %s." % (username, target_character)
            character = Character(target_character)  #Loads a character file based off of name
            # nick = character_sheet.username  # for changing their name in discord
            dm.logged_in_as[username] = character  #Associates a given username with a character sheet
            dm.add_character(character)
            print (character)
            print ("%s has logged in as %s." % (username, target_character))

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
        print (dm.logged_in_as)
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

# async def do_poker_game(message):
#     await play_poker_game(message)

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
    ("greet", do_greet),
    ("hello", do_hello),
    ("help", do_help),  # Handles vanilla help and help [command]
    ("suggest", do_suggest), ## REQUIRES FEEDBACK AND FIXING
    ("login", do_login),  # formats as login [user]
    ("logout", do_logout),
    ("roll", do_roll),  # Handles both normal and wod rolls
    ("coinflip", do_coinflip),  # These are all the same but people screw up and call it differently
    ("flipcoin", do_coinflip),
    ("cointoss", do_coinflip),
    ("rockpaperscissors", do_rock_paper_scissors), ## NEEDS VS BOT FIX
    ("rps", do_rock_paper_scissors),
    ("whoisloggedin", do_showlogins),
    ("whoisplaying", do_showlogins),
    ("murderdeathkill", do_murderdeathkill),
    ("tableflip", do_tableflip),
    ("fliptable", do_tableflip),
    ("unfliptable", do_unfliptable),
    ("breaktable", do_breaktable),
    ("sunglassesfingerguns", do_sunglassesfingerguns),
    ("kickinthedoor", do_kickinthedoor),
    # ROLEPLAY COMMANDS
    ("whois", do_whois),
    ("whoami", do_whoami),
    ("me", do_whoami),
    ("status", do_status)
    # COMBAT COMMANDS - Available during combat only

]

@client.event
async def on_message(message):  # This is the main entry point for the discord bot
    member = message.author
    username = "%s#%s" % (member.name, member.discriminator)

    command_found = False

    if message.content.startswith("!"):
        for chat_command, do_func in CHAT_COMMANDS:
            if message.content.startswith("!"+chat_command):
                response, response_channel = await do_func(message)  # Response channel is either pub channel or personal
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