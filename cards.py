import random

CARD_VALUES = {
    "A" : "Ace",
    "2" : "Two",
    "3" : "Three",
    "4" : "Four",
    "5" : "Five",
    "6" : "Six",
    "7" : "Seven",
    "8" : "Eight",
    "9" : "Nine",
    "10": "Ten",
    "J" : "Jack",
    "Q" : "Queen",
    "K" : "King"
}

CARD_SUITS = {
    "D" : "Diamonds",
    "C" : "Clubs",
    "H" : "Hearts",
    "S" : "Spades"
}

class Card_Player(object):
    def __init__(self, player_name = ""):
        self.player_name = player_name
        self.cards_in_hand = []

    def add_to_hand(self, card):
        self.cards_in_hand.append(card)

    def remove_from_hand(self, card):
        self.cards_in_hand.remove(card)
        return card

    def toss_hand(self):
        cards = self.cards_in_hand
        self.cards_in_hand = []
        return cards

    def sort_hand(self):
        self.cards_in_hand.sort()

    def show_hand(self):
        return self.cards_in_hand

class Playing_Cards(object):
    def __init__(self, new_deck_order = True):
        self.cards = []
        self.make_the_deck()
        if new_deck_order == True:
            self.new_deck_order()
        elif new_deck_order == False:
            self.shuffle()

    def __str__(self):
        return self.get_deck()

    def make_the_deck(self):
        _str = ""
        for suit in CARD_SUITS.keys():
            for card in CARD_VALUES.keys():
                _str = card+suit
                self.cards.append(_str)

    def new_deck_order(self):
        pass

    def get_deck(self):
        return str(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_a_card(self):
        """ Pulls a card from the top of the deck. """
        card = ""
        card = self.cards[0]
        self.cards.pop(0) # Remove card from the deck
        return card

    def pick_a_card(self, position = -1):
        """ Pulls a card from a specific position.
         If position is left unspecified,
         it pulls from a random position."""
        card = ""
        if position == -1:  # Default but nonvalid position
            position = random.randint(1,52)
        else:
            pass
        position = position - 1
        try:
            card = self.cards[position]
            self.cards.pop(position)
        except KeyError:
            print ("Wasn't able to pick the random card at %i position." % (position))
        return card

    def return_card(self, card):
        self.cards.append(card)

    def set_new_deck_order(self):
        pass

class Card_Dealer(object):
    def __init__(self):
        """ A class that can handle card games."""
        self.players = []

        self.current_dealer = None  # If none, the first player will be the permanent dealer.
        self.current_player = 0  # The position of the turn player, counting from the dealer.

        self.deck = Playing_Cards()
        self.hand_size = -1  # Override with the hand size of the game you are playing
        self.game_in_progress = False
        self.debug = True

    def shuffle_deck(self):
        self.deck.shuffle()

    def add_player(self, player):
        self.players.append(player)
        if self.debug == True:
            print ("%s was added to the player list." % (player.player_name))

    def remove_player(self, player):
        if player in self.players:
            self.players.remove(player)

    def deal_a_card_to(self,player):
        card = self.deck.draw_a_card()

        card_suit = card.strip("A2345678910JQK")
        card_suit = CARD_SUITS[card_suit]

        card_value = card.strip("CHSD")
        card_value = CARD_VALUES[card_value]

        player.add_to_hand(card)
        print ("%s of %s was dealt to player %s" % (card_value, card_suit, player.player_name))

    def deal_cards(self):
        for card in range(self.hand_size):
            for player in self.players:
                self.deal_a_card_to(player)

    def show_hand(self, player):
        return self.player.cards_in_hand

    def get_turn_player(self):
        return self.players[self.current_player]

    def next_player(self):
        self.current_player+=1
        if self.current_player >= len(self.player):
            self.current_player = 0

class Poker_Card_Dealer(Card_Dealer):
    def __init__(self):
        """ Defaults to standard Poker Rules. """
        super().__init__()

        ## Poker Settings
        self.hand_size = 5

        self.turn_count = 0
        self.max_turn_count = 3

        for shuffles in range(7):
            self.shuffle_deck()

        print (self.deck)

    def start_game(self):
        self.game_in_progress = True
        self.deal_cards()

def test_1():
    d = Playing_Cards()
    d.shuffle()
    print (d.get_deck())
    print (d.pick_a_card(52))

def test_2():  # Test a hand of poker 1v1
    deck = Playing_Cards()
    deck.shuffle()
    players = ["joey","care"]
    joeys_hand = []
    cares_hand = []
    hand_size = 5
    for player in players:
        for x in range(hand_size):
            card = deck.draw_a_card()
            if player == "joey":
                joeys_hand.append(card)
            elif player == "care":
                cares_hand.append(card)

    print ("Joey's hand: "+str(joeys_hand))
    print ("Care's hand: "+str(cares_hand))

    ## GAME LOOP

    turns = 3

    game_is_running = True
    while game_is_running == True:
        for player in players:
            card_choice = input("It's "+player+"'s turn. Which card do you want to return?")
            if player == "joey":
                if card_choice in joeys_hand:
                    joeys_hand.remove(card_choice)
                    deck.return_card(card_choice)
                    new_card = deck.draw_a_card()
                    joeys_hand.append(new_card)
                    print(player + " drew a " + new_card + ".")
                    print("Joey's hand is now: "+str(joeys_hand))
            elif player == "care":
                if card_choice in cares_hand:
                    cares_hand.remove(card_choice)
                    deck.return_card(card_choice)
                    new_card = deck.draw_a_card()
                    cares_hand.append(new_card)
                    print (player+" drew a "+new_card+".")
                    print("Care's hand is now: " + str(cares_hand))
            turns -= 1
            if turns == 0:
                game_is_running = False
    print ("The game is now over!!!")
    print ("Joey's hand: "+str(joeys_hand))
    print ("Care's hand: "+str(cares_hand))

def test_3():
    dealer = Poker_Card_Dealer()
    joey = Card_Player(player_name="Joey")
    care = Card_Player(player_name="Care")
    dealer.add_player(joey)
    dealer.add_player(care)
    dealer.start_game()

if __name__ == "__main__":
    test_3()
