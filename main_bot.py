import discord
from discord.ext import commands
from TOKEN import TOKEN
from DM_helper import DM_helper, Character
from user_commands import (
    do_login,
    do_logout,
    do_status,
    do_whoami,
    do_save,
    do_profile
)
from inventory_commands import (
    do_additem, do_removeitem, do_equip, do_unequip, do_inventory
)
from dice_commands import (
    do_coinflip, do_roll
)
from character_commands import CharacterCommands

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

dm = DM_helper()
dm.logged_in_as = {}

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    username = f"{message.author.name}#{message.author.discriminator}"
    if username not in dm.logged_in_as:
        try:
            default_char = Character.from_json("characters/rynn_dragonwhisper.json")
            dm.logged_in_as[username] = default_char
            dm.add_character(default_char)
            print(f"Auto-logged in {username} as Rynn")
        except Exception as e:
            print(f"Auto-login failed for {username}: {e}")

    await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

CHAT_COMMANDS = [
    ("help", None, "Show a list of available commands"),
    ("roll", do_roll, "Roll dice, e.g. !roll 2d6+1"),
    ("coinflip", do_coinflip, "Flip a coin"),
    ("login", lambda ctx: do_login(ctx, dm), "Login as a character"),
    ("logout", lambda ctx: do_logout(ctx, dm), "Logout of your character"),
    ("status", lambda ctx: do_status(ctx, dm), "View your character's status"),
    ("whoami", lambda ctx: do_whoami(ctx, dm), "Check your current character"),
    ("save", lambda ctx: do_save(ctx, dm), "Save your character"),
    ("additem", lambda ctx: do_additem(ctx, dm), "Add item to inventory"),
    ("removeitem", lambda ctx: do_removeitem(ctx, dm), "Remove item from inventory"),
    ("equip", lambda ctx: do_equip(ctx, dm), "Equip an item"),
    ("unequip", lambda ctx: do_unequip(ctx, dm), "Unequip an item"),
    ("inventory", lambda ctx: do_inventory(ctx, dm), "View inventory"),
    ("profile", lambda ctx: do_profile(ctx, dm), "View full character sheet"),
    ("npc", lambda ctx: do_npc(ctx, dm), "Generate NPC"),
    ("setscene", lambda ctx: do_setscene(ctx, dm), "Set scene description"),
    ("npc_list", lambda ctx: do_npc_list(ctx, dm), "List NPCs"),
    ("npc_detail", lambda ctx: do_npc_detail(ctx, dm), "NPC details")
]

@bot.command(name='help')
async def do_help(ctx):
    help_lines = ["**Available Commands:**"]
    for cmd, _, desc in CHAT_COMMANDS:
        help_lines.append(f"- `!{cmd}` – {desc}")
    help_text = "\n".join(help_lines)
    await ctx.author.send(help_text)

async def setup_cogs():
    await bot.add_cog(CharacterCommands(bot))

bot.loop.create_task(setup_cogs())
bot.run(TOKEN)
