import discord

import asyncio

from TOKEN import TOKEN

from DM_helper import * ## Module for running the game, lets us keep track of characters
from NPC import * ## non-player character information

help_login_message = """Wondering how to 'login'? Type !help followed by your characters first name.\n
If your Discord account is associated with that character,
You will be logged in and able to access your profile.
After that, you can type !me to view your logged in character,
or you can type !whois [username] to see a character's profile.
Type '!help character sheet' to learn more about it.
Please note that your username is CASE SENSITIVE!"""

help_whois_message = """Wondering how to use 'whois'?: Type !whois followed by a target character's first name.\n
This command will bring up a character profile, which is a
version of their character sheet that is intended for others
to see. This could include their picture, character description,
character history and public backstory.
Please note that the username is CASE SENSITIVE!"""

help_general_message = """Need some help using the Roleplay Bot?\n
Here's a list of available commands. More to come.\n
!greet\n !hello
!help\n !help [command]\n !login [username]\n !logout\n
!whois [username]\n !me\n !rollwod\n !rollchancedie\n
!rolld3\n !rolld4\n !rolld6\n !rolld8\n !rolld10\n !rolld12\n
!rolld16\n !rolld20\n !rolld24\n !rolld100\n !rolld1000\n !coinflip\n
!tableflip\n !fliptable\n"""

ADMINS = ['StabbyStabby#1327', 'alanwongis#3590']

dnd_players = ['StabbyStabby#1327', 'Coruba#1432', 'mystia#2889',
               'Frail Faintheart#5181', 'Magromancer#6352', 'NormL75#0235',
               'baronanansi#2600', 'alanwongis#3590']

valid_characters_for = {'StabbyStabby#1327' : ['vsevellar', 'zandrius', 'zandria', 'thaddeus', 'paige'],
                        'Coruba#1432'       : ['ulfric', 'barco', 'tebbo'],
                        'mystia#2889'       : ['chai', 'manda'],
                        'Magromancer#6352'  : ['cymancer'],
                        'NormL75#0235'      : ['kaelyn'],
                        'baronanansi#2600'  : ['barda'],
                        'alanwongis#3590'   : ['bob', 'akbar']}

client = discord.Client()

dm = DM_helper()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

def do_roll(command_line, username):
    print(command_line)
    print(username)
    if command_line.startswith('!rolld'): ## Rolls a single dice
        if "+" in command_line or "-" in command_line:
            dice_result, dice_total, dice_type, modifier = handle_dice_command(command_line) ## Pulls the 
            return "%s rolled %i total on a %s. (Natural %i%i)" % (username, dice_total, dice_type, dice_result, modifier)
        else:
            dice_result, dice_type = handle_dice_command(command_line)
            return "%s rolled a %i on a %s." % (username, dice_result, dice_type)
    else: ## Multiple dice
        if "+" in message.content or "-" in message.content:
            dice_total, num_dice, results, dice_type, modifier = handle_multiple_dice(message.content) ## Pulls the 
            return "%s rolled a %i on a %i%s. Results: %s%i" % (username, dice_total, num_dice, dice_type, results, modifier)
        else:
            dice_total, num_dice, results, dice_type = handle_multiple_dice(message.content)
            return "%s rolled a %i on %i%s. Results: %s" % (username, dice_total, num_dice, dice_type, results)

def do_login(message):
    nick = None
    member = message.author
    username = str(message.author)
    command_line = message.content
    #Error Check 1 - You're not one of my friends
    if not username in dnd_players:
        response = "You are not allowed to play DnD. Please contact DM Joey for permission."
        return response, nick
    try:
        command_line = command_line.split(" ") ## splits the argument into two pieces IE login character
        target_character = " ".join(command_line[1:]) ## target character is the second side of the argument
    except ValueError: ## means that the command failed to parse
        response = "Failed to login."
        return response, nick

    ##Error Check 2 - Don't try to steal my character!!!
    if target_character not in valid_characters_for[username]: # checks if the target character is valid for the user
            response = "You cannot login as %s, %s is not your character." % (target_character, target_character)
            return response, nick

    ##Exception, you're already logged in, I'm going to swap your character for you.
    if username in logged_in_as.keys(): ## Already logged in
        response = "%s, you are already logged in as %s." % (username, target_character)#thecharacter I'm logged in as
        return response, nick
    else: # Truly log their character in and load them in the system
        try: ## tries to rename the person, will be successful if they are a normal username
            response = "Successfully logged %s in as the character %s." % (username,target_character)
            nick = target_character # for changing their name in discord
            character_sheet = Character(target_character)
            dm.logged_in_as[username] = character_sheet
            return response, nick
        except: ## fails to rename the person, they are stronger than the bot in priviledges
            response = "Successfully logged in as %s (I wasn't able to change your username, you're probably an admin.)" % (target_character)
            character_sheet = Character(target_character)
            dm.logged_in_as[username] = character_sheet
            return response, nick
        
async def do_logout(message):
    member = message.author
    username = str(message.author)
    if username in logged_in_as.keys(): # checks if the username is in the logged_in_as dictionary keys ie Bobby#2451
        character_name = logged_in_as[username] # retrieves the name of the character they are logged in as
        logged_in_as.pop(username) # remove them from the logged in 
        return "%s, your character %s has been logged out." % (username, character_name)
    else:
        return "You're not logged in!"

