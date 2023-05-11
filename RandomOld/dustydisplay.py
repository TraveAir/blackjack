Spades = "Spades"
Hearts = "Hearts"
Diamonds = "Diamonds"
Clubs = "Clubs"


class Card:
    def __init__(self, name, value, suit) -> None:
        self.name = name
        self.value = value
        self.suit = suit

    def __repr__(self) -> str:
        symbol_map = {"Clubs": "♣", "Diamonds": "♦", "Hearts": "♥", "Spades": "♠"}
        symbol = symbol_map[self.suit]
        return (
            "\n"
            + "+------+\n"
            + "|{0:>6}|\n".format(symbol)
            + "|{0:^6}|\n".format(self.name)
            + "|      |\n"
            + "|{0:<6}|\n".format(symbol)
            + "+------+\n"
        )


hand = [
    Card("Ace", 1, Spades),
    Card("King", 10, Hearts),
    Card("4", 4, Diamonds),
    Card("9", 9, Spades),
]


[print(x, end="") for x in hand]
