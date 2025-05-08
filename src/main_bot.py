import os
import json
import discord
from discord.ext import commands
from TOKEN import DISCORD_BOT_TOKEN

from src.commands import user_commands, dm_commands, character_commands
from src.dungeon_master.AIDM import AIDM
from src.world.scene import Scene

LOGIN_FILE = "../data/logged_in.json"
logins = {}
active_chars = {}

if os.path.exists(LOGIN_FILE):
    with open(LOGIN_FILE, 'r', encoding='utf-8') as f:
        logins = json.load(f)

class GameBot(commands.Bot):
    async def setup_hook(self):
        self.dm = AIDM()
        self.current_scene = Scene.load_from_file("scenes/bilgerats_cellar/bilgerats_cellar_test.json")
        await user_commands.setup(self)
        await dm_commands.setup(self)
        await character_commands.setup(self)
        print("✅ User, DM, and Character commands loaded via direct import")

bot = GameBot(command_prefix="!", intents=discord.Intents.default().all())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

@bot.command(name="move")
async def move(ctx, direction: str):
    username = f"{ctx.author.name}#{ctx.author.discriminator}"
    char = active_chars.get(username)
    if not char:
        await ctx.send("You're not logged in!")
        return

    direction_map = {
        "north": (0, -1),
        "south": (0, 1),
        "east": (1, 0),
        "west": (-1, 0)
    }

    direction = direction.lower()
    if direction not in direction_map:
        await ctx.send("Invalid direction. Use north, south, east, or west.")
        return

    dx, dy = direction_map[direction]
    if char.name not in bot.current_scene.character_positions:
        bot.current_scene.add_character(char.name, char.position["x"], char.position["y"])

    moved = bot.current_scene.move_character(char.name, dx, dy)
    if moved:
        pos = bot.current_scene.character_positions[char.name]
        char.position["x"] = pos["x"]
        char.position["y"] = pos["y"]
        await ctx.send(f"🚶 {char.name} moved {direction}. Now at ({pos['x']}, {pos['y']})")
    else:
        await ctx.send(f"❌ {char.name} cannot move {direction}. Blocked!")

bot.run(DISCORD_BOT_TOKEN)
