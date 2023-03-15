from cards import *

import random

import time

VALID_SHOE_SIZES = [
    1, 2, 4, 6, 8
]

class Shoe(Deck):
    def __init__(self, shoe_size=1):
        self.cards = []
        for decks in range(shoe_size):
            deck = Deck()
            deck.shuffle()
            self.cards.extend(deck.cards)

    def show_shoe(self):
        explicit_shoe_contents = str(self.cards)
        num_cards = len(self.cards)
        response = "%s cards in shoe. Shoe contents = %s." % (num_cards, explicit_shoe_contents)
        return response

    def shuffle_shoe(self, debug=False):
        random.shuffle(self.cards)
        if debug == True:
            print (self.cards)

    def draw_a_card(self):
        """ Pulls a card from the top of the deck. """
        card = self.cards[0]
        self.cards.pop(0) # Remove card from the deck
        return card

class Blackjack_Dealer(Card_Dealer):
    """ A class that can handle blackjack."""
    def __init__(self, shoe_size = 2):
        ## The Dealer is always player eight and plays last.
        super().__init__()

        #Management Variables
        self.players = []
        self.current_player = 0
        self.final_scores = {} #Associates a player with a score

        # Game Settings
        self.shoe_size = shoe_size # Typically 1, 2, 4, 6 or maximum 8
        self.shoe = Shoe(self.shoe_size)
        self.hand_size = 2
        self.game_in_progress = False

        # Self Data
        self.hand = []
        self.name = "The Dealer"

        # DEBUG VAR
        self.debug = True

    def get_name(self, card):
        # Attain the value
        value = card.strip("CHSD")
        value = CARD_VALUE_NAMES[value]
        # Attain the suit
        suit = card.strip("A23456789TJQK")
        suit = CARD_SUIT_NAMES[suit]

        return value, suit

    def give_card_to(self, player):
        card = self.shoe.draw_a_card()
        player.hand.append(card)
        return card

    def deal_initial_cards(self):
        for cards in range(self.hand_size):
            for player in self.players:
                card = self.shoe.draw_a_card()
                player.add_to_hand(card)
                # Gets fancy card name
                value, suit = self.get_name(card)
                if self.debug == True:
                    print ("%s of %s was dealt to player %s." % (value, suit, player.name))
            #Draw a card for the Dealer
            card = self.shoe.draw_a_card()
            self.give_card_to(self)
            value, suit = self.get_name(card)
            if len(self.hand) == 1:
                print ("%s shows %s of %s." % (self.name, value, suit))
            elif len(self.hand) == 2:
                print ("%s places one card face down." % (self.name))

    def calculate_score_for(self, player):
        score = 0
        for card in player.hand:
            value = card.strip("CHSD")
            if value in ["T", "J", "Q", "K"]:
                score += 10
                continue
            elif value in ["2","3","4","5","6","7","8","9"]:
                score += int(value)
                continue
            elif value == "A":
                soft_score = score + 1
                hard_score = score+11
                score = str(soft_score)+"/"+str(hard_score)
                continue
        return score

    def start_blackjack_game(self):
        self.game_in_progress = True
        print ("No More Bets!")
        self.deal_initial_cards()
        print ("Good Luck!")
        self.main_loop()

    def determine_winner(self):
        bet = 1
        winnings = 1 #Default to 1 until we get chips working
        dealer_score = self.calculate_score_for(self)
        if dealer_score > 21:
            for player in self.players:
                player_score = self.calculate_score_for(player)
                if player_score <= 21:
                    print ("%s wins! They gain %i chip(s)." % (player.name, winnings))
        elif dealer_score <= 21:
            for player in self.players:
                player_score = self.calculate_score_for(player)
                if player_score <= 21 and player_score > dealer_score:
                    print ("%s wins! They gain %i chip(s)." % (player.name, winnings))
                elif player_score < dealer_score:
                    print("%s loses their bet of %i chip(s)." % (player.name, bet))

    def main_loop(self):
        while self.game_in_progress == True:
            turn_over = False
            if self.current_player == 8: # Dealer's turn
                print("%s's turn begins." % (self.name))
                score = self.calculate_score_for(self)
                print("%s opens %i. %s" % (self.name, score, self.hand))
                if score == 21:
                    print("%s has Blackjack. Game Over. [%s]" % (self.name, self.hand))
                    turn_over = True
                while turn_over == False:
                    if score < 17: #Hit until soft 17
                        print("%s hits!" % (self.name))
                        card = self.give_card_to(self)
                        value, suit = self.get_name(card)
                        print("%s of %s was dealt to %s." % (value, suit, self.name))
                        score = self.calculate_score_for(self)
                        print("Score is now %s." % (score))
                        time.sleep(1.0)
                    elif score >= 17 and score < 21:
                        print ("%s stands on %i." % (self.name, score))
                        turn_over = True
                    elif score > 21:
                        print("%s Busts! [Score was %s.]" % (self.name, score))
                        turn_over = True
                self.determine_winner()
                self.game_in_progress = False
            else:
                player = self.players[self.current_player]
                if self.calculate_score_for(player) == "11/21": # True Blackjack, turn over immediately
                    print ("%s has BlackJack! Nice! %s" % (player.name, player.hand))
                    turn_over = True
                while turn_over == False: # Player Turn
                    print("It is %s's turn." % (player.name))
                    score = self.calculate_score_for(player)
                    print("%s, you have %s. %s" % (player.name, score, player.hand))
                    response = input("Would you like to hit or stand?")
                    if response == "hit":
                        card = self.give_card_to(player)
                        score = self.calculate_score_for(player)
                        value, suit = self.get_name(card)
                        print("%s of %s was dealt to player %s. [%s]" % (value, suit, player.name, score))
                        if score > 21:
                            print("%s Busts!!!" % (player.name))
                            turn_over = True
                        elif score == 21:
                            print("%s now has 21. Perfect." % (player.name))
                            turn_over = True
                    elif response == "stay" or response == "stand":
                        print("%s is standing at %s." % (player.name, score))
                        turn_over = True
                    time.sleep(1)
                self.next_player()

    def next_player(self):
        if self.current_player+1 == len(self.players):
            self.current_player = 8
        else:
            self.current_player += 1

    def check_bust(self, player):
        if self.debug == True:
            print ("Checking bust... Cards in hand=[%s]" % player.hand)

