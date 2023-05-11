class Card:
    def __init__(self, name, value, suit) -> None:
        self.name = name
        self.value = value
        self.suit = suit

    def fancy_print():
        pass


class Deck:
    cards: list[Card] = []

    def build_deck(self):
        c = Card("Ace", 1, "Spades")
        self.cards.append(c)

    def shuffle(self):
        pass

    def deal(self):
        self.cards.pop()


class Game:
    def start_game(self):
        self.players = [CardPlayer("Player 1", False), CardPlayer("Dealer", True)]
        self.deck.build_deck()
        self.deck.shuffle()
        self.deck.deal()


class CardPlayer:
    is_dealer = False
    win_streak = 0
    balance = 0
    bet = 0
    hand = []
    hand_value = 0

    def __init__(self, name, is_dealer) -> None:
        self.name = name
        self.is_dealer = is_dealer

    def get_possible_actions(self) -> list[str]:
        options = ["hit", "stand"]
        if self.balance > self.bet * 2:
            options.append("double")
        if len(self.hand) == 2 and self.hand[0].value == self.hand[1].value:
            options.append("split")
        return options

    def player_turn(self):
        self.bet = self.bet * 2


def main():
    player1 = CardPlayer("Player 1", False)
    player2 = CardPlayer("Dealer", True)

    if player2.is_dealer:
        print("Dealer is dealing...")
