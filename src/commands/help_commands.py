## help_commands.py

## halp

from discord.ext import commands
from src.help_messages import (
    HELP_LOGIN_MESSAGE,
    HELP_WHOIS_MESSAGE,
    HELP_ROLL,
    HELP_GENERAL_MESSAGE,
    HELP_LAST_UPDATED
)

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.categories = {
            'user': ['login','logout','status','whoami','profile'],
            'inventory': ['additem','removeitem','equip','unequip','inventory'],
            'combat': ['attack','defend','look','search','open','pickup','drop','unlock','hide','move'],
            'npc': ['npc','npc_list','npc_detail'],
            'dm': ['askdm','explore'],
            'dice': ['roll','coinflip']
        }

    @commands.command(name='help')
    async def help(self, ctx, topic: str = None):
        if not topic:
            cat_list = ', '.join(self.categories.keys())
            message = HELP_GENERAL_MESSAGE + f"""
**Help Categories:** {cat_list}
Type `!help <category>` to see commands in that category.
"""
            await ctx.send(message)
            return
        t = topic.lower()
        if t == 'login':
            await ctx.send(HELP_LOGIN_MESSAGE)
        elif t == 'whois':
            await ctx.send(HELP_WHOIS_MESSAGE)
        elif t in ('roll','dice'):
            await ctx.send(HELP_ROLL)
        elif t in ('general','commands'):
            await ctx.send(HELP_GENERAL_MESSAGE)
        elif t in ('last','updated'):
            await ctx.send(HELP_LAST_UPDATED)
        elif t in self.categories:
            cmds = self.categories[t]
            lines = [f"**{t.capitalize()} Commands:**"] + [f"- `!{c}`" for c in cmds]
            await ctx.send("\n".join(lines))
        else:
            cat_list = ', '.join(self.categories.keys())
            await ctx.send(f"No help available for `{topic}`. Available categories: {cat_list}")

def setup(bot):
    bot.add_cog(HelpCommands(bot))
