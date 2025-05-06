import discord
from discord.ext import commands

npc_registry = []  # List of NPC descriptions

class NPCCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="npc")
    async def create_npc(self, ctx, *, npc_text: str):
        npc_registry.append(npc_text)
        await ctx.send("✅ NPC added to registry.")

    @commands.command(name="npc_list")
    async def list_npcs(self, ctx):
        if not npc_registry:
            await ctx.send("No NPCs have been added yet.")
            return
        lines = [f"{i+1}. {npc_registry[i].splitlines()[0]}" for i in range(len(npc_registry))]
        await ctx.send("**NPCs:**\n" + "\n".join(lines))

    @commands.command(name="npc_detail")
    async def npc_detail(self, ctx, index: int):
        if index < 1 or index > len(npc_registry):
            await ctx.send("❌ Invalid NPC number.")
            return
        await ctx.send(f"NPC #{index}:\n\n{npc_registry[index-1]}")


def setup(bot):
    bot.add_cog(NPCCommands(bot))
