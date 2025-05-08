import discord
from discord.ext import commands
import os
from user_commands import active_chars  # shared login state

class InventoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def save_character(self, character):
        character.save_to_json()  # ✅ uses built-in safe serializer

    def get_character(self, user):
        username = f"{user.name}#{user.discriminator}"
        return active_chars.get(username)

    @commands.command(name="additem")
    async def add_item(self, ctx, *, item: str):
        character = self.get_character(ctx.author)
        if not character:
            await ctx.send("No active character.")
            return
        character.inventory[item] = character.inventory.get(item, 0) + 1
        self.save_character(character)
        await ctx.send(f"Added 1x {item} to {character.name}'s inventory.")

    @commands.command(name="removeitem")
    async def remove_item(self, ctx, *, item: str):
        character = self.get_character(ctx.author)
        if not character:
            await ctx.send("No active character.")
            return
        if item not in character.inventory:
            await ctx.send(f"{item} not found in inventory.")
            return
        del character.inventory[item]
        self.save_character(character)
        await ctx.send(f"Removed {item} from {character.name}'s inventory.")

    @commands.command(name="equip")
    async def equip_item(self, ctx, *, item: str):
        character = self.get_character(ctx.author)
        if not character:
            await ctx.send("No active character.")
            return
        if item not in character.inventory:
            await ctx.send(f"You don't have {item}.")
            return
        character.equipment[item] = character.inventory.pop(item)
        self.save_character(character)
        await ctx.send(f"{character.name} equipped {item}.")

    @commands.command(name="unequip")
    async def unequip_item(self, ctx, *, item: str):
        character = self.get_character(ctx.author)
        if not character:
            await ctx.send("No active character.")
            return
        if item not in character.equipment:
            await ctx.send(f"{item} is not equipped.")
            return
        character.inventory[item] = character.equipment.pop(item)
        self.save_character(character)
        await ctx.send(f"{character.name} unequipped {item}.")

    @commands.command(name="inventory")
    async def show_inventory(self, ctx):
        character = self.get_character(ctx.author)
        if not character:
            await ctx.send("No active character.")
            return

        def format_item(k, v):
            return f"{k} x{v}" if isinstance(v, int) else f"{k}: {v}"

        inv_lines = [format_item(k, v) for k, v in character.inventory.items()]
        eq_lines = []
        for k, v in character.equipment.items():
            if isinstance(v, dict):
                desc = " | ".join(f"{key}: {val}" for key, val in v.items())
                eq_lines.append(f"{k} [{desc}]")
            else:
                eq_lines.append(f"{k}: {v}")

        lines = ["**Inventory**"] + inv_lines + ["**Equipment**"] + eq_lines
        await ctx.send("\n".join(lines) or "Inventory is empty.")

async def setup(bot):
    await bot.add_cog(InventoryCog(bot))
