dnd_players = ['StabbyStabby#1327', 'Coruba#1432', 'mystia#2889',
               'Frail Faintheart#5181', 'Magromancer#6352', 'NormL75#0235',
               'baronanansi#2600']

valid_characters = {'StabbyStabby#1327' : ['Vsevellar', 'Zandrius', 'Zandria'],
                    'Coruba#1432'       : ['Ulfric'],
                    'mystia#2889'       : ['Chailaine'],
                    'Magromancer#6352'  : ['Cymancer'],
                    'NormL75#0235'      : ['Kaelyn']}

logged_in_as = {}

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
