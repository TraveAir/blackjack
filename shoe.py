NUM_DECKS = 6

import random
from card import Card, CARD_SUITS, CARD_NAMES


class Shoe:
    """Holds and deals cards used in the game"""

    def __init__(self):
        self.cards = []
        self.build()
        self.shuffle()

    # Build shoe with NUM_DECKS decks of cards
    def build(self):
        for _ in range(NUM_DECKS):
            for suit in CARD_SUITS:
                for index, name in enumerate(CARD_NAMES, start=1):
                    value = index
                    if name in ["Jack", "Queen", "King"]:
                        value = 10
                    card = Card(name, suit, value)
                    self.cards.append(card)
        for _ in range(200):
            self.cards.append(Card("Ace", "♥", 1))

    def shuffle(self):
        random.shuffle(self.cards)

    # Display shoe for debugging
    def display(self):
        for card in self.cards:
            print(card)

    # Method to get size of shoe
    def size(self) -> int:
        return len(self.cards)

    # Method to deal first card in shoe
    def deal(self) -> Card:
        # Checks for empty shoe (shouldn't happen)
        if not self.cards:
            raise ValueError("No cards left in shoe")
        return self.cards.pop(0)

    # Method to clear all cards in shoe
    def clear(self):
        self.cards.clear()
