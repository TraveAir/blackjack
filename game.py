"""
Created on Tue May 9, 2023

@author: Travis Michels
"""
import time
import os

from shoe import Shoe
from hand import Hand
from player import Player, STARTING_BALANCE
from card import Card

# Minimum bet amount
MIN_BET = 5


# Display all hands for player and dealer with names
def display_all_hands(show_total=False):
    clear_screen()
    print(f"Balance: {player.balance}")
    dealer.display_hands(show_total)
    player.display_hands(show_total)


def clear_screen():
    """Clears terminal window, typically called before cards are displayed"""
    if os.name == "nt":  # windows
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")


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
    for _ in range(2):
        player.hands[0].cards.append(shoe.deal())
        dealer.hands[0].cards.append(shoe.deal())

    # Hide dealer's second card
    dealer.hands[0].cards[1].hidden = True


def get_bet_amount():
    """Prompts user for a bet amount and stores it in hand object"""
    clear_screen()
    print(f"WIN STREAK: {player.streak}\n")
    print(f"Balance: {player.balance}")
    while True:  # Loop until valid bet amount is entered
        inp = input("Enter bet amount: ")
        if inp == "":
            player.hands[0].bet_amount = MIN_BET
            break
        try:
            player.hands[0].bet_amount = int(inp)
            if player.hands[0].bet_amount > player.balance:
                raise ValueError("You don't have enough money!")
            if player.hands[0].bet_amount < MIN_BET:
                raise ValueError(f"Minimum bet is {MIN_BET}!")
            break
        except ValueError as e:  # Error handling for invalid bet amount
            if str(e).startswith("invalid literal"):
                e = "Please enter a valid number!"
            print(f"Invalid bet amount: {e}")
    player.balance -= player.hands[0].bet_amount


# Function to handle player's turn
def player_turn():
    for hand in player.hands:
        while not hand.turn_over:
            # Give card to hand if split
            if len(hand.cards) == 1:
                hand.cards.append(shoe.deal())
                if hand.total() == 21:
                    break
                # Check if aces were split
                if hand.cards[0].value == 1:
                    # Check if new card is ace
                    if hand.cards[1].value == 1:
                        hand.allow_hit = False
                    else:
                        break
            # Print all hands
            display_all_hands()

            # Refresh possible actions
            hand.update_options(player)

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


def determine_outcomes():
    # Hide hand number if only one hand
    for hand in player.hands:
        if len(player.hands) == 1:
            s = ""
        else:
            s = f"Hand {player.hands.index(hand) + 1}: "

        # Check for player BJ win
        if (hand.blackjack) and (not dealer.hands[0].blackjack):
            hand.outcome["message"] = f"{s}BLACKJACK!"
            hand.outcome["bal_change"] += hand.bet_amount  # Return bet
            hand.outcome["bal_change"] += int(hand.bet_amount * 1.5)  # Pay 3:2
        # Check for dealer BJ loss
        elif (dealer.hands[0].blackjack) and (not hand.blackjack):
            hand.outcome["message"] = f"{s}LOSE! Dealer has blackjack!"
        # Check for player bust loss
        elif hand.busted:
            hand.outcome["message"] = f"{s}BUSTED! :("
        # Check for dealer bust win
        elif dealer.hands[0].busted:
            hand.outcome["message"] = f"{s}WIN! Dealer busted!"
            hand.outcome["bal_change"] += hand.bet_amount * 2
        # Check for player win by being closer to 21
        elif hand.total() > dealer.hands[0].total():
            hand.outcome["message"] = f"{s}WIN! You beat the dealer!"
            hand.outcome["bal_change"] += hand.bet_amount * 2
        # Check for dealer win by being closer to 21
        elif hand.total() < dealer.hands[0].total():
            hand.outcome["message"] = f"{s}LOSE! Dealer beat you!"
        # Result is a push
        else:
            hand.outcome["message"] = f"{s}PUSH! You tied the dealer!"
            hand.outcome["bal_change"] += hand.bet_amount


def update_balance():
    for hand in player.hands:
        player.balance += hand.outcome["bal_change"]


def display_outcomes():
    for hand in player.hands:
        print(hand.outcome["message"])


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
    determine_outcomes()
    update_balance()
    display_all_hands(show_total=True)
    display_outcomes()
    input("\n\nPress enter to continue...")
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
