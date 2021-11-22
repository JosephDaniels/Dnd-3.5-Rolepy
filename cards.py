import random

CARD_VALUES = [
    ("A", "Ace"),
    ("2", "Two"),
    ("3", "Three"),
    ("4", "Four"),
    ("5", "Five"),
    ("6", "Six"),
    ("7", "Seven"),
    ("8", "Eight"),
    ("9", "Nice"),
    ("10", "Ten"),
    ("J", "Jack"),
    ("Q", "Queen"),
    ("K", "King")
]

CARD_SUITS = [
    ("D", "Diamonds"),
    ("C", "Clubs"),
    ("H", "Hearts"),
    ("S", "Spades")
]

class Playing_Cards(object):
    def __init__(self, new_deck_order = True):
        self.cards = []
        self.make_the_deck()
        if new_deck_order == False:
            self.shuffle()

    def make_the_deck(self):
        _str = ""
        for suit, suit_name in CARD_SUITS:
            for card, card_name in CARD_VALUES:
                _str = card+suit
                self.cards.append(_str)

    def get_deck(self):
        return self.cards

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
    card_count = 5
    for player in players:
        for x in range(card_count):
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

if __name__ == "__main__":
    test_2()
