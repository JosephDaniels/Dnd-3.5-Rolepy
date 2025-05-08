from discord.ext import commands
from user_commands import active_chars
from src.inventory.consumable import get_consumable, Food, Drink

class ConsumableCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_character(self, user):
        username = f"{user.name}#{user.discriminator}"
        return active_chars.get(username)

    @commands.command(name="eat")
    async def eat(self, ctx, *, item: str):
        character = self.get_character(ctx.author)
        if not character:
            await ctx.send("You are not logged in.")
            return

        if item not in character.inventory or character.inventory[item] <= 0:
            await ctx.send(f"You don't have any {item} to eat.")
            return

        consumable = get_consumable(item)
        if not consumable or not isinstance(consumable, Food):
            await ctx.send(f"{item} is not edible.")
            return

        msg = consumable.apply(character)
        character.inventory[item] -= 1
        if character.inventory[item] <= 0:
            del character.inventory[item]

        character.save_to_json()
        await ctx.send(msg)

    @commands.command(name="drink")
    async def drink(self, ctx, *, item: str):
        character = self.get_character(ctx.author)
        if not character:
            await ctx.send("You are not logged in.")
            return

        if item not in character.inventory or character.inventory[item] <= 0:
            await ctx.send(f"You don't have any {item} to drink.")
            return

        consumable = get_consumable(item)
        if not consumable or not isinstance(consumable, Drink):
            await ctx.send(f"{item} is not drinkable.")
            return

        msg = consumable.apply(character)
        character.inventory[item] -= 1
        if character.inventory[item] <= 0:
            del character.inventory[item]

        character.save_to_json()
        await ctx.send(msg)

async def setup(bot):
    await bot.add_cog(ConsumableCog(bot))
