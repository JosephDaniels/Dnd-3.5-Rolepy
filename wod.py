def handle_roll_wod(message, eight_again=False, nine_again=False):
    cmd, dice_pool = message.content.split(" ")
    dice_pool = int(dice_pool)
    username = message.author
    dice_results, successes, rerolls = roll_wod_dice(dice_pool, eight_again, nine_again)

    extra_text = ""
    if eight_again == True:
        extra_text = " with eight-again"
    elif nine_again == True:
        extra_text = " with nine-again"

    if successes == 0:
        return "%s rolled %i dice and failed their roll%s. Dice Results: %s" % (
            username, dice_pool, extra_text, dice_results)
    elif successes > 0:
        if rerolls > 0:
            return "%s rolled %i dice and received %i successes%s. They had %i rerolled dice. Dice Results: %s" % (
                username, dice_pool, successes, extra_text, rerolls, dice_results)
        else:
            return "%s rolled %i dice and had %i successes%s. Dice Results: %s" % (
                username, dice_pool, successes, extra_text, dice_results)

async def do_roll(message):
    username = "%s#%s" % (message.author.name, message.author.discriminator)
    command_line = message.content  # E.g. !roll3d8

    if message.content.startswith("!rollwod"):
        try:
            command, dice_pool = message.content.split(" ")
        except ValueError:
            response = "Sorry that didn't work. Try again."
            return response, message.channel
        if command == "!rollwod":
            response = handle_roll_wod(message, dice_pool)
        elif command == ("!rollwod8again"):
            response = handle_roll_wod(message, dice_pool, eight_again=True)
        elif command == ("!rollwod9again"):
            response = handle_roll_wod(message, dice_pool, nine_again=True)

    elif message.content.startswith('!rollchancedie'):
        dice_result = rolld(10)
        if dice_result == 1:
            response = "%s rolled a chance die and suffered a dramatic failure. [Rolled 1 on a d10]" % (username)
        elif dice_result == 10:
            response = "%s rolled a chance die and managed to succeed. [Rolled 10 on a d10]" % (username)
        else:
            response = "%s rolled a chance die and failed. [Rolled %s on a d10]" % (username, dice_result)

    cmd = message.content
    dice_total, num_dice, results, dice_type, modifier = parse_dice_command(command_line)  # Pulls the
    response = "%s rolled a %i on a %i%s. Results: %s%s" % (username,
                                                            dice_total,
                                                            num_dice,
                                                            dice_type,
                                                            results,
                                                            modifier)
    return response, message.channel