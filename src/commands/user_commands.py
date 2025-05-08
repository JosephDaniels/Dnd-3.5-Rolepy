import os
import json
from discord.ext import commands
from src.character.charactersheet import CharacterSheet

HELP_LOGIN = "Usage: !login <character_name>"
LOGIN_FILE = "../../data/logged_in.json"
logins = {}
active_chars = {}


# Restore saved sessions
if os.path.exists(LOGIN_FILE):
    with open(LOGIN_FILE, encoding='utf-8') as f:
        logins = json.load(f)
    for user_key, name in logins.items():
        path = f"character_sheets/{name.lower()}.json"
        if os.path.exists(path):
            char = CharacterSheet.from_json(path)
            active_chars[user_key] = char

class UserCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="login")
    async def login(self, ctx, *, target_character: str = None):
        username = f"{ctx.author.name}#{ctx.author.discriminator}"
        if not target_character:
            return await ctx.send(HELP_LOGIN)
        if username in active_chars:
            return await ctx.send(f"{username}, you are already logged in as {active_chars[username].name}.")
        characters_dir = "character_sheets"
        if not os.path.isdir(characters_dir):
            return await ctx.send(f"No character_sheets directory found.")
        matches = [f for f in os.listdir(characters_dir)
                   if f.lower().startswith(target_character.lower()) and f.lower().endswith('.json')]
        if not matches:
            return await ctx.send(f"Character '{target_character}' not found.")
        if len(matches) > 1:
            options = ', '.join(m[:-5] for m in matches)
            return await ctx.send(f"Multiple matches found: {options}. Please specify more precisely.")
        filename = matches[0]
        char_name = filename[:-5]
        path = os.path.join(characters_dir, filename)
        char = CharacterSheet.from_json(path)
        active_chars[username] = char
        logins[username] = char.name
        os.makedirs(os.path.dirname(LOGIN_FILE) or '.', exist_ok=True)
        with open(LOGIN_FILE, 'w', encoding='utf-8') as f:
            json.dump(logins, f)
        await ctx.send(f"Successfully logged in as **{char.name}**.")

    @commands.command(name="logout")
    async def logout(self, ctx):
        username = f"{ctx.author.name}#{ctx.author.discriminator}"
        char = active_chars.pop(username, None)
        if char:
            logins.pop(username, None)
            with open(LOGIN_FILE, 'w', encoding='utf-8') as f:
                json.dump(logins, f)
            return await ctx.send(f"{username}, your character {char.name} has been logged out and saved.")
        await ctx.send("You're not logged in!")

    @commands.command(name="status")
    async def status(self, ctx):
        username = f"{ctx.author.name}#{ctx.author.discriminator}"
        char = active_chars.get(username)
        if not char:
            return await ctx.send("You're not logged in!")
        hp = f"{char.physical_status.current_health}/{char.physical_status.max_health}"
        hunger = char.physical_status.hunger_state()
        thirst = char.physical_status.thirst_state()
        mood = char.mental_status.overall_mood()
        msg = (
            f"**{char.name}** | Level {char.total_level()} | "
            f"HP: {hp} | Hunger: {hunger} | Thirst: {thirst} | Mood: {mood}"
        )
        await ctx.send(msg)

    @commands.command(name="whoami")
    async def whoami(self, ctx):
        username = f"{ctx.author.name}#{ctx.author.discriminator}"
        char = active_chars.get(username)
        if not char:
            return await ctx.send("You're not logged in.")
        await ctx.send(f"**You are logged in as {char.name}**")

async def setup(bot):
    await bot.add_cog(UserCog(bot))

