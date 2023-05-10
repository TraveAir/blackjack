"""
Created on Tue May 9, 2023

@author: Travis Michels
"""
import random
import time

NUM_DECKS = 1
SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
NAMES = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]


class Card:
    def __init__(self, name, suit, value):
        self.name = name
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.name} of {self.suit} with value {self.value}"


class Shoe:
    def __init__(self):
        self.cards = []
        self.build()
        self.shuffle()

    def build(self):
        for _ in range(NUM_DECKS):
            for suit in SUITS:
                for index, name in enumerate(NAMES, start=1):
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
    cards = []
    bet_amount = 0


class Player:
    balance = 0
    hands = []


shoe = Shoe()
shoe.shuffle()
shoe.display()
shoe.clear()
shoe.deal()
