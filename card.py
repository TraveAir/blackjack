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
        # Card name, printed on screen
        self.name = name
        # Card suit
        self.suit = suit
        # Card value, 10 for face cards
        self.value = value
        # Hidden flag for dealer's second card
        self.hidden = False

    def __repr__(self):
        return f"[{self.name} of {self.suit}] "
