"""
Created on Tue May 9, 2023

@author: Travis Michels
"""
import random
import time
import os

# Number of decks in shoe
NUM_DECKS = 6

# Starting balance for player
STARTING_BALANCE = 100

# Minimum bet amount
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


# Class for individual cards
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


# Class for shoe of cards
class Shoe:
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

    # Method to shuffle shoe
    def shuffle(self):
        random.shuffle(self.cards)

    # Method to display shoe for debugging
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
        return shoe.cards.pop(0)

    # Method to clear all cards in shoe
    def clear(self):
        self.cards.clear()


# Class for a single playable hand
class Hand:
    def __init__(self):
        # Cards in hand
        self.cards = []
        # Bet amount for hand
        self.bet_amount = 0
        # Flags for hand status
        self.busted = False
        self.turn_over = False
        self.blackjack = False
        # Flags for allowed actions
        self.allow_split = False
        self.allow_double = False

    def __repr__(self) -> str:
        ret = ""
        for card in self.cards:
            ret += f"{card}"
        return ret

    # Method display all cards in hand via ASCII art
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
    def update_options(self):
        self.allow_double = False
        self.allow_split = False
        if (len(self.cards) == 2) and (self.bet_amount <= player.balance):
            self.allow_double = True
            if len(player.hands) <= 4:
                self.allow_split = self.cards[0].value == self.cards[1].value

    # Method to get player action and return action number
    def get_action(self) -> str:
        s = ""
        allowed = ["1", "2"]  # Hit, Stand are always allowed
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

        while True:  # Loop until valid action is chosen
            act = input("Choose an action: ")
            if act in allowed:
                return act
            else:
                print("Invalid action!")


# Class for player and dealer
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

    # Method to display all hands for player, hides HAND # if only one hand
    def display_hands(self, total=False):
        print(f"{self.name}: ")
        for index, hand in enumerate(self.hands):
            if len(self.hands) > 1:
                print(f"\tHAND {index+1}:")
            hand.display()
            if total:
                print(f"\tTotal: {hand.total()}\n")


# Function to display all hands for player and dealer with names
def display_all_hands(total=False):
    clear_screen()
    print(f"Balance: {player.balance}")
    dealer.display_hands(total)
    player.display_hands(total)


# Function to clear screen
def clear_screen():
    os.system("cls")


# Function to check for blackjacks and set flags
def check_blackjacks():
    if (player.hands[0].total() == 21) or (dealer.hands[0].total() == 21):
        # Applicable if either player or dealer has blackjack
        dealer.hands[0].cards[1].hidden = False
        dealer.hands[0].turn_over = True
        player.hands[0].turn_over = True
        # Specific to player or dealer blackjack
        if player.hands[0].total() == 21:
            player.hands[0].blackjack = True
        if dealer.hands[0].total() == 21:
            dealer.hands[0].blackjack = True


# Function to create a new game, clear cards and re-deal
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


# Function to get bet amount from player before their first turn
def get_bet_amount():
    clear_screen()
    print(f"WIN STREAK: {player.streak}\n")
    print(f"Balance: {player.balance}")
    while True:  # Loop until valid bet amount is entered
        try:
            player.hands[0].bet_amount = int(input("Enter bet amount: "))
            if player.hands[0].bet_amount > player.balance:
                raise ValueError("You don't have enough money!")
            if player.hands[0].bet_amount < MIN_BET:
                raise ValueError(f"Minimum bet is {MIN_BET}!")
            break
        except ValueError as e:  # Exception handling for invalid bet amount
            if str(e).startswith("invalid literal"):
                e = "Please enter a valid number!"
            print(f"Invalid bet amount: {e}")
    player.balance -= player.hands[0].bet_amount


# Function to handle player's turn
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


# Function to handle dealer's turn
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


# Function to determine outcome of game
def determine_outcome():
    display_all_hands(True)  # Display all hands with totals

    # Hide hand number if only one hand
    for hand in player.hands:
        if len(player.hands) == 1:
            s = ""
        else:
            s = f"Hand {player.hands.index(hand) + 1}: "

        # Check for player BJ win
        if (hand.blackjack) and (not dealer.hands[0].blackjack):
            print(f"{s}BLACKJACK!")
            player.balance += hand.bet_amount  # Return bet
            player.balance += int(hand.bet_amount * 1.5)  # Pay 3:2
        # Check for dealer BJ loss
        elif (dealer.hands[0].blackjack) and (not hand.blackjack):
            print(f"{s}LOSE! Dealer has blackjack!")
        # Check for player bust loss
        elif hand.busted:
            print(f"{s}BUSTED! :(")
        # Check for dealer bust win
        elif dealer.hands[0].busted:
            print(f"{s}WIN! Dealer busted!")
            player.balance += hand.bet_amount * 2
        # Check for player win by being closer to 21
        elif hand.total() > dealer.hands[0].total():
            print(f"{s}WIN! You beat the dealer!")
            player.balance += hand.bet_amount * 2
        # Check for dealer win by being closer to 21
        elif hand.total() < dealer.hands[0].total():
            print(f"{s}LOSE! Dealer beat you!")
        # Result is a push
        else:
            print(f"{s}PUSH! You tied the dealer!")
            player.balance += hand.bet_amount
    input("\n\nPress Enter to continue...")


# Function to reset game state (clear cards, etc.), does not reset balance
def reset_game():
    player.hands.clear()
    player.hands.append(Hand())
    dealer.hands.clear()
    dealer.hands.append(Hand())


# Main game loop
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
    # Keep looping if player split until all hands are played
    while not all(len(hand.cards) >= 2 for hand in player.hands):
        player_turn()

    # ---- Dealer's turn ----
    dealer.hands[0].cards[1].hidden = False
    dealer_turn()

    # ---- End of game ----
    determine_outcome()
    reset_game()


# Enter game loop after after each game until player runs out of money
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


# ---- Main ----
# Create player and dealer
player = Player()
dealer = Player(True)

# Create shoe
shoe = Shoe()

# Enter game loop and rebuy if player runs out of money
enter_game()
while True:
    clear_screen()
    print("You ran out of money!")
    if input("Would you like to rebuy? (y/n): ") == "y":
        player.balance = STARTING_BALANCE
        player.streak = 0
        enter_game()
    else:  # Exit game if player doesn't want to rebuy
        break
