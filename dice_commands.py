# dice_commands.py
from DM_helper import parse_dice_command, coinflip
async def do_coinflip(message):
    result = coinflip()
    return f"{message.author} flips a coin! Result is {result}.", message.channel


async def do_roll(message):
    username = f"{message.author.name}#{message.author.discriminator}"
    command_line = message.content
    dice_total, num_dice, results, dice_type, modifier = parse_dice_command(command_line)
    response = f"{username} rolled a {dice_total} on a {num_dice}{dice_type}. Results: {results}{modifier}"
    return response, message.channel
