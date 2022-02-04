from cards import *

""" This is a module that handles a few different card games.

Originally intended for poker game use with Jordan Vo's Rolepy system.
"""

def play_poker_game(message):
    member = message.author
    username = "%s#%s" % (member.name, member.discriminator)
    bet = 0
    chips = dealer.poker_chips[username]
    min_bet, max_bet = dealer.MIN_MAX_BET_AMOUNTS[dealer.betting_level]
    waiting_for_bet = True
    await message.author.send("Starting a 1 on 1 game of poker.")
    while waiting_for_bet == True:
        await member.send("%s, you currently have %i poker chips to bet with. How many would you like to bet?" % (member.name, chips))
        try:
            msg = await client.wait_for('message', timeout=30.0)
            try:
                bet = int(msg.content)
            except ValueError:
                await member.send("I did not get a valid amount. [You said: %s] Please try again." % (msg.content))
                continue
            if bet > chips:
                await member.send('%s, you do not have enough chips to bet %s.'
                                  ' Please try again. [You have %i chips.]' % (username, bet, chips))
            elif bet <= chips:
                if bet <= max_bet and bet >= min_bet:
                    await member.send('%s, you have successfully bet %i chips.' % (username, bet))
                    waiting_for_bet = False
                    player = Card_Player(username)
                    dealer.add_player(player)
                    dealer.add_bet(username, bet)
                    dealer.start_game()
                elif bet < min_bet:
                    await member.send('Sorry %s, you cannot bet less than the minimum bet. [Min bet:%s]' % (username, max_bet))
                elif bet > max_bet:
                    await member.send('Sorry %s, you cannot bet more than the maximum bet. [Max bet:%s]' % (username, max_bet))
        except asyncio.TimeoutError:
            await message.author.send("I waited for you to place a bet! [Timeout 30 seconds]")
            waiting_for_bet = False

    ###      Poker Game Loop     ###
    while dealer.game_in_progress == True:
        turn_player = dealer.get_turn_player()
        name = turn_player.player_name
        cards_in_hand = turn_player.print_hand()
        await message.author.send("It's %s's turn!" % (name))
        await message.author.send("Your cards are:\n %s"
                    "Which cards which you like to trade this turn?\n"
                          "[You can trade 3 cards at most.]" % (cards_in_hand))
        try:
            msg = await client.wait_for('message', timeout=10.0)
            if msg:
                cards_received = dealer.trade_in_cards(msg, turn_player)
                await message.author.send("You traded (%s) and got (%s) back."
                                          % msg, cards_received)
                dealer.next_player()
        except asyncio.TimeoutError:
            await message.author.send("It's your turn! Which cards would you like to trade? [30 seconds left]")
            msg = await client.wait_for('message', timeout=10.0)
            dealer.next_player()
            await message.author.send("Your turn is now over! [60 seconds has elapsed]")


def play_poker():
    dealer = Poker_Card_Dealer()