"""
Rewritten by Jordan Vo for use in his Roleplay Discord Bot
"""

import random

from collections import defaultdict, OrderedDict

ROYAL_FLUSH = ["AS", "JS", "QS", "KS", "TS"]

CARD_ORDER_DICT = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "T":10,"J":11, "Q":12, "K":13, "A":14}

CARD_VALUE_NAMES = {
    "A" : "Ace",
    "2" : "Two",
    "3" : "Three",
    "4" : "Four",
    "5" : "Five",
    "6" : "Six",
    "7" : "Seven",
    "8" : "Eight",
    "9" : "Nine",
    "T": "Ten",
    "J" : "Jack",
    "Q" : "Queen",
    "K" : "King"
}

CARD_SUIT_NAMES = {
    "D" : "Diamonds",
    "C" : "Clubs",
    "H" : "Hearts",
    "S" : "Spades"
}

HAND_RANKINGS = {
    10  :   "Royal Flush",
    9   :   "Straight Flush",
    8   :   "Four of a Kind",
    7   :   "Full House",
    6   :   "Flush",
    5   :   "Straight",
    4   :   "Three of a Kind",
    3   :   "Two Pair",
    2   :   "One Pair",
    1   :   "High Card"
}

# def compare(card_1,card_2):
#     if card_1.value > card_2.value:
#         return card_1
#     elif card_2.value > card_1.value:
#         return card_2
#     else:
#         if card_1.


class Card(object):
    def __init__(self, name):
        self.name = name
        self.value = int(name[0])
        self.suit = name[1]

class Deck(object):
    def __init__(self, new_deck_order = True):
        self.cards = []
        self.make_the_deck()
        if new_deck_order == True:
            self.new_deck_order()
        elif new_deck_order == False:
            for shuffles in range(7):
                self.shuffle()

    def __str__(self):
        return self.get_deck()

    def make_the_deck(self):
        _str = ""
        for suit in CARD_SUIT_NAMES.keys():
            for card in CARD_VALUE_NAMES.keys():
                _str = card+suit
                self.cards.append(_str)

    def new_deck_order(self):
        """" Assumes the deck starts in this order:
        ['AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD',
         'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC',
         'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH',
         'AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS']"""
        diamonds = self.cards[0:13]
        clubs = self.cards[13:26]
        hearts = self.cards[26:39]
        hearts.reverse()
        spades = self.cards[39:52]
        spades.reverse()
        self.cards = diamonds+clubs+hearts+spades

    def mirror_stack_deck_order(self):
        """" Assumes the deck starts in this order:
        ['AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD',
         'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC',
         'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH',
         'AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS']"""
        diamonds = self.cards[0:13]
        clubs = self.cards[13:26]
        hearts = self.cards[26:39]
        hearts.reverse()
        spades = self.cards[39:52]
        spades.reverse()
        self.cards = clubs+diamonds+hearts+spades

    def get_deck(self):
        return str(self.cards)

    def shuffle(self, debug=False):
        random.shuffle(self.cards)
        if debug == True:
            print (self.cards)

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

class Card_Player(object):
    def __init__(self, player_name = ""):
        self.player_name = player_name
        self.hand = []

    def add_to_hand(self, card):
        self.hand.append(card)

    def remove_from_hand(self, card):
        self.hand.remove(card)
        return card

    def toss_hand(self):
        cards = self.hand
        self.hand = []
        return cards

    def sort_hand(self):
        self.hand.sort()

    def get_hand(self):
        return str(self.hand)

    def print_hand(self):
        cards = ""
        for card in self.hand:
            value, suit, = card
            _str = ("(%s) %s of %s\n" % (card, CARD_VALUE_NAMES[value], CARD_SUIT_NAMES[suit]))
            cards = cards+_str
        return cards

