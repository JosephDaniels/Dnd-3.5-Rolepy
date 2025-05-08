import discord
from discord.ext import commands

class DMCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dm = getattr(bot, 'dm', None)

    @commands.command(name='askdm')
    async def askdm(self, ctx, *, question: str):
        if self.dm and callable(getattr(self.dm, 'ask', None)):
            response = await self.dm.ask(question, ctx)
        else:
            response = "[Error: DM system is not initialized or missing 'ask' method.]"
        await ctx.send(response)

    @commands.command(name='explore')
    async def explore(self, ctx):
        if self.dm and callable(getattr(self.dm, 'explore', None)):
            description = await self.dm.explore()
        else:
            description = "[Error: DM system is not initialized or missing 'explore' method.]"
        await ctx.send(description)

async def setup(bot):
    await bot.add_cog(DMCommands(bot))
