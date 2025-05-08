import discord
from discord.ext import commands

class CombatCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='attack')
    async def attack(self, ctx, *, target: str):
        await ctx.send(f"⚔️ {ctx.author.display_name} attacks **{target}**!")

    @commands.command(name='defend')
    async def defend(self, ctx):
        await ctx.send(f"🛡️ {ctx.author.display_name} takes a defensive stance.")

    @commands.command(name='look')
    async def look(self, ctx, *, location: str = None):
        location_desc = location if location else "around carefully"
        await ctx.send(f"👀 {ctx.author.display_name} looks {location_desc}.")

    @commands.command(name='search')
    async def search(self, ctx, *, item: str = "the area"):
        await ctx.send(f"🔎 {ctx.author.display_name} searches {item}.")

    @commands.command(name='open')
    async def open_item(self, ctx, *, item: str):
        await ctx.send(f"📬 {ctx.author.display_name} opens the {item}.")

    @commands.command(name='pickup', aliases=['get'])
    async def pickup(self, ctx, *, item: str):
        await ctx.send(f"👐 {ctx.author.display_name} picks up {item}.")

    @commands.command(name='drop')
    async def drop(self, ctx, *, item: str):
        await ctx.send(f"📦 {ctx.author.display_name} drops {item}.")

    @commands.command(name='unlock')
    async def unlock(self, ctx, *, target: str):
        await ctx.send(f"🔑 {ctx.author.display_name} attempts to unlock {target}.")

    @commands.command(name='hide')
    async def hide(self, ctx):
        await ctx.send(f"🌳 {ctx.author.display_name} hides skillfully.")

    @commands.command(name='move')
    async def move(self, ctx, *, destination: str):
        await ctx.send(f"🚶 {ctx.author.display_name} moves towards {destination}.")

def setup(bot):
    bot.add_cog(CombatCommands(bot))
