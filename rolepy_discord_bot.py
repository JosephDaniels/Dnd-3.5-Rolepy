import asyncio
import discord
import json
import os

from DM_helper import *  # Core game systems
from TOKEN import TOKEN
from help_messages import *

ADMINS = ['StabbyStabby#1327', 'alanwongis#3590']

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# Initialize virtual DM
dm = DM_helper()
dm.load_last_session()


def dump_character(character):
    path = f"characters/{character.username.lower()}.json"
    with open(path, 'w') as f:
        json.dump(character.__dict__, f, indent=2)


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


async def do_coinflip(message):
    result = coinflip()
    return f"{message.author} flips a coin! Result is {result}.", message.channel


async def do_roll(message):
    username = f"{message.author.name}#{message.author.discriminator}"
    command_line = message.content
    dice_total, num_dice, results, dice_type, modifier = parse_dice_command(command_line)
    response = f"{username} rolled a {dice_total} on a {num_dice}{dice_type}. Results: {results}{modifier}"
    return response, message.channel


async def do_help(message):
    help_lines = ["**Available Commands:**"]
    for cmd, _, desc in CHAT_COMMANDS:
        help_lines.append(f"- `!{cmd}` – {desc}")
    help_text = "\n".join(help_lines)
    return help_text, message.author


async def do_login(message):
    username = f"{message.author.name}#{message.author.discriminator}"
    try:
        _, target_character = message.content.split(" ", 1)
    except ValueError:
        return "Usage: !login <character_name>", message.channel

    if username in dm.logged_in_as:
        return f"{username}, you are already logged in as {dm.logged_in_as[username].username}.", message.channel

    character_path = f"characters/{target_character.lower()}.json"
    if not os.path.exists(character_path):
        return f"Character file {character_path} not found.", message.channel

    with open(character_path, 'r') as f:
        data = json.load(f)

    character = Character()
    character.__dict__.update(data)
    character.username = target_character

    # Ensure defaults exist
    if not hasattr(character, "inventory"):
        character.inventory = {}
    if not hasattr(character, "equipment"):
        character.equipment = {}

    dm.logged_in_as[username] = character
    dm.add_character(character)
    print(f"{username} has logged in as {target_character}.")
    return f"Successfully logged in as {target_character}.", message.channel


async def do_logout(message):
    username = f"{message.author.name}#{message.author.discriminator}"
    if username in dm.logged_in_as:
        char = dm.logged_in_as.pop(username)
        return f"{username}, your character {char.username} has been logged out.", message.channel
    return "You're not logged in!", message.channel


async def do_status(message):
    username = f"{message.author.name}#{message.author.discriminator}"
    character = dm.logged_in_as.get(username)
    if character:
        return character.get_status(), message.channel
    return "You're not logged in!", message.channel


async def do_whoami(message):
    username = f"{message.author.name}#{message.author.discriminator}"
    if username in dm.logged_in_as:
        char = dm.logged_in_as[username]
        return f"You are currently logged in as **{char.username}**.", message.channel
    return "You're not logged in.", message.channel


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
    key = item.lower()

    if not hasattr(character, "inventory"):
        character.inventory = {}

    if key in character.inventory:
        original, count = character.inventory[key]
        character.inventory[key] = (original, count + qty)
    else:
        character.inventory[key] = (item, qty)

    return f"Added {qty}x {item} to {character.username}'s inventory.", message.channel


async def do_removeitem(message):
    username = f"{message.author.name}#{message.author.discriminator}"
    if username not in dm.logged_in_as:
        return "You're not logged in!", message.channel

    try:
        _, item, qty = message.content.split(" ", 2)
        qty = int(qty)
    except ValueError:
        return "Usage: !removeitem <item> <quantity>", message.channel

    character = dm.logged_in_as[username]
    key = item.lower()

    if not hasattr(character, "inventory") or key not in character.inventory:
        return f"{character.username} doesn't have any {item}.", message.channel

    original, count = character.inventory[key]
    if qty >= count:
        del character.inventory[key]
        return f"Removed all of {original} from {character.username}'s inventory.", message.channel
    else:
        character.inventory[key] = (original, count - qty)
        return f"Removed {qty}x {original} from {character.username}'s inventory.", message.channel


async def do_equip(message):
    username = f"{message.author.name}#{message.author.discriminator}"
    if username not in dm.logged_in_as:
        return "You're not logged in!", message.channel

    try:
        _, item, slot = message.content.split(" ", 2)
    except ValueError:
        return "Usage: !equip <item> <slot>", message.channel

    character = dm.logged_in_as[username]
    key = item.lower()

    if not hasattr(character, "inventory") or key not in character.inventory:
        return f"{character.username} doesn't have a(n) {item}.", message.channel

    if not hasattr(character, "equipment"):
        character.equipment = {}

    character.equipment[slot.lower()] = item
    return f"{character.username} equips {item} in the {slot} slot.", message.channel


async def do_inventory(message):
    username = f"{message.author.name}#{message.author.discriminator}"
    if username not in dm.logged_in_as:
        return "You're not logged in!", message.channel

    character = dm.logged_in_as[username]
    lines = []

    # Show equipment
    if hasattr(character, "equipment") and character.equipment:
        lines.append(f"**{character.username}'s Equipment:**")
        for slot, item in character.equipment.items():
            lines.append(f"- {slot.capitalize()}: {item}")
    else:
        lines.append(f"**{character.username} has nothing equipped.**")

    # Show inventory
    if hasattr(character, "inventory") and character.inventory:
        lines.append(f"\n**Inventory:**")
        for key, (name, qty) in character.inventory.items():
            lines.append(f"- {name}: {qty}")
    else:
        lines.append("\nInventory is empty.")

    return "\n".join(lines), message.channel


async def do_dump(message):
    username = f"{message.author.name}#{message.author.discriminator}"
    if username not in dm.logged_in_as:
        return "You're not logged in!", message.channel

    character = dm.logged_in_as[username]
    dump_character(character)
    return f"{character.username}'s data has been saved to disk.", message.channel


# Annotated command list
CHAT_COMMANDS = [
    ("help", do_help, "Show a list of available commands"),
    ("roll", do_roll, "Roll dice, e.g. !roll 2d6+1"),
    ("coinflip", do_coinflip, "Flip a coin"),
    ("flipcoin", do_coinflip, "Flip a coin (alias)"),
    ("cointoss", do_coinflip, "Flip a coin (alias)"),
    ("login", do_login, "Login as a character, e.g. !login Rynn"),
    ("logout", do_logout, "Logout of your current character"),
    ("additem", do_additem, "Add an item to your inventory, e.g. !additem sword 1"),
    ("removeitem", do_removeitem, "Remove an item from your inventory, e.g. !removeitem sword 1"),
    ("equip", do_equip, "Equip an item to a slot, e.g. !equip sword hand"),
    ("inventory", do_inventory, "View your inventory and currently equipped items"),
    ("status", do_status, "View your character's current status"),
    ("whoami", do_whoami, "Check which character you are logged in as"),
    ("dump", do_dump, "Save your character data to disk"),
]


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!"):
        for command_entry in CHAT_COMMANDS:
            cmd = command_entry[0]
            func = command_entry[1]

            if message.content.startswith("!" + cmd):
                response, target = await func(message)
                if response:
                    await target.send(response)
                return

        await message.channel.send(f"Unknown command: {message.content}")


client.run(TOKEN)
