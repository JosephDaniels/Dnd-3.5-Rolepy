import json
from discord.ext import commands
# from user_commands import active_chars, logins, LOGIN_FILE

HELP_SET = "Usage: !set <stat> <value>"

MOOD_PRESETS = {
    "happy": "Happy",
    "sad": "Sad",
    "neutral": "Neutral",
    "angry": "Angry",
    "anxious": "Anxious",
    "excited": "Excited",
    "tired": "Tired",
    "focused": "Focused",
    "horny": "Flirty",
    "bored": "Bored",
    "playful": "Playful",
    "confident": "Confident",
    "uncomfortable": "Uncomfortable",
    "chillin": "Chillin'",
    "inspired": "Inspired",
    "grateful": "Grateful",
    "loved": "Loved",
    "paranoid": "Paranoid",
    "guilty": "Guilty",
    "jealous": "Jealous"
}

MOOD_BAR_VALUES = {
    "happy":        {"happiness": 80.0, "sadness": 10.0, "anger": 5.0,  "stress": 10.0},
    "sad":          {"happiness": 20.0, "sadness": 80.0, "anger": 5.0,  "stress": 30.0},
    "angry":        {"happiness": 10.0, "sadness": 20.0, "anger": 80.0, "stress": 50.0},
    "anxious":      {"fear": 60.0,      "stress": 70.0,  "sadness": 40.0},
    "excited":      {"happiness": 85.0, "arousal": 75.0, "inspiration": 60.0},
    "tired":        {"stamina": 20.0,    "sleep": 15.0,   "stress": 40.0},
    "focused":      {"focus": 80.0,      "stress": 20.0},
    "bored":        {"boredom": 80.0,    "happiness": 20.0},
    "playful":      {"happiness": 70.0,  "boredom": 10.0,  "arousal": 60.0},
    "confident":    {"happiness": 70.0,  "fear": 10.0,      "courage": 80.0},
    "uncomfortable":{"stress": 60.0,     "fear": 50.0},
    "chillin":      {"relaxation": 80.0,  "stress": 10.0},
    "inspired":     {"inspiration": 85.0, "hope": 70.0},
    "grateful":     {"happiness": 75.0,  "hope": 70.0},
    "loved":        {"happiness": 80.0,  "social": 75.0},
    "paranoid":     {"fear": 70.0,       "stress": 80.0},
    "guilty":       {"shame": 70.0,      "stress": 60.0},
    "jealous":      {"anger": 60.0,      "sadness": 40.0},
    "horny":        {"arousal": 85.0,    "libido": 80.0},
    "neutral":      {"happiness": 50.0,  "sadness": 50.0,  "anger": 50.0,  "fear": 50.0,  "stress": 50.0}
}

class DebugCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="set")
    async def set_stat(self, ctx, stat: str = None, *, value: str = None):
        if not stat or not value:
            return await ctx.send(HELP_SET)
        key = f"{ctx.author.name}#{ctx.author.discriminator}"
        char = active_chars.get(key)
        if not char:
            return await ctx.send("No active character.")
        ps = char.physical_status
        ms = char.mental_status
        stat_low = stat.lower()
        if stat_low in ("hunger", "thirst", "current_health", "max_health", "temp_health"):
            try:
                num = float(value)
            except ValueError:
                return await ctx.send(f"Invalid number: {value}")
            if stat_low == "hunger":
                ps.hunger = max(0.0, min(100.0, num))
            elif stat_low == "thirst":
                ps.thirst = max(0.0, min(100.0, num))
            elif stat_low == "current_health":
                ps.current_health = max(0.0, min(ps.max_health, num))
            elif stat_low == "max_health":
                ps.max_health = max(1.0, num)
                ps.current_health = min(ps.current_health, ps.max_health)
            elif stat_low == "temp_health":
                ps.temp_health = max(0.0, num)
        elif stat_low == "mood":
            preset = value.lower()
            if preset not in MOOD_PRESETS:
                return await ctx.send(f"Unknown mood: {value}. Valid: {', '.join(MOOD_PRESETS.keys())}")
            ms.mood = MOOD_PRESETS[preset]
            if preset in MOOD_BAR_VALUES:
                for bar, val in MOOD_BAR_VALUES[preset].items():
                    setattr(ms, bar, max(0.0, min(100.0, val)))
        else:
            return await ctx.send(f"Unknown stat: {stat_low}")
        logins[key] = char.name
        with open(LOGIN_FILE, 'w', encoding='utf-8') as f:
            json.dump(logins, f)
        char.save_to_json()
        await ctx.send(f"Set {stat_low} to {value} for **{char.name}**.")


async def setup(bot):
    await bot.add_cog(DebugCog(bot))

