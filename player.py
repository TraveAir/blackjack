STARTING_BALANCE = 500

from hand import Hand


class Player:
    def __init__(self, dealer=False):
        # List of hands, starts with one hand
        self.hands = [Hand()]
        self.balance = STARTING_BALANCE
        # Win streak counter
        self.streak = 0
        # Name of player displayed on screen
        self.name = "PLAYER"
        if dealer:
            self.name = "DEALER"

    def display_balance(self):
        return f"${self.balance}"

    # Display all hands for player, hides HAND # if only one hand
    def display_hands(self, total=False):
        print(f"\n{self.name}: ")
        for index, hand in enumerate(self.hands):
            if len(self.hands) > 1:
                print(f"\tHAND {index+1}:")
            hand.display()
            if total:
                print(f"\tTotal: {hand.total()}\n")
