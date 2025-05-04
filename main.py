import asyncio
import discord
from TOKEN import TOKEN
from DM_helper import *
from help_messages import *

# External command modules
from character_commands import (
    do_login, do_logout, do_status, do_whoami, do_save, do_profile
)
from inventory_commands import (
    do_additem, do_removeitem, do_equip, do_unequip, do_inventory
)
from dice_commands import (
    do_coinflip, do_roll
)

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# Initialize the game engine
dm = DM_helper()
dm.logged_in_as = {}  # Wipe ghost sessions on startup
dm.load_last_session()


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


# Local help command (uses command registry)
async def do_help(message):
    help_lines = ["**Available Commands:**"]
    for cmd, _, desc in CHAT_COMMANDS:
        help_lines.append(f"- `!{cmd}` – {desc}")
    help_text = "\n".join(help_lines)
    return help_text, message.author


# Command registry: (command_name, handler_function, help_text)
CHAT_COMMANDS = [
    ("help", do_help, "Show a list of available commands"),
    ("roll", do_roll, "Roll dice, e.g. !roll 2d6+1"),
    ("coinflip", do_coinflip, "Flip a coin"),
    ("flipcoin", do_coinflip, "Flip a coin (alias)"),
    ("cointoss", do_coinflip, "Flip a coin (alias)"),
    ("login", lambda msg: do_login(msg, dm), "Login as a character, e.g. !login Rynn"),
    ("logout", lambda msg: do_logout(msg, dm), "Logout of your current character"),
    ("status", lambda msg: do_status(msg, dm), "View your character's current status"),
    ("whoami", lambda msg: do_whoami(msg, dm), "Check which character you're using"),
    ("save", lambda msg: do_save(msg, dm), "Save your character data to disk"),
    ("additem", lambda msg: do_additem(msg, dm), "Add an item to your inventory"),
    ("removeitem", lambda msg: do_removeitem(msg, dm), "Remove an item from your inventory"),
    ("equip", lambda msg: do_equip(msg, dm), "Equip an item to a slot"),
    ("unequip", lambda msg: do_unequip(msg, dm), "Unequip a gear item."),
    ("inventory", lambda msg: do_inventory(msg, dm), "View your inventory and equipment"),
    ("profile", lambda msg: do_profile(msg, dm), "View your full character sheet and portrait"),
]


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!"):
        for cmd, func, _ in CHAT_COMMANDS:
            if message.content.startswith("!" + cmd):
                result = await func(message)

                if isinstance(result, tuple):
                    content, target = result
                    if content:
                        await target.send(content)
                return

        await message.channel.send(f"Unknown command: {message.content}")


client.run(TOKEN)
