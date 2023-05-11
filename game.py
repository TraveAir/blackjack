"""
Created on Tue May 9, 2023

@author: Travis Michels
"""
import random
import time
import os

NUM_DECKS = 6

STARTING_BALANCE = 100

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
        self.allow_split = False
        self.allow_double = False

    def __repr__(self) -> str:
        ret = ""
        for card in self.cards:
            ret += f"{card}"
        return ret

    def display(self):
        if self.cards[-1].hidden:
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

        if self.cards[-1].name == "?":
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

    def bust_check(self):
        if self.total() > 21:
            self.busted = True
            self.turn_over = True

    def update_options(self):
        self.allow_double = False
        self.allow_split = False
        if (len(self.cards) == 2) and (self.bet_amount <= player.balance):
            self.allow_double = True
            if len(player.hands) <= 4:
                self.allow_split = self.cards[0].value == self.cards[1].value

    def get_action(self) -> str:
        s = ""
        allowed = ["1", "2"]
        if self.allow_double:
            allowed.append("3")
        if self.allow_split:
            allowed.append("4")

        for x in range(len(allowed)):
            if x == 0:
                s = f"{s}1) Hit\n"
            elif x == 1:
                s = f"{s}2) Stay\n"
            elif x == 2:
                s = f"{s}3) Double\n"
            elif x == 3:
                s = f"{s}4) Split\n"
        print(s)

        while True:
            act = input("Choose an action: ")
            if act in allowed:
                return act
            else:
                print("Invalid action!")


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
    clear_screen()
    print(f"Balance: {player.balance}")
    dealer.display_hands(total)
    player.display_hands(total)


def clear_screen():
    os.system("cls")


def check_blackjacks():
    if (player.hands[0].total() == 21) or (dealer.hands[0].total() == 21):
        dealer.hands[0].cards[1].hidden = False
        dealer.hands[0].turn_over = True
        player.hands[0].turn_over = True
        if player.hands[0].total() == 21:
            player.hands[0].blackjack = True
        if dealer.hands[0].total() == 21:
            dealer.hands[0].blackjack = True


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
    clear_screen()
    print(f"WIN STREAK: {player.streak}\n")
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
        # Give card to hand if split
        if len(hand.cards) == 1:
            hand.cards.append(shoe.deal())
            if hand.total() == 21:
                hand.turn_over = True
        # check if player is allowed to make any moves
        while not hand.turn_over:
            # Print all hands
            display_all_hands()

            # Refresh possible actions
            hand.update_options()

            # Get player action
            action = hand.get_action()

            # Perform player action
            if action == "1":  # Hit
                hand.cards.append(shoe.deal())
                hand.bust_check()
            elif action == "2":  # Stand
                hand.turn_over = True
            elif action == "3":  # Double
                # Remove extra bet from balance
                player.balance -= hand.bet_amount
                # Double hand bet
                hand.bet_amount *= 2
                # Deal one card
                hand.cards.append(shoe.deal())
                # End turn
                hand.turn_over = True
            elif action == "4":  # Split
                # Create new hand
                player.hands.append(Hand())
                # Remove extra bet from balance
                player.balance -= hand.bet_amount
                # Add bet to new hand
                player.hands[-1].bet_amount = hand.bet_amount
                # Move second card to new hand
                player.hands[-1].cards.append(hand.cards.pop(1))
                # Deal one card to hand
                hand.cards.append(shoe.deal())

            # Check for bust
            hand.bust_check()

            # check for hand total of 21 and end turn if so
            if hand.total() == 21:
                hand.turn_over = True


def dealer_turn():
    # Check if dealer turn is necessary
    if all(hand.busted for hand in player.hands):
        dealer.hands[0].turn_over = True

    while not dealer.hands[0].turn_over:
        display_all_hands()
        # Check if dealer has to hit
        if dealer.hands[0].total() < 17:
            time.sleep(1)
            dealer.hands[0].cards.append(shoe.deal())
        else:
            # Dealer has to stand and turn is over
            dealer.hands[0].turn_over = True
        # Check for bust
        dealer.hands[0].bust_check()


def determine_outcome():
    display_all_hands(True)
    for hand in player.hands:
        if len(player.hands) == 1:
            s = ""
        else:
            s = f"Hand {player.hands.index(hand) + 1}: "

        if (hand.blackjack) and (not dealer.hands[0].blackjack):
            print(f"{s}BLACKJACK!")
            player.balance += hand.bet_amount
            player.balance += int(hand.bet_amount * 1.5)
        elif (dealer.hands[0].blackjack) and (not hand.blackjack):
            print(f"{s}LOSE! Dealer has blackjack!")
        elif hand.busted:
            print(f"{s}BUSTED! :(")
        elif dealer.hands[0].busted:
            print(f"{s}WIN! Dealer busted!")
            player.balance += hand.bet_amount * 2
        elif hand.total() > dealer.hands[0].total():
            print(f"{s}WIN! You beat the dealer!")
            player.balance += hand.bet_amount * 2
        elif hand.total() < dealer.hands[0].total():
            print(f"{s}LOSE! Dealer beat you!")
        else:
            print(f"{s}PUSH! You tied the dealer!")
            player.balance += hand.bet_amount
    input("\n\nPress Enter to continue...")


def reset_game():
    player.hands.clear()
    player.hands.append(Hand())
    dealer.hands.clear()
    dealer.hands.append(Hand())


def game_loop():
    # Start game, deal initial cards
    start_new_game()

    # Check for blackjacks
    check_blackjacks()

    # ---- Player's turn ----

    # Get bet amount
    get_bet_amount()

    # Give player turn
    player_turn()
    while not all(len(hand.cards) >= 2 for hand in player.hands):
        player_turn()

    # ---- Dealer's turn ----
    dealer.hands[0].cards[1].hidden = False
    dealer_turn()

    # ---- End of game ----
    determine_outcome()
    reset_game()


def enter_game():
    # Enter game loop while player has money
    while player.balance > MIN_BET:
        tmpbal = player.balance
        game_loop()
        # Update win streak
        if player.balance > tmpbal:
            player.streak += 1
        elif player.balance < tmpbal:
            player.streak = 0


# Create player and dealer
player = Player()
dealer = Player(True)

# Create shoe
shoe = Shoe()


enter_game()
while True:
    clear_screen()
    print("You ran out of money!")
    if input("Would you like to rebuy? (y/n): ") == "y":
        player.balance = STARTING_BALANCE
        player.streak = 0
        enter_game()
    else:
        break
