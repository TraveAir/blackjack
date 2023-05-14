import game_util
from card import Card

# Minimum bet amount
MIN_BET = 10


class Hand:
    """Represents a single blackjack hand"""

    def __init__(self):
        # Cards in hand
        self.cards = []
        # Bet amount for hand
        self.bet_amount = 0
        # Flags for hand status
        self.busted = False
        self.turn_over = False
        self.blackjack = False
        self.insured = False
        # Flags for allowed actions
        self.allow_hit = True
        self.allow_stay = True
        self.allow_split = False
        self.allow_double = False
        self.outcome = {"message": "", "bal_change": 0}

    def __repr__(self) -> str:
        ret = ""
        for card in self.cards:
            ret += f"{card}"
        return ret

    def display(self, use_color=True):
        """Print to std out all cards in hand via ASCII art"""
        cards = [x for x in self.cards]  # copy to ensure original list is not modified
        game_util.display_hand(cards, use_color=use_color)

    # Method to get total value of hand
    def total(self) -> int:
        total = 0
        num_aces = 0
        for card in self.cards:
            total += card.value
            if card.name == "Ace":
                num_aces += 1
        # Check if aces should be 1 or 11
        for _ in range(num_aces):
            if total + 10 <= 21:
                total += 10
        return total

    # Method to check if hand is busted and set flags
    def bust_check(self):
        if self.total() > 21:
            self.busted = True
            self.turn_over = True

    # Method to update allowed action flags
    def update_options(self, player):
        self.allow_double = False
        self.allow_split = False

        if (len(self.cards) == 2) and (self.bet_amount <= player.balance):
            # Check if aces were split and new card is ace
            if (len(player.hands) > 1) and (
                self.cards[0].value == 1 and self.cards[1].value == 1
            ):
                self.allow_double = False
            else:
                self.allow_double = True
            if len(player.hands) < 4:
                self.allow_split = self.cards[0].value == self.cards[1].value

    # Method to get player action and return action number
    def get_action(self) -> str:
        s = ""
        allowed = []
        if self.allow_hit:
            allowed.append("1")
            s = f"{s}1) Hit\n"
        if self.allow_stay:
            allowed.append("2")
            s = f"{s}2) Stay\n"
        if self.allow_double:
            allowed.append("3")
            s = f"{s}3) Double\n"
        if self.allow_split:
            allowed.append("4")
            s = f"{s}4) Split\n"

        print(s)

        while True:  # Loop until valid action is chosen
            act = input("Choose an action: ")
            if act in allowed or act == "help":
                return act
            else:
                print("Invalid action!")
