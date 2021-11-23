import discord

import asyncio

import os
from datetime import date

from TOKEN import TOKEN
from rolepy_help import *

from DM_helper import *  # Module for running the game, lets us keep track of characters
from NPC import *  # non-player character information

ADMINS = ['StabbyStabby#1327', 'alanwongis#3590']

DND_PLAYERS = ['StabbyStabby#1327', 'Coruba#1432', 'mystia#2889',
               'Frail Faintheart#5181', 'Magromancer#6352', 'NormL75#0235',
               'baronanansi#2600', 'alanwongis#3590']

VALID_CHARACTERS_FOR = {'StabbyStabby#1327': ['vsevellar', 'zandrius', 'zandria', 'thaddeus', 'paige'],
                        'Coruba#1432': ['ulfric', 'barco', 'tebbo'],
                        'mystia#2889': ['chai', 'manda'],
                        'Magromancer#6352': ['cymancer'],
                        'NormL75#0235': ['kaelyn'],
                        'baronanansi#2600': ['barda'],
                        'alanwongis#3590': ['bob', 'akbar']}

## START THE ENGINES

client = discord.Client()

dm = DM_helper()

dm.load_last_session()

## This block detects how many suggestions are already found and updates the suggestion counter
path, dirs, files = next(os.walk("suggestionbox/"))  # walk through the directory waka waka
file_count = len(files)  # spits out the len of the journey
print(" suggestions found: %i" % (file_count))

suggestions = file_count

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

def do_roll(command_line, username):
    dice_total, num_dice, results, dice_type, modifier = parse_dice_command(command_line)  # Pulls the
    return "%s rolled a %i on a %i%s. Results: %s%s" % (username, dice_total, num_dice, dice_type, results, modifier)

def do_login(message):
    nick = None
    username = str(message.author)
    command_line = message.content
    # Error Check 1 - You're not one of my friends
    if username not in DND_PLAYERS:
        response = "You are not allowed to play DnD. Please contact DM Joey for permission."
        return response, nick
    try:
        command_line = command_line.split(" ")  # splits the argument into two pieces IE login character
        target_character = " ".join(command_line[1:])  # target character is the second side of the argument
    except ValueError:  # means that the command failed to parse
        response = "Failed to login."
        return response, nick

    # Error Check 2 - Don't try to steal my character!!!
    if target_character not in VALID_CHARACTERS_FOR[username]:  # checks if the target character is valid for the user
        response = "You cannot login as %s, %s is not your character." % (target_character, target_character)
        return response, nick

    # Exception, you're already logged in, I'm going to swap your character for you.
    if username in dm.logged_in_as.keys():  # Already logged in
        response = "%s, you are already logged in as %s." % (username,
                                                             target_character)
        return response, nick
    else:  # Truly log their character in and load them in the system
        response = "Successfully logged %s in as the character %s." % (username, target_character)
        character_sheet = Character(target_character)
        nick = character_sheet.username  # for changing their name in discord
        dm.logged_in_as[username] = character_sheet  #Associates a given username with a character sheet
        dm.add_character(character_sheet)
        print ("%s has logged in as %s." % (username, target_character))
        return response, nick

async def do_logout(message):
    member = message.author
    username = str(message.author)
    if username in dm.logged_in_as.keys():  # checks if the username is in the logged_in_as dictionary keys ie Bobby#2451
        character = dm.logged_in_as[username]  # retrieves the the character they are logged in as
        dm.logged_in_as.pop(username)  # remove them from the logged in
        return "%s, your character %s has been logged out." % (username, character.name)
    else:
        return "You're not logged in!"


def do_roll_wod(message, dice_pool, eight_again=False, nine_again=False):
    dice_pool = int(dice_pool)
    username = str(message.author)
    dice_results, successes, rerolls = roll_wod_dice(dice_pool, eight_again, nine_again)
    print(dice_results, dice_pool, successes, rerolls)
    extra_text = ""

    if eight_again == True:
        extra_text = " with eight-again"
    elif nine_again == True:
        extra_text = " with nine-again"

    if successes == 0:
        return "%s rolled %i dice and failed their roll %s. Dice Results: %s" % (
        username, dice_pool, extra_text, str(dice_results))
    elif successes > 0:
        if rerolls > 0:
            return "%s rolled %i dice and received %i successes %s. They had %i rererolled dice. Dice Results: %s" % (
            username, dice_pool, successes, extra_text, rerolls, str(dice_results))
        else:
            return "%s rolled %i dice and had %i successes %s. Dice Results: %s" % (
            username, dice_pool, successes, extra_text, str(dice_results))


