import os
import json
import discord
from DM_helper import Character

def dump_character(character):
    path = f"characters/{character.name.lower()}.json"
    with open(path, 'w') as f:
        json.dump(character.__dict__, f, indent=2)

async def do_login(message, dm):
    username = f"{message.author.name}#{message.author.discriminator}"
    try:
        _, target_character = message.content.split(" ", 1)
    except ValueError:
        return "Usage: !login <character_name>", message.channel

    if username in dm.logged_in_as:
        logged = dm.logged_in_as[username]
        if not hasattr(logged, "name") or not logged.name:
            del dm.logged_in_as[username]
        else:
            return f"{username}, you are already logged in as {logged.name}.", message.channel

    path = f"characters/{target_character.lower()}.json"
    if not os.path.exists(path):
        return f"Character file `{target_character.lower()}.json` not found.", message.channel

    character = Character.from_json(path)

    if not hasattr(character, "inventory"):
        character.inventory = {}
    if not hasattr(character, "equipment"):
        character.equipment = {}

    dm.logged_in_as[username] = character
    dm.add_character(character)
    return f"Successfully logged in as {target_character}.", message.channel

async def do_logout(message, dm):
    username = f"{message.author.name}#{message.author.discriminator}"
    if username in dm.logged_in_as:
        char = dm.logged_in_as.pop(username)
        return f"{username}, your character {char.name} has been logged out.", message.channel
    return "You're not logged in!", message.channel

async def do_status(message, dm):
    username = f"{message.author.name}#{message.author.discriminator}"
    character = dm.logged_in_as.get(username)
    if character:
        return character.get_status(), message.channel
    return "You're not logged in!", message.channel

async def do_whoami(message, dm):
    username = f"{message.author.name}#{message.author.discriminator}"
    if username in dm.logged_in_as:
        char = dm.logged_in_as[username]
        info = f"**You are logged in as {char.name}**\n"
        info += char.get_status()
        return info, message.channel
    return "You're not logged in.", message.channel

async def do_save(message, dm):
    username = f"{message.author.name}#{message.author.discriminator}"
    if username not in dm.logged_in_as:
        return "You're not logged in!", message.channel

    character = dm.logged_in_as[username]
    dump_character(character)
    return f"{character.name}'s data has been saved to disk.", message.channel

async def do_profile(message, dm):
    username = f"{message.author.name}#{message.author.discriminator}"
    if username not in dm.logged_in_as:
        return "You're not logged in.", message.channel

    character = dm.logged_in_as[username]
    profile_text, profile_image = character.get_full_profile()

    await message.channel.send(profile_text)
    if profile_image:
        await message.channel.send(file=discord.File(profile_image))

    return None, None
