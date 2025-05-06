import discord
from discord.ext import commands
from TOKEN import TOKEN
from DM_helper import DM_helper, Character
from user_commands import do_login, do_logout, do_status, do_whoami, do_profile
from inventory_commands import do_additem, do_removeitem, do_equip, do_unequip, do_inventory
from dice_commands import do_roll, do_coinflip
from npc_commands import NPCCommands
from combat_commands import CombatCommands
from dm_commands import DMCommands
from help_commands import HelpCommands

intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents, help_command=None)
        self.dm = DM_helper()
        self.dm.logged_in_as = {}
        self.dm.logged_out = set()

    async def setup_hook(self):
        await self.add_cog(NPCCommands(self))
        await self.add_cog(CombatCommands(self))
        await self.add_cog(DMCommands(self))
        await self.add_cog(HelpCommands(self))

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        if message.author.bot:
            return
        username = f"{message.author.name}#{message.author.discriminator}"
        if username not in self.dm.logged_in_as and username not in self.dm.logged_out:
            try:
                default_char = Character.from_json("characters/rynn_dragonwhisper.json")
                self.dm.logged_in_as[username] = default_char
                self.dm.add_character(default_char)
                print(f"Auto-logged in {username} as Rynn")
            except:
                pass
        await self.process_commands(message)

bot = MyBot()

@bot.command()
async def login(ctx):
    username = f"{ctx.author.name}#{ctx.author.discriminator}"
    # clear any logout state
    ctx.bot.dm.logged_out.discard(username)
    res = await do_login(ctx.message, ctx.bot.dm)
    if isinstance(res, tuple):
        content, target = res
        if content:
            await target.send(content)

@bot.command()
async def logout(ctx):
    username = f"{ctx.author.name}#{ctx.author.discriminator}"
    res = await do_logout(ctx.message, ctx.bot.dm)
    if isinstance(res, tuple):
        content, target = res
        if content:
            await target.send(content)
        ctx.bot.dm.logged_out.add(username)

@bot.command()
async def status(ctx):
    res = await do_status(ctx.message, bot.dm)
    if isinstance(res, tuple):
        content, target = res
        if content:
            await target.send(content)

@bot.command()
async def whoami(ctx):
    res = await do_whoami(ctx.message, bot.dm)
    if isinstance(res, tuple):
        content, target = res
        if content:
            await target.send(content)

@bot.command()
async def profile(ctx):
    res = await do_profile(ctx.message, bot.dm)
    if isinstance(res, tuple):
        content, target = res
        if content:
            await target.send(content)

@bot.command()
async def additem(ctx):
    res = await do_additem(ctx.message, bot.dm)
    if isinstance(res, tuple):
        content, target = res
        if content:
            await target.send(content)

@bot.command()
async def removeitem(ctx):
    res = await do_removeitem(ctx.message, bot.dm)
    if isinstance(res, tuple):
        content, target = res
        if content:
            await target.send(content)

@bot.command()
async def equip(ctx):
    res = await do_equip(ctx.message, bot.dm)
    if isinstance(res, tuple):
        content, target = res
        if content:
            await target.send(content)

@bot.command()
async def unequip(ctx):
    res = await do_unequip(ctx.message, bot.dm)
    if isinstance(res, tuple):
        content, target = res
        if content:
            await target.send(content)

@bot.command(name='inventory')
async def inventory_cmd(ctx):
    res = await do_inventory(ctx.message, bot.dm)
    if isinstance(res, tuple):
        content, target = res
        if content:
            await target.send(content)

@bot.command()
async def roll(ctx):
    res = await do_roll(ctx.message)
    if isinstance(res, tuple):
        content, target = res
        if content:
            await target.send(content)

@bot.command()
async def coinflip(ctx):
    res = await do_coinflip(ctx.message)
    if isinstance(res, tuple):
        content, target = res
        if content:
            await target.send(content)

bot.run(TOKEN)