def do_roll_wod(message, dice_pool, eight_again = False, nine_again = False):
    dice_pool = int(dice_pool)
    username = str(message.author)
    dice_results, successes, rerolls = roll_wod_dice(dice_pool, eight_again, nine_again)
    print (dice_results, dice_pool, successes, rerolls)
    extra_text = ""
    
    if eight_again == True:
        extra_text = " with eight-again"
    elif nine_again == True:
        extra_text = " with nine-again"
        
    if successes == 0:
        return "%s rolled %i dice and failed their roll %s. Dice Results: %s" % (username, dice_pool, extra_text, str(dice_results))
    elif successes>0:
        if rerolls>0:
            return "%s rolled %i dice and received %i successes %s. They had %i rererolled dice. Dice Results: %s" % (username, dice_pool, successes, extra_text, rerolls, str(dice_results))
        else:
            return "%s rolled %i dice and had %i successes %s. Dice Results: %s" % (username, dice_pool, successes, extra_text, str(dice_results))

@client.event
async def on_message(message):
    username = str(message.author)
    member = message.author
    
    if message.content.startswith('!login'):
        response, nick = do_login(message)
        if nick != None: # change their nickname
            await member.edit(nick=target_character)
        await message.channel.send(response)

    if message.content.startswith('!logout'):
        response = await do_logout(message)
        if response == "logout!":
            await member.edit(nick=username) # restore username
            return
        else:
            await message.channel.send(response)

    ## BATTLE COMMANDS

    if message.content.startswith('!addcombatant'):
        ## Check if they have DM power
        if not (str(message.author) in ADMINS):
            await message.author.send("Hey!! You're not allowed to add combatants to the initiative. Nice try. Chump.")

        else:
            combatant_name = message.content.split(" ")[1].strip()## grabs the second element and removes whitespace
            if combatant_name in logged_in_as.values():
                pass
                ## to do, during the login by the user, retrieve all their info
            enemy = NPC(combatant_name) ## tries to make an npc of the type specified
            dm.add_to_combat(enemy)
            
            
    ## DICE COMMANDS
            
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
        dice_result, dice_type = handle_dice_command("rolld10")
        if dice_result == 1:
            await message.channel.send(username+" rolled a chance die and suffered a dramatic failure. [Rolled 1 on a d10]")
        elif dice_result == 10:
            await message.channel.send(username+" rolled a chance die and managed to succeed. [Rolled 10 on a d10]")
        else:
            await message.channel.send(username+" rolled a chance die and failed. [Rolled "+str(dice_result)+" on a d10]")
        
    if message.content.startswith('!roll'):
        cmd = message.content
        response = do_roll(cmd, username)
        await message.channel.send(response)
        
    if message.content.startswith('!coinflip'):
        result = coinflip()
        await message.channel.send(username+" flips a coin! Result is "+result)

    ## JUST FOR FUN COMMANDS

    if message.content.startswith('!breaktable') or message.content.startswith('!tableflip'):
        result, dice_type = rolld2()
        print(result)
        if (result == 1):
            await message.channel.send(username+" dropkicks his foot straight through the table, splintering it into two seperate halves!")
        if (result == 2):
            await message.channel.send(username+" hammers their fist down upon  the innocent table in an unbridled display of nerd rage. It cracks directly in half!")
            
    if message.content.startswith('!fliptable') or message.content.startswith('!tableflip'):
        await message.channel.send(username+" grabs the table by the edges, flipping it over like an absolute savage and ruining everything! Paper, dice and doritos crash into the ground!")

    if message.content.startswith('!unfliptable'):
        await message.channel.send(username+" sheepishly returns the table to an upright position, collecting up the dice and brushing Dorito crumbs off the now orange-dusted character sheets.")

    if message.content.startswith('!kickinthedoor'):
        result, dice_type = rolld2()
        print(result)
        if (result == 1):
            await message.channel.send(username+" delivers a swift kick to the door, but the sturdy door doesn't budge. Their foot crumples as the force of the blow reverberates back through their leg. You hop up and down on one foot for 1d4 rounds in agony.")
        if (result == 2):
            await message.channel.send(username+" delivers a hearty kick to the door. The door flies off its hinges under the weight of their mighty boot.")

    if message.content.startswith('!sunglassesfingerguns'):
        await message.channel.send("%s is looking too damn cool with their sunglasses and fingerguns. Watch out, here comes %s!" % (username, username))

    ## HELP AND SUGGESTION COMMANDS
    if message.content.startswith('!hello'):
        await message.channel.send("Hello, welcome to The Joey DnD RP Server," + username)

    if message.content.startswith('!suggestion'):
        await message.author.send("Please type your message to be added to the suggestion box.")
        try:
            msg = await client.wait_for('message', timeout=12.0, check=None)
        except asyncio.TimeoutError:
            await message.author.send("Your suggestion timed out. (60 secs)")
        else:
            await message.author.send("Thanks!")

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
    
    if message.content.startswith('!help'): ## All Help Commands
        if message.content == ('!help login'):
            await message.author.send(help_login_message)
        if message.content.startswith('!help whois'):
            await message.author.send(help_whois_message)
        if message.content == ('!help'):
            await message.author.send(help_general_message)
client.run(TOKEN)