def do_rock_paper_scissors(message):
    """ Gives a random result, rock, paper or scissors.
        If you give it an argument, it will try to play against you.
        If you win, lose or tie, it will tell you.
        Everything gets returned in the response variable."""
    bonus_message = ""  # victory, tie or loss message
    victory_message = " You win!!!"
    lose_message = " You lose!!!"
    if message.content == "!rockpaperscissors":  # Solo play
        bot_throw = rock_paper_scissors()  # returns a string = 'rock' 'paper' or 'scissors'
    else:  # Against the bot
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
    response = "Rock! Paper! Scissors. . .  %s!!! %s" % (bot_throw, bonus_message)
    return response


@client.event
async def on_message(message):
    member = message.author
    username = message.author

    ##USER COMMANDS

    if message.content.startswith('!login'):
        response, nick = do_login(message)
        if nick != None:  # change their nickname
            if username in ADMINS:
                print ("tried to change your name but you are too powerful, %s" % (username))
            else:
                await member.edit(nick=nick)
        await message.channel.send(response)

    if message.content.startswith('!logout'):
        response = await do_logout(message)
        if response == "logout!":
            await member.edit(nick=username)  # restore username
            return
        else:
            await message.channel.send(response)

    ## ROLEPLAY COMMANDS

    if message.content == ("!whoami") or message.content == ("!me"):
        char_sheet = dm.logged_in_as[username]  ## Finds your character sheet from your discord username
        response = "You are playing %s, AKA %s" % (char_sheet.display_name, char_sheet.name)
        await message.author.send(response)

    if message.content.startswith("!whois"):
        if message.content == "!whoisplaying" or message.content == "!whoisloggedin":
            char_name_list = []
            for key in dm.logged_in_as.keys():  ## grabs all users who are logged in
                char_name_list.append(dm.logged_in_as[key].display_name)  ## appends their current character to a list
            if char_name_list == []:
                response = "Noone is logged in at the moment."
            else: #players on the list
                response = "Characters currently logged in: "
                for char_name in char_name_list:
                    response = "%s\n%s\n" % (response,char_name)
            await message.author.send(response)
        else: # typed !whois something
            target_character = message.content.split(" ")[1].strip()  ## gets the second parameter which is the target chara
            char_sheet = None
            for key in dm.logged_in_as.keys():  # A list of usernames
                if dm.logged_in_as[key].name == target_character:  # check if a username is associated with a certain character
                    char_sheet = dm.logged_in_as[key]  ## Finds their character sheet from theirr discord username
                    response, image_file = char_sheet.get_profile()  # This is their public profile
                    await message.author.send(response, file=discord.File(image_file))

    ## BATTLE COMMANDS

    if message.content.startswith('!addcombatant'):
        ## Check if they have DM power
        if not (str(message.author) in ADMINS):
            await message.author.send("Hey!! You're not allowed to add combatants to the initiative. Nice try. Chump.")

        else:
            combatant_name = message.content.split(" ")[1].strip()  ## grabs the second element and removes whitespace
            if combatant_name in dm.logged_in_as.values():
                pass
                ## to do, during the login by the user, retrieve all their info
            enemy = NPC(combatant_name)  ## tries to make an npc of the type specified
            dm.add_to_combat(enemy)

    ## DICE COMMANDS

    if message.content.startswith('!roll'):
        cmd = message.content
        response = do_roll(cmd, username)
        await message.channel.send(response)

    if message.content.startswith('!coinflip') or message.content.startswith('!flipcoin') or message.content.startswith('!cointoss'):
        result = coinflip()
        await message.channel.send("%s flips a coin! Result is %s." % (username,result))

    if message.content.startswith('!rollwod'):
        try:
            command, dice_pool = message.content.split(" ")
        except ValueError:
            await message.channel.send("Sorry that didn't work. Try again.")
            return
        if command == ("!rollwod"):
            response = do_roll_wod(message, dice_pool)
            await message.channel.send(response)
        if command == ("!rollwod8again"):
            response = do_roll_wod(message, dice_pool, eight_again=True)
            await message.channel.send(response)
        if command == ("!rollwod9again"):
            response = do_roll_wod(message, dice_pool, nine_again=True)
            await message.channel.send(response)

    if message.content.startswith('!rollchancedie'):
        dice_result = parse_dice_command("rolld10")
        if dice_result == 1:
            await message.channel.send(
                username + " rolled a chance die and suffered a dramatic failure. [Rolled 1 on a d10]")
        elif dice_result == 10:
            await message.channel.send(username + " rolled a chance die and managed to succeed. [Rolled 10 on a d10]")
        else:
            await message.channel.send(
                username + " rolled a chance die and failed. [Rolled " + str(dice_result) + " on a d10]")

    if message.content.startswith('!rockpaperscissors'):
        response = do_rock_paper_scissors(message)
        await message.channel.send(response)


    ## JUST FOR FUN COMMANDS

    if message.content.startswith('!breaktable'):
        result = rolld(2)
        print(result)
        if (result == 1):
            await message.channel.send(
                username + " dropkicks his foot straight through the table, splintering it into two seperate halves!")
        if (result == 2):
            await message.channel.send(
                username + " hammers their fist down upon  the innocent table in an unbridled display of nerd rage. It cracks directly in half!")

    if message.content.startswith('!fliptable') or message.content.startswith('!tableflip'):
        await message.channel.send(
            username + " grabs the table by the edges, flipping it over like an absolute savage and ruining everything! Paper, dice and doritos crash into the ground!")

    if message.content.startswith('!unfliptable'):
        await message.channel.send(
            username + " sheepishly returns the table to an upright position, collecting up the dice and brushing Dorito crumbs off the now orange-dusted character sheets.")

    if message.content.startswith('!kickinthedoor'):
        result, dice_type = rolld(2)
        print(result)
        if (result == 1):
            await message.channel.send(
                username + " delivers a swift kick to the door, but the sturdy door doesn't budge. Their foot crumples as the force of the blow reverberates back through their leg. You hop up and down on one foot for 1d4 rounds in agony.")
        if (result == 2):
            await message.channel.send(
                username + " delivers a hearty kick to the door. The door flies off its hinges under the weight of their mighty boot.")

    if message.content.startswith('!sunglassesfingerguns'):
        await message.channel.send(
            "%s is looking too damn cool with their sunglasses and fingerguns. Watch out, here comes %s!" % (
            username, username))

    ## HELP AND SUGGESTION COMMANDS
    if message.content.startswith('!hello'):
        msg = "Hello, welcome to The Joey DnD RP Server, %s." % (username)
        await message.author.send(msg, file=discord.File('images/BaldursGate2Enhanced.jpg'))

    if message.content.startswith('!suggest'):
        global suggestions
        await message.author.send("Please type your message to be added to the suggestion box.")
        try:
            msg = await client.wait_for('message', timeout=180.0, check=None)
        except asyncio.TimeoutError:
            await message.author.send("Sorry, your suggestion has timed out. (180 secs or 3 minutes elapsed)")
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
            await message.author.send("Thanks! received suggestion: %s" % (msg.content))

    if message.content.startswith('!greet'):
        channel = message.channel
        await channel.send('Say hello!')

        def check(m):
            return m.content == 'hello' and m.channel == channel

        try:
            msg = await client.wait_for('message', timeout=30.0, check=check)
            await channel.send('Hello {.author}!'.format(msg))
        except asyncio.TimeoutError:
            await message.author.send("I waited for you to say hello... </3")

    if message.content.startswith('!help'):  ## All Help Commands
        if message.content == '!help login':
            await message.author.send(HELP_LOGIN_MESSAGE)
        if message.content == '!help whois':
            await message.author.send(HELP_WHOIS_MESSAGE)
        if message.content == ('!help'):
            await message.author.send(HELP_GENERAL_MESSAGE)

client.run(TOKEN)