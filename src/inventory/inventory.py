import os
import json
from discord.ext import commands
from src.commands.user_commands import active_chars, logins, LOGIN_FILE

class InventoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="additem")
    async def additem(self, ctx, item: str, qty: int = 1):
        key = f"{ctx.author.name}#{ctx.author.discriminator}"
        char = active_chars.get(key)
        if not char:
            return await ctx.send("No active character.")
        for _ in range(qty):
            char.inventory[item] = char.inventory.get(item, 0) + 1
        self._save(char, key)
        await ctx.send(f"Added {qty}x {item} to {char.name}'s inventory.")

    @commands.command(name="removeitem")
    async def removeitem(self, ctx, *, item: str):
        key = f"{ctx.author.name}#{ctx.author.discriminator}"
        char = active_chars.get(key)
        if not char:
            return await ctx.send("No active character.")
        inv = char.inventory
        found = next((k for k in inv if k.lower() == item.lower()), None)
        if not found:
            return await ctx.send(f"{item} not found in inventory.")
        del inv[found]
        self._save(char, key)
        await ctx.send(f"Removed {found} from {char.name}'s inventory.")

    @commands.command(name="equip")
    async def equip(self, ctx, *, item: str):
        key = f"{ctx.author.name}#{ctx.author.discriminator}"
        char = active_chars.get(key)
        if not char:
            return await ctx.send("No active character.")
        inv = char.inventory
        found = next((k for k in inv if k.lower() == item.lower()), None)
        if not found:
            return await ctx.send(f"You don't have {item}.")
        char.equipment[found] = inv.pop(found)
        self._save(char, key)
        await ctx.send(f"{char.name} equipped {found}.")

    @commands.command(name="unequip")
    async def unequip(self, ctx, *, item: str):
        key = f"{ctx.author.name}#{ctx.author.discriminator}"
        char = active_chars.get(key)
        if not char:
            return await ctx.send("No active character.")
        eq = char.equipment
        found = next((k for k in eq if k.lower() == item.lower()), None)
        if not found:
            return await ctx.send(f"{item} is not equipped.")
        char.inventory[found] = eq.pop(found)
        self._save(char, key)
        await ctx.send(f"{char.name} unequipped {found}.")

    @commands.command(name="inventory")
    async def inventory(self, ctx):
        key = f"{ctx.author.name}#{ctx.author.discriminator}"
        char = active_chars.get(key)
        if not char:
            return await ctx.send("No active character.")
        inv = char.inventory
        eq = char.equipment
        inv_list = ', '.join(f"{k}x{v}" for k, v in inv.items()) or 'Empty'
        eq_list = ', '.join(eq.keys()) or 'None'
        await ctx.send(f"**Inventory**: {inv_list}\n**Equipment**: {eq_list}")

    def _save(self, char, key):
        logins[key] = char.name
        os.makedirs(os.path.dirname(LOGIN_FILE) or '.', exist_ok=True)
        with open(LOGIN_FILE, 'w', encoding='utf-8') as f:
            json.dump(logins, f)
        char.save_to_json()


def setup(bot):
    bot.add_cog(InventoryCog(bot))