class Card_Dealer(object):
    def __init__(self):
        """ A class that can handle card games."""
        self.players = []

        self.current_dealer = None  # If none, the first player will be the permanent dealer.
        self.current_player = 0  # The position of the turn player, counting from the dealer.

        self.deck = Deck()
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

    def deal_a_card_to(self, player, debug = False):
        card = self.deck.draw_a_card()

        card_suit = card.strip("A23456789TJQK")
        ## Gets the fancy full name
        card_suit = CARD_SUIT_NAMES[card_suit]

        card_value = card.strip("CHSD")
        card_value = CARD_VALUE_NAMES[card_value]

        player.add_to_hand(card)
        if debug == True:
            print ("%s of %s was dealt to player %s" % (card_value, card_suit, player.player_name))

    def deal_cards(self):
        for card in range(self.hand_size):
            for player in self.players:
                self.deal_a_card_to(player)

    def get_turn_player(self):
        return self.players[self.current_player]

    def next_player(self):
        self.current_player+=1
        if self.current_player >= len(self.players):
            self.current_player = 0

class Poker_Player(Card_Player):
    def __init__(self,name):
        super().__init__(Card_Player)
        self.player_name = name
        self.highest_card = None

    def get_high_card(self):
        """ Gets the highest of the cards of 'non-winning' cards """
        pass

    def check_royal_flush(self):
        if self.check_flush() and self.check_straight():
            for card in self.hand:
                if card in ROYAL_FLUSH:
                    return True
        else:
            return False

    def check_straight_flush(self):
        if self.check_flush() and self.check_straight():
            return True
        else:
            return False

    def count_same_valued_cards(self):
        same_cards = defaultdict(lambda: [])
        for card in self.hand:
            value = card[0]  # Card value is the first element e.g. [K] S
            same_cards[value].append(card)  # Associates the value with the card
        ## Group non zero counts with their list of cards
        count_list = []
        for value in same_cards:
            count_list.append((len(same_cards[value]), same_cards[value]))
        count_list.sort()
        count_list.reverse()
        return count_list

    def count_same_suited_cards(self):
        same_cards = defaultdict(lambda: [])
        for card in self.hand:
            suit = card[1]  # Card value is the first element e.g. [K] S
            same_cards[suit].append(card)  # Associates the value with the card
        ## Group non zero counts with their list of cards
        count_list = []
        for value in same_cards:
            count_list.append((len(same_cards[value]), same_cards[value]))
        count_list.sort()
        count_list.reverse()
        return count_list

    def check_four_of_a_kind(self):
        count_list = self.count_same_valued_cards()
        if count_list[0][0] == 4: ## Four of a kind
            self.highest_card = count_list[-1][1]
            return True
        return False

    def check_full_house(self):
        count_list = self.count_same_valued_cards()
        if count_list[0][0] == 3 and count_list[1][0] == 2:
            self.highest_card = count_list[0][0]
            return True
        return False

    def check_flush(self):
        count_list = self.count_same_suited_cards()
        if count_list[0][0] == 5:
            return True
        else:
            return False

    def check_straight(self):
        values = [i[0] for i in self.hand]
        value_counts = defaultdict(lambda: 0)
        for v in values:
            value_counts[v] += 1
        rank_values = [CARD_ORDER_DICT[i] for i in values]
        value_range = max(rank_values) - min(rank_values)
        if len(set(value_counts.values())) == 1 and (value_range == 4):
            return True
        else:
            # check straight with low Ace
            if set(values) == set(["A", "2", "3", "4", "5"]):
                return True
            return False

    def check_three_of_a_kind(self):
        values = [i[0] for i in self.hand]
        value_counts = defaultdict(lambda: 0)
        for v in values:
            value_counts[v] += 1
        if set(value_counts.values()) == set([3, 1]):
            return True
        else:
            return False

    def check_two_pair(self):
        values = [i[0] for i in self.hand]
        value_counts = defaultdict(lambda: 0)
        for v in values:
            value_counts[v] += 1
        if sorted(value_counts.values()) == [1, 2, 2]:
            return True
        else:
            return False

    def check_one_pair(self):
        values = [i[0] for i in self.hand]
        value_counts = defaultdict(lambda: 0)
        for v in values:
            value_counts[v] += 1
        if 2 in value_counts.values():
            return True
        else:
            return False

    def get_hand_ranking(self):
        """ Gets the highest score of the hand.
        10 = Royal Flush,
        9 = Straight Flush, Etc."""
        if self.check_royal_flush():
            return 10
        if self.check_straight_flush():
            return 9
        if self.check_four_of_a_kind():
            return 8
        if self.check_full_house():
            return 7
        if self.check_flush():
            return 6
        if self.check_straight():
            return 5
        if self.check_three_of_a_kind():
            return 4
        if self.check_two_pair():
            return 3
        if self.check_one_pair():
            return 2
        return 1

