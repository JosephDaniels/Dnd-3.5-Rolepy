
### This is for a Rock Paper Scissors game!! ###

async def do_rock_paper_scissors(message):
    """ Gives a random result, rock, paper or scissors.
        If you give it an argument, it will try to play against you.
        If you win, lose or tie, it will tell you.
        Everything gets returned in the response variable."""
    bonus_message = ""  # victory, tie or loss message
    victory_message = " You win!!!"
    lose_message = " You lose!!!"
    if message == "!rockpaperscissors" or "!rps":  # Solo play
        bot_throw = rock_paper_scissors()  # returns a string = 'rock' 'paper' or 'scissors'

    ### THIS ENTIRE VS AI PART DOESN'T WORK!!!!
    else:  # Against the bot
        print("against the bot block")
        player_throw = message.content.split(" ")[1].strip()  # should be 'rock' 'paper' or 'scissors'
        bot_throw = rock_paper_scissors()  # should be 'rock' 'paper' or 'scissors'
        if player_throw == bot_throw:  ## detects a tie
            bonus_message = " It's a tie. Thats means we both lose."
        elif player_throw == "rock" and bot_throw == "scissors":
            bonus_message = "Rock breaks scissors." + victory_message
        elif player_throw == "paper" and bot_throw == "rock":
            bonus_message = "Paper covers rock." + victory_message
        elif player_throw == "scissors" and bot_throw == "paper":
            bonus_message = "Scissors cuts paper." + victory_message
        else:
            bonus_message = lose_message
        bonus_message = " (Player threw %s. Bot threw %s.)" % (player_throw, bot_throw) + bonus_message
    response = "%s is playing Rock, Paper, Scissors! Are you ready...?" \
               " Rock! Paper! Scissors. . . %s!!! %s" % (message.author, bot_throw, bonus_message)
    return response, message.channel