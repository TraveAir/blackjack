"""
Created on Tue May 9, 2023

@author: Travis Michels
"""
import random
import time
import os

NUM_DECKS = 6

STARTING_BALANCE = 1000

MIN_BET = 5

CARD_SUITS = ["♥", "♦", "♣", "♠"]
CARD_NAMES = [
    "Ace",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "Jack",
    "Queen",
    "King",
]


class Card:
    def __init__(self, name, suit, value):
        self.name = name
        self.suit = suit
        self.value = value
        self.hidden = False

    def __repr__(self):
        return f"[{self.name} of {self.suit}] "


class Shoe:
    def __init__(self):
        self.cards = []
        self.build()
        self.shuffle()

    def build(self):
        for _ in range(NUM_DECKS):
            for suit in CARD_SUITS:
                for index, name in enumerate(CARD_NAMES, start=1):
                    value = index
                    if name in ["Jack", "Queen", "King"]:
                        value = 10
                    card = Card(name, suit, value)
                    self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def display(self):
        for card in self.cards:
            print(card)

    def size(self) -> int:
        return len(self.cards)

    def deal(self) -> Card:
        if not self.cards:
            raise ValueError("No cards left in shoe")
        return shoe.cards.pop(0)

    def clear(self):
        self.cards.clear()


class Hand:
    def __init__(self):
        self.cards = []
        self.bet_amount = 0
        self.busted = False
        self.turn_over = False
        self.blackjack = False

    def __repr__(self) -> str:
        ret = ""
        for card in self.cards:
            ret += f"{card}"
        return ret

    def display(self):
        if self.cards[1].hidden:
            tmpcard = self.cards.pop(1)
            self.cards.append(Card("?", "?", 0))
        card_size = 9
        hline = ""
        vline = "|"
        vspacer = ""
        hspacer = ""
        s = ""

        for _ in range(card_size):
            hline = f"{hline}-"
            vline = f"{vline} "
        vline = f"{vline}|"

        for card in self.cards:
            vspacer = f"{vspacer}\t{vline}"
            hspacer = f"{hspacer}\t {hline}"

        print(hspacer)
        print(vspacer)

        for card in self.cards:
            if card.name == "10":
                s = f"{s}\t{vline[:2]}{card.name}{vline[4:]}"
            else:
                s = f"{s}\t{vline[:2]}{card.name[0]}{vline[3:]}"
        print(s)
        s = ""

        print(vspacer)

        for card in self.cards:
            index = len(vline) // 2
            s = f"{s}\t{vline[:index]}{card.suit}{vline[index+1:]}"
        print(s)
        s = ""

        print(vspacer)

        for card in self.cards:
            index = len(vline) - 3
            if card.name == "10":
                s = f"{s}\t{vline[:index-1]}{card.name}{vline[index+1:]}"
            else:
                s = f"{s}\t{vline[:index]}{card.name[0]}{vline[index+1:]}"
        print(s)
        s = ""

        print(vspacer)
        print(hspacer)

        if self.cards[1].name == "?":
            self.cards[1] = tmpcard

    def total(self) -> int:
        total = 0
        num_aces = 0
        for card in self.cards:
            total += card.value
            if card.name == "Ace":
                num_aces += 1
        for _ in range(num_aces):
            if total + 10 <= 21:
                total += 10
        return total

    def blackjack_check(self) -> bool:
        if self.total() == 21:
            return True
        return False


class Player:
    def __init__(self, dealer=False):
        self.hands = [Hand()]
        self.balance = STARTING_BALANCE
        self.streak = 0
        self.name = "PLAYER"
        if dealer:
            self.name = "DEALER"

    def display_hands(self, total=False):
        print(f"{self.name}: ")
        for index, hand in enumerate(self.hands):
            if len(self.hands) > 1:
                print(f"\tHAND {index+1}:")
            hand.display()
            if total:
                print(f"\tTotal: {hand.total()}\n")


def display_all_hands(total=False):
    os.system("cls")
    player.display_hands(total)
    dealer.display_hands(total)


def check_blackjack(person):
    if person.hands[0].blackjack_check():
        person.hands[0].blackjack = True
        person.hands[0].cards[1].hidden = False
        dealer.hand[0].turn_over = True
        player.hand[0].turn_over = True


def start_new_game():
    # Check Shoe size and rebuild if necessary
    if shoe.size() < 40:
        shoe.clear()
        shoe.build()
        shoe.shuffle()

    # Deal initial cards
    player.hands[0].cards.append(shoe.deal())
    dealer.hands[0].cards.append(shoe.deal())
    player.hands[0].cards.append(shoe.deal())
    dealer.hands[0].cards.append(shoe.deal())
    # Hide dealer's second card
    dealer.hands[0].cards[1].hidden = True


def get_bet_amount():
    print(f"Balance: {player.balance}")
    while True:
        try:
            player.hands[0].bet_amount = int(input("Enter bet amount: "))
            if player.hands[0].bet_amount > player.balance:
                raise ValueError("You don't have enough money!")
            if player.hands[0].bet_amount < MIN_BET:
                raise ValueError(f"Minimum bet is {MIN_BET}!")
            break
        except ValueError as e:
            if str(e).startswith("invalid literal"):
                e = "Please enter a valid number!"
            print(f"Invalid bet amount: {e}")
    player.balance -= player.hands[0].bet_amount


def player_turn():
    for hand in player.hands:
        while not hand.turn_over:

# Start of game

# Create player and dealer
player = Player()
dealer = Player(True)

# Create shoe
shoe = Shoe()

# Start game, deal initial cards
start_new_game()

# Check for blackjacks
check_blackjack(player)
check_blackjack(dealer)

# ---- Player's turn ----

# Get bet amount
get_bet_amount()
print(f"Bet amount is: {player.hands[0].bet_amount}")
get_bet_amount()
print(f"Bet amount is: {player.hands[0].bet_amount}")

# Give player turn
player_turn()