"""
Created on Tue May 9, 2023

@author: Travis Michels
"""
import random
import time

NUM_DECKS = 6

STARTING_BALANCE = 1000

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
        return shoe.cards.pop()

    def clear(self):
        self.cards.clear()


class Hand:
    def __init__(self):
        self.cards = []
        self.bet_amount = 0
        self.busted = False

    def __repr__(self) -> str:
        ret = ""
        for card in self.cards:
            ret += f"{card}"
        return ret

    def display(self):
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


class Player:
    def __init__(self):
        self.hands = [Hand()]
        self.balance = STARTING_BALANCE
        self.streak = 0


shoe = Shoe()
player = Player()
player.hands[0].cards.append(shoe.deal())
player.hands[0].cards.append(shoe.deal())
player.hands[0].cards.append(shoe.deal())

player.hands[0].display()
