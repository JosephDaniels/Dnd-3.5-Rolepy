import os
import json
import discord
from DM_helper import Character

HELP_LOGIN = "Usage: !login <character_name>"

def dump_character(character):
    path = f"characters/{character.name.lower()}.json"
    with open(path, 'w') as f:
        json.dump(character.__dict__, f, indent=2)

async def do_login(message, dm):
    username = f"{message.author.name}#{message.author.discriminator}"
    try:
        _, target_character = message.content.split(" ", 1)
    except ValueError:
        return HELP_LOGIN, message.channel

    if username in dm.logged_in_as:
        logged = dm.logged_in_as[username]
        if not getattr(logged, 'name', None):
            del dm.logged_in_as[username]
        else:
            return f"{username}, you are already logged in as {logged.name}.", message.channel

    path = f"characters/{target_character.lower()}.json"
    if not os.path.exists(path):
        return f"Character file `{target_character.lower()}.json` not found.", message.channel

    character = Character.from_json(path)
    character.inventory = getattr(character, 'inventory', {})
    character.equipment = getattr(character, 'equipment', {})

    dm.logged_in_as[username] = character
    dm.add_character(character)
    return f"Successfully logged in as {target_character}.", message.channel

async def do_logout(message, dm):
    username = f"{message.author.name}#{message.author.discriminator}"
    if username in dm.logged_in_as:
        character = dm.logged_in_as.pop(username)
        try:
            dump_character(character)
        except Exception:
            pass
        return f"{username}, your character {character.name} has been logged out and saved.", message.channel
    return "You're not logged in!", message.channel

async def do_status(message, dm):
    username = f"{message.author.name}#{message.author.discriminator}"
    character = dm.logged_in_as.get(username)
    if not character:
        return "You're not logged in!", message.channel
    status = character.get_status()
    inv = character.inventory
    eq = character.equipment
    inv_desc = ', '.join([f"{item} x{qty}" for item, qty in inv.items()]) or 'Empty'
    eq_desc = ', '.join(eq.keys()) or 'None'
    full = f"{status}\n**Inventory:** {inv_desc}\n**Equipment:** {eq_desc}"
    return full, message.channel

async def do_whoami(message, dm):
    username = f"{message.author.name}#{message.author.discriminator}"
    character = dm.logged_in_as.get(username)
    if not character:
        return "You're not logged in.", message.channel
    info = f"**You are logged in as {character.name}**\n"
    info += character.get_status()
    return info, message.channel

async def do_profile(message, dm):
    username = f"{message.author.name}#{message.author.discriminator}"
    character = dm.logged_in_as.get(username)
    if not character:
        return "You're not logged in.", message.channel
    if not hasattr(character, 'get_full_profile'):
        return f"No profile available for {character.name}.", message.channel
    profile_text, profile_image = character.get_full_profile()
    await message.channel.send(profile_text)
    if profile_image:
        await message.channel.send(file=discord.File(profile_image))
    return None, None
