from cards import *

import random

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
    def __init__(self):
        ## The Dealer is always player eight and plays last.
        super().__init__()
        self.players = []
        self.current_player = 0
        self.shoe = Shoe(shoe_size=2)
        self.hand_size = 2
        self.game_in_progress = False
        self.debug = True

    def deal_initial_cards(self):
        for cards in range(self.hand_size):
            for player in self.players:
                card = self.shoe.draw_a_card()
                player.add_to_hand(card)

                card_suit = card.strip("A23456789TJQK")
                ## Gets the fancy full name
                card_suit = CARD_SUIT_NAMES[card_suit]

                card_value = card.strip("CHSD")
                card_value = CARD_VALUE_NAMES[card_value]
                if self.debug == True:
                    print ("%s of %s was dealt to player %s." % (card_value, card_suit, player.player_name))
                    if len(player.hand) == 2:
                        total = 0
                        for card in player.hand:
                            value = card.strip("CHSD")
                            if value in ["T","J","Q","K"]:
                                value = 10
                            if value == "A":
                                value = 11
                            total+=int(value)
                        print ("They have %s and %s in their hand for a total of %i." % (player.hand[0], player.hand[1], total))

    def check_bust(self, player):
        if self.debug == True:
            print ("Checking bust... Cards in hand=[%s]" % player.hand)

class Blackjack_Player(Card_Player):
    def __init__(self, player_name = ""):
        super().__init__(Card_Player)
        self.player_name = player_name

def test_1():
    # Just a quick test to get things working
    bj_shoe = Shoe(shoe_size=2)
    # print(bj_shoe.show_shoe())
    dealer = Blackjack_Dealer()
    # print(dir(dealer))
    bj_player = Blackjack_Player(player_name = "Joey")
    # print(dir(bj_player))
    dealer.add_player(bj_player)

    ## CURRENT DEBUGGING THIS
    dealer.deal_initial_cards()

if __name__ == "__main__":
    test_1()