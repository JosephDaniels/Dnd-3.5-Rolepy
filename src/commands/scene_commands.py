import os
import json
import discord
from discord.ext import commands
import openai

scene_registry = {}          # { guild_id: scene_name }
scene_descriptions = {}      # { guild_id: description }
scene_backgrounds = {}       # { guild_id: background_url }
scene_maps = {}              # { guild_id: map_url }

class SceneCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setscene')
    async def set_scene(self, ctx, *, scene_name: str):
        scene_registry[ctx.guild.id] = scene_name
        await ctx.send(f"📍 Scene set to **{scene_name}**.")

    @commands.command(name='describe')
    async def describe_scene(self, ctx, *, description: str):
        if ctx.guild.id not in scene_registry:
            await ctx.send("❌ No scene set. Use `!setscene <name>` first.")
            return
        scene_descriptions[ctx.guild.id] = description
        await ctx.send(f"📝 Description for **{scene_registry[ctx.guild.id]}** updated.")

    @commands.command(name='scene')
    async def show_scene(self, ctx):
        scene = scene_registry.get(ctx.guild.id)
        if not scene:
            await ctx.send("❌ No scene set. Use `!setscene <name>` to set one.")
            return
        desc = scene_descriptions.get(ctx.guild.id, "(no description)")
        bg = scene_backgrounds.get(ctx.guild.id)
        mp = scene_maps.get(ctx.guild.id)
        lines = [f"**Scene:** {scene}", f"**Description:** {desc}"]
        if bg:
            lines.append(f"**Background:** {bg}")
        if mp:
            lines.append(f"**Map:** {mp}")
        await ctx.send("\n".join(lines))

    @commands.command(name='resetscene')
    async def reset_scene(self, ctx):
        scene_registry.pop(ctx.guild.id, None)
        scene_descriptions.pop(ctx.guild.id, None)
        scene_backgrounds.pop(ctx.guild.id, None)
        scene_maps.pop(ctx.guild.id, None)
        await ctx.send("🔄 Scene has been reset.")

    @commands.command(name='setbackground')
    async def set_background(self, ctx, *, url: str):
        if ctx.guild.id not in scene_registry:
            await ctx.send("❌ Set a scene first with `!setscene <name>`.")
            return
        scene_backgrounds[ctx.guild.id] = url
        await ctx.send(f"🖼️ Background for **{scene_registry[ctx.guild.id]}** set to: {url}")

    @commands.command(name='background')
    async def show_background(self, ctx):
        bg = scene_backgrounds.get(ctx.guild.id)
        if not bg:
            await ctx.send("❌ No background set. Use `!setbackground <url>`.")
            return
        await ctx.send(f"**Background:** {bg}")

    @commands.command(name='setmap')
    async def set_map(self, ctx, *, map_url: str):
        if ctx.guild.id not in scene_registry:
            await ctx.send("❌ Set a scene first with `!setscene <name>`.")
            return
        scene_maps[ctx.guild.id] = map_url
        await ctx.send(f"🗌️ Map for **{scene_registry[ctx.guild.id]}** set to: {map_url}")

    @commands.command(name='map')
    async def show_map(self, ctx):
        mp = scene_maps.get(ctx.guild.id)
        if not mp:
            await ctx.send("❌ No map set. Use `!setmap <url>`.")
            return
        await ctx.send(f"**Map:** {mp}")

    @commands.command(name='save_scene')
    async def save_scene(self, ctx):
        scene = scene_registry.get(ctx.guild.id)
        if not scene:
            await ctx.send("❌ No scene to save.")
            return
        desc = scene_descriptions.get(ctx.guild.id, "")
        bg = scene_backgrounds.get(ctx.guild.id, "")
        mp = scene_maps.get(ctx.guild.id, "")
        filename = scene.lower().replace(" ", "_")
        os.makedirs("../scenes", exist_ok=True)
        path = os.path.join("../scenes", f"{filename}.json")
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({
                    "scene": scene,
                    "description": desc,
                    "background": bg,
                    "map": mp
                }, f, indent=2)
            await ctx.send(f"📂 Scene **{scene}** saved to `{path}`.")
        except Exception as e:
            await ctx.send(f"❌ Error saving scene: {e}")

    @commands.command(name='load_scene')
    async def load_scene(self, ctx, *, scene_name: str):
        filename = scene_name.lower().replace(" ", "_") + ".json"
        path = os.path.join("../scenes", filename)
        if not os.path.exists(path):
            await ctx.send("❌ Scene file not found.")
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                scene_registry[ctx.guild.id] = data.get("scene", scene_name)
                scene_descriptions[ctx.guild.id] = data.get("description", "")
                scene_backgrounds[ctx.guild.id] = data.get("background", "")
                scene_maps[ctx.guild.id] = data.get("map", "")
            await ctx.send(f"✅ Scene **{data['scene']}** loaded from `{path}`.")
        except Exception as e:
            await ctx.send(f"❌ Error loading scene: {e}")

    @commands.command(name='scene_generate')
    async def generate_scene(self, ctx):
        current_scene = scene_registry.get(ctx.guild.id, "unknown location")
        prompt = f"Describe a vivid, immersive fantasy scene that could logically occur near or within a {current_scene}. Include evocative sensory details, and assume this is a scene transition in a dark fantasy setting."
        await ctx.send("🧠 Generating scene... (thinking...)")
        try:
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a scene-describing AI for a fantasy RPG."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.9
            )
            generated = response.choices[0].message.content.strip()
            scene_descriptions[ctx.guild.id] = generated
            await ctx.send(f"""🎭 Scene transition:\n{generated}""")
        except Exception as e:
            await ctx.send(f"❌ Error generating scene: {e}")

def setup(bot):
    bot.add_cog(SceneCommands(bot))
