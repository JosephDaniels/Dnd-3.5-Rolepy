import os
import json
import discord
from discord.ext import commands
from openai import AsyncOpenAI
import re

npc_registry = []  # List of NPC descriptions
openai_client = AsyncOpenAI()

class NPCCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def generate_npc_description(self, prompt):
        try:
            response = await openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": (
                        "You are a dungeon_master creating NPC stat blocks for a fantasy RPG. "
                        "If the prompt suggests a simple animal or mundane creature, generate basic stats accordingly—"
                        "referencing official 5e or SRD monster stat blocks when needed. Format the output like a character sheet "
                        "with a realistic paragraph of description. Do not assign magical classes or powers to ordinary animals unless explicitly prompted."
                    )},
                    {"role": "user", "content": f"Create an NPC based on: {prompt}"}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[Error generating NPC: {e}]"

    @commands.command(name="npc")
    async def create_npc(self, ctx, *, npc_text: str):
        await ctx.send("🧠 Generating NPC stat block...")
        npc_description = await self.generate_npc_description(npc_text)
        npc_registry.append(npc_description)
        await ctx.send("✅ NPC added to registry.")

    @commands.command(name="npc_list")
    async def list_npcs(self, ctx):
        if not npc_registry:
            await ctx.send("No NPCs have been added yet.")
            return
        lines = [f"{i+1}. {npc_registry[i].splitlines()[0]}" for i in range(len(npc_registry))]
        await ctx.send("**NPCs:**\n" + "\n".join(lines))

    @commands.command(name="npc_detail")
    async def npc_detail(self, ctx, index: int = None):
        if index is None:
            await ctx.send("❌ Please provide the NPC number. Try `!npc_list` to see the available NPCs.")
            return
        if index < 1 or index > len(npc_registry):
            await ctx.send("❌ Invalid NPC number.")
            return
        await ctx.send(f"NPC #{index}:\n\n{npc_registry[index-1]}")

    @commands.command(name="save_npc")
    async def save_npc(self, ctx, index: int = None):
        if index is None or index < 1 or index > len(npc_registry):
            await ctx.send("❌ Invalid NPC index.")
            return
        npc_data = npc_registry[index - 1]
        lines = npc_data.splitlines()
        name_line = lines[0].strip()
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '', name_line.replace(' ', '_')).lower()
        os.makedirs("../npc", exist_ok=True)
        path = os.path.join("../npc", f"{safe_name}.json")
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"name": name_line, "description": npc_data}, f, indent=2)
            await ctx.send(f"📂 NPC #{index} saved to `npc/{safe_name}.json`.")
        except Exception as e:
            await ctx.send(f"❌ Error saving NPC: {e}")

    @commands.command(name="load_npc")
    async def load_npc(self, ctx, *, filename: str):
        if not filename.endswith(".json"):
            filename += ".json"
        path = os.path.join("../npc", filename)
        if not os.path.exists(path):
            await ctx.send("❌ NPC file not found.")
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                npc_registry.append(data["description"])
                await ctx.send(f"✅ NPC `{data['name']}` loaded into registry.")
        except Exception as e:
            await ctx.send(f"❌ Error loading NPC: {e}")

def setup(bot):
    bot.add_cog(NPCCommands(bot))