class Blackjack_Player(Card_Player):
    def __init__(self, name = ""):
        super().__init__(Card_Player)
        self.name = name

def test_1():
    # Just a quick test to get things working
    bj_shoe = Shoe(shoe_size=2)
    # print(bj_shoe.show_shoe())
    dealer = Blackjack_Dealer()
    # print(dir(dealer))
    bj_player = Blackjack_Player(player_name = "Joey")
    # print(dir(bj_player))
    dealer.add_player(bj_player)
    ## WORKS
    dealer.deal_initial_cards()

def test_2():
    # Setup Initial Parameters
    bj_shoe = Shoe(shoe_size=2)

    # Create Game Engine
    dealer = Blackjack_Dealer()

    # Create Players
    joey = Blackjack_Player(name = "Joey")

    # Add Players
    dealer.add_player(joey)

    # GAME LOOP
    dealer.start_blackjack_game()

def test_3():
    # Multiple Players

    # Setup Initial Parameters
    bj_shoe = Shoe(shoe_size=2)

    # Create Game Engine
    dealer = Blackjack_Dealer()

    # Create Players
    joey = Blackjack_Player(name = "Joey")
    jenny = Blackjack_Player(name="Jenny")

    # Add Players
    dealer.add_player(joey)
    dealer.add_player(jenny)

    # GAME LOOP
    dealer.start_blackjack_game()

if __name__ == "__main__":
    test_2()