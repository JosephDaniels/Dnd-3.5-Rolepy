import discord
from discord.ext import commands

class DMCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dm = getattr(bot, 'dm', None)

    @commands.command(name='askdm')
    async def askdm(self, ctx, *, question: str):
        if hasattr(self.dm, 'ask'):
            response = await self.dm.ask(question)
        else:
            response = f"🤖 DM response to: {question}"
        await ctx.send(response)

    @commands.command(name='explore')
    async def explore(self, ctx):
        if hasattr(self.dm, 'explore'):
            description = await self.dm.explore()
        else:
            description = "🌲 You explore the surroundings and find nothing noteworthy."
        await ctx.send(description)

def setup(bot):
    bot.add_cog(DMCommands(bot))