class Poker_Card_Dealer(Card_Dealer):
    def __init__(self):
        """ Defaults to standard Poker Rules.
         I made the check hand functions using Brian Caffey's code."""
        super().__init__()
        self.poker_chips = {} ## Usernames associated with the amount of chips that they have.
        self.load_poker_chips() ## Populates the poker chip amounts based off of data/poker_chips.txt
        self.betting_level = 1
        self.MIN_MAX_BET_AMOUNTS = {
            # Max Bet Amounts, rising by level
            1   :   (5, 100),
            2   :   (10, 200),
            3   :   (25, 500),
            4   :   (50, 1000),
            5   :   (100, 2500),
            6   :   (250, 5000),
            7   :   (500, 10000),
            8   :   (1000, 25000),
            9   :   (2500, 100000),
            10  :   (5000, 250000),
            11  :   (10000, 500000), #Five Hundred Thousand
            12  :   (25000, 1000000), #One Million
            13  :   (100000, 2000000), #Two Million
            14  :   (250000, 5000000), #Five Million
            15  :   (500000, 10000000) #Ten Million
        }
        ## Poker Settings
        self.hand_size = 5
        self.turn_count = 0
        self.max_turn_count = 2
        for shuffles in range(7):
            self.shuffle_deck()
        ## Player Settings
        self.betting_players = {}  # A dictionary associating names to bet amounts.

    def trade_cards(self, cards_to_trade, player):
        """ Swaps a string of cards out of the player's hand,
        and replaces them with new cards until they have a full hand again.
        (Determined by the hand size)"""

        _str = cards_to_trade  ## Example "TSKSTC"
        cards = []  ## A list of cards that are seperated
        while _str:
            cards.append(_str[:2])
            _str = _str[2:]
        for card in cards:
            if card in player.hand:
                player.hand.pop(card)
        num_cards = self.hand_size-player.hand
        cards_received = []
        for card in num_cards:
            card = dealer.draw_a_card()
            player.add_to_hand(card)
            cards_received.append(card)
        return cards_received



    def add_bet(self, player, bet_amount):
        if player in self.players:
            self.betting_players[player] = int(bet_amount)

    def save_poker_chips(self):
        _lines = []
        _str = ""
        for player in self.players:
            chips = self.poker_chips[player]
            _str = "%s = %i" % (player, chips)
            _lines.append(_str)
        _lines = "\n".join(_lines)
        filename = "data/poker_chips.txt"
        self.save(filename, _lines)

    def save(self, filename, data):
        filename = filename
        f = open(filename, mode='w+')
        f.write(data)
        f.close()

    def load_poker_chips(self):
        filename = "data/poker_chips.txt"
        poker_chip_file = open(filename, encoding="latin-1").read()
        poker_chip_file = poker_chip_file.split("\n")
        for line in poker_chip_file:
            player, chips = line.split("=")
            player, chips = player.strip(), chips.strip()
            self.poker_chips[player] = int(chips)

    def start_game(self):
        self.game_in_progress = True
        self.deal_cards()

