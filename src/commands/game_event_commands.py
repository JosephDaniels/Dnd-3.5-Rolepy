from datetime import datetime
from discord.ext import commands
from src.main_bot import active_chars

# Map of event keys to (mental_bar, delta, journal_message)
EVENT_MAP = {
    "quest_success": ("happiness", +20, "celebrated a grand victory!"),
    "companion_falls": ("sadness", +30, "grieved the loss of a friend."),
    "insulted": ("anger", +15, "grew angry at an insult."),
    "narrow_escape": ("fear", +25, "survived a hair-raising encounter."),
    # add additional mappings here...
}


def clamp(val, mn, mx):
    return max(mn, min(mx, val))


def trigger_event(user_id: str, event_key: str):
    """
    Adjusts a mental bar and logs a journal entry for a given user event.
    """
    if event_key not in EVENT_MAP:
        return False
    mental_bar, delta, msg = EVENT_MAP[event_key]
    char = active_chars.get(user_id)
    if not char:
        return False
    # adjust mental status
    current = getattr(char.mental_status, mental_bar, 0)
    new_val = clamp(current + delta, 0, 100)
    setattr(char.mental_status, mental_bar, new_val)
    # add to journal
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"[{timestamp}] {char.name} {msg}"
    if not hasattr(char, 'journal'):
        char.journal = []
    char.journal.append(entry)
    # save character
    char.save_to_json()
    return True


class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="journal")
    async def show_journal(self, ctx, lines: int = 10):
        key = str(ctx.author.id)
        char = active_chars.get(key)
        if not char:
            return await ctx.send("No active character.")
        journal = getattr(char, 'journal', [])
        if not journal:
            return await ctx.send("*Your journal is empty.*")
        # show last N entries
        to_show = journal[-lines:]
        formatted = "\n".join(to_show)
        await ctx.send(f"**{char.name}'s Journal:**\n{formatted}")

    @commands.command(name="write")
    async def write_journal(self, ctx, *, note: str):
        key = str(ctx.author.id)
        char = active_chars.get(key)
        if not char:
            return await ctx.send("No active character.")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = f"[{timestamp}] {note}"
        if not hasattr(char, 'journal'):
            char.journal = []
        char.journal.append(entry)
        char.save_to_json()
        await ctx.send("Entry added to your journal.")


def setup(bot):
    bot.add_cog(EventsCog(bot))
