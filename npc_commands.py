import discord
from discord.ext import commands

# This will hold NPCs by region
npc_registry = {}  # { region_name: [npc_response1, npc_response2, ...] }

# This holds the current scene per guild
current_scenes = {}  # { guild_id: region_name }

def get_current_scene(ctx):
    return current_scenes.get(ctx.guild.id, "default")

class NPCCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setscene")
    async def set_scene(self, ctx, *, region_name):
        current_scenes[ctx.guild.id] = region_name
        await ctx.send(f"📍 Scene set to: **{region_name}**")

    @commands.command(name="npc")
    async def create_npc(self, ctx, *, npc_text):
        region = get_current_scene(ctx)
        if region not in npc_registry:
            npc_registry[region] = []
        npc_registry[region].append(npc_text)
        await ctx.send(f"✅ NPC added to **{region}**.")

    @commands.command(name="npc_list")
    async def list_npcs(self, ctx):
        region = get_current_scene(ctx)
        npcs = npc_registry.get(region, [])
        if not npcs:
            await ctx.send(f"No NPCs found in **{region}**.")
            return

        header = f"NPCs in **{region}**:\n"
        lines = []
        for i, npc in enumerate(npcs, start=1):
            snippet = npc.split("\n")[0]
            lines.append(f"{i}. {snippet}")

        # Split into chunks below 2000 characters
        message = header
        for line in lines:
            if len(message) + len(line) + 1 > 2000:
                await ctx.send(message)
                message = ""
            message += line + "\n"
        if message:
            await ctx.send(message)

    @commands.command(name="npc_detail")
    async def npc_detail(self, ctx, index: int):
        region = get_current_scene(ctx)
        npcs = npc_registry.get(region, [])
        if index < 1 or index > len(npcs):
            await ctx.send("❌ Invalid NPC number.")
            return
        await ctx.send(f"NPC #{index} in **{region}**:\n\n{npcs[index - 1]}")


def setup(bot):
    bot.add_cog(NPCCommands(bot))