def test_1():  # Just make a deck dagnabbit
    d = Deck()
    print(d.get_deck())

def test_2():  # Test a hand of poker 1v1
    deck = Deck()
    deck.shuffle()
    players = ["joey", "care"]
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
    print("Joey's hand: " + str(joeys_hand))
    print("Care's hand: " + str(cares_hand))
    ## GAME LOOP
    turns = 3

    game_is_running = True
    while game_is_running == True:
        for player in players:
            card_choice = input("It's " + player + "'s turn. Which card do you want to return?")
            if player == "joey":
                if card_choice in joeys_hand:
                    joeys_hand.remove(card_choice)
                    deck.return_card(card_choice)
                    new_card = deck.draw_a_card()
                    joeys_hand.append(new_card)
                    print(player + " drew a " + new_card + ".")
                    print("Joey's hand is now: " + str(joeys_hand))
            elif player == "care":
                if card_choice in cares_hand:
                    cares_hand.remove(card_choice)
                    deck.return_card(card_choice)
                    new_card = deck.draw_a_card()
                    cares_hand.append(new_card)
                    print(player + " drew a " + new_card + ".")
                    print("Care's hand is now: " + str(cares_hand))
            turns -= 1
            if turns == 0:
                game_is_running = False
    print("The game is now over!!!")
    print("Joey's hand: " + str(joeys_hand))
    print("Care's hand: " + str(cares_hand))

def test_3():  # Poker with new Poker Card Dealer object
    dealer = Poker_Card_Dealer()
    joey = Card_Player(player_name="Joey")
    care = Card_Player(player_name="Care")
    dealer.add_player(joey)
    dealer.add_player(care)
    dealer.start_game()
    while dealer.game_in_progress == True:
        turn_player = dealer.get_turn_player()
        print("It's %s's turn to play. (Player %s's cards:%s" % (turn_player.player_name,
                                                                 turn_player.player_name,
                                                                 turn_player.hand))
        break

def test_4():  # Working with Poker Hand Rankings
    d = Deck(new_deck_order=False)
    dealer = Poker_Card_Dealer()
    hand = ["2S","KS","KC","KH","KD"]
    # hand_size = 5
    # for x in range(hand_size):
    #     card = dealer.deck.draw_a_card()
    #     hand.append(card)
    p = Poker_Player("Bob")
    for card in hand:
        p.add_to_hand(card)
    hand_result = HAND_RANKINGS[p.get_hand_ranking()]
    print ("Your hand is: %s. Best Hand: [%s]" % (hand, hand_result))
    print ("High Card: %s" % (p.highest_card))

def test_5(): ## testing print hand functionality
    d = Deck(new_deck_order=False)
    dealer = Poker_Card_Dealer()
    p = Card_Player("Joey")
    hand_size = 5
    for x in range(hand_size):
        card = dealer.deck.draw_a_card()
        p.add_to_hand(card)
    p.print_hand()

def test_6():  # Working with Poker Hand Rankings
    d = Deck(new_deck_order=False)
    dealer = Poker_Card_Dealer()
    players = []
    names = ["ed", "edd", "eddy", "bob", "alan"]
    for name in names:
        p = Poker_Player(name)
        players.append(p)
    hand_size = 5
    for c in range(hand_size):
        for player in players:
            card = dealer.deck.draw_a_card()
            player.add_to_hand(card)

    winner = players[0]
    for player in players[1:]:
        if player.get_hand_ranking() > winner.get_hand_ranking():
            winner = player
        if player.get_hand_ranking() == winner.get_hand_ranking():
            pass

    hand_type = HAND_RANKINGS[winner.get_hand_ranking()]
    print ("Player %s has the best hand with a %s: [%s]" % (winner.player_name,
                                                            hand_type,
                                                            winner.print_hand()))
    for player in players:
        if player != winner:
            print ("Player %s had %s." % (player.player_name, player.print_hand()))

if __name__ == "__main__":
    test_4()
