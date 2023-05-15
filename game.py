"""
Created on Tue May 9, 2023

@author: Travis Michels
"""
import time
import os

from shoe import Shoe
from hand import Hand, MIN_BET
from player import Player
from logger import Logger
from bot import Bot

""" CHANGE BETWEEN HUMAN AND BOT PLAYER HERE
    True: human player
    False: bot player"""
HUMAN_PLAYER = False


# Display all hands for player and dealer with names
def display_all_hands(show_total=False):
    if (not HUMAN_PLAYER) and (bot.speed == 0):
        return
    clear_screen()
    if (not HUMAN_PLAYER) and (bot.speed > 0):
        print(f"Playing Hand {logger.hand_number} OF {bot.max_hands}\n")

    total_bet_amount = 0
    for hand in player.hands:
        total_bet_amount += hand.bet_amount

    if dealer.hands[0].turn_over:
        # Game over, display updated balance
        win_loss_amount = 0
        for hand in player.hands:
            win_loss_amount += hand.outcome["bal_change"]
            if win_loss_amount == 0:
                print(f"You Lost ${total_bet_amount}! | ", end="")
            elif (win_loss_amount - total_bet_amount) == 0:
                print(f"Push! | ", end="")
            else:
                print(f"You Won ${win_loss_amount - total_bet_amount}! | ", end="")
        print(f"New Balance: {player.display_balance()}")
    else:
        # Game still going, display bet amount and remaining balance
        str = "Bet Amount"
        if len(player.hands) > 1:
            str = f"{str} (Per Hand):"
        print(f"{str} ${player.hands[0].bet_amount} | ", end="")
        print(f"Remaining Balance: {player.display_balance()}")

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


def start_new_game():
    """Called at the start of each game (round) to deal cards and reset flags"""
    # Check Shoe size and rebuild if necessary
    if shoe.size() < 40:
        shoe.clear()
        shoe.build()
        shoe.shuffle()
        bot.true_count = 0
        bot.running_count = 0

    # Get bet amount
    get_bet_amount()

    # Deal 2 initial cards to player and dealer
    for _ in range(2):
        player.hands[0].cards.append(shoe.deal())
        dealer.hands[0].cards.append(shoe.deal())

    # Let bot update card count, excluding dealers hidden card
    bot.update_count(player.hands[0].cards[0], shoe.size())
    bot.update_count(player.hands[0].cards[1], shoe.size())
    bot.update_count(dealer.hands[0].cards[0], shoe.size())

    # Hide dealer's second card
    dealer.hands[0].cards[1].hidden = True

    logger.hand_number = logger.hand_number + 1


def get_bet_amount():
    """Prompts user for a bet amount and stores it in hand object"""
    clear_screen()
    if not HUMAN_PLAYER:
        player.hands[0].bet_amount = bot.choose_bet_amount(player)
        player.balance -= player.hands[0].bet_amount
        logger.true_count = bot.true_count
        return
    print(f"WIN STREAK: {player.streak}\n")
    print(f"Balance: {player.display_balance()}")
    while True:  # Loop until valid bet amount is entered
        inp = input("Enter bet amount: $")
        if inp == "quit":
            exit()
        if inp == "":
            player.hands[0].bet_amount = 10
            break
        try:
            player.hands[0].bet_amount = int(inp)
            if player.hands[0].bet_amount > player.balance:
                raise ValueError("You don't have enough money!")
            if player.hands[0].bet_amount < MIN_BET:
                raise ValueError(f"Minimum bet is ${MIN_BET}!")
            break
        except ValueError as e:  # Error handling for invalid bet amount
            if str(e).startswith("invalid literal"):
                e = "Please enter a valid number!"
            print(f"Invalid bet amount: {e}")
    player.balance -= player.hands[0].bet_amount


def offer_insurance():
    insurance_taken = False
    if player.balance < int(player.hands[0].bet_amount / 2):
        return
    clear_screen()
    display_all_hands()
    if HUMAN_PLAYER:
        if input("Would you like insurance? (y/n)") == "y":
            insurance_taken = True
    else:
        insurance_taken = bot.choose_insurance_action(player.hands[0])
    if insurance_taken:
        player.hands[0].insured = True
        player.balance -= int(player.hands[0].bet_amount / 2)


# Function to handle player's turn
def player_turn():
    for hand in player.hands:
        while not hand.turn_over:
            # Give card to hand if split
            if len(hand.cards) == 1:
                hand.cards.append(shoe.deal())
                bot.update_count(hand.cards[-1], shoe.size())
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
            if (not dealer.hands[0].blackjack) and (player.hands[0].insured):
                print("Dealer does not have blackjack, insurance lost!")
            if not HUMAN_PLAYER:
                time.sleep(bot.speed / 5)

            # Refresh possible actions
            hand.update_options(player)

            # Get player action
            if not HUMAN_PLAYER:
                action = bot.choose_hand_action(hand, dealer.hands[0].cards[0].value)
            else:
                while True:
                    action = hand.get_action()
                    if not action == "help":
                        break
                    disp_table = {
                        "1": "Hit",
                        "2": "Stay",
                        "3": "Double",
                        "4": "Split",
                    }
                    print(
                        f"Bot recommends you {disp_table[bot.choose_hand_action(hand, dealer.hands[0].cards[0].value)]}!\n"
                    )

            # Perform player action
            if action == "1":  # Hit
                hand.cards.append(shoe.deal())
                bot.update_count(hand.cards[-1], shoe.size())
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
                bot.update_count(hand.cards[-1], shoe.size())
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
    bot.update_count(dealer.hands[0].cards[1], shoe.size())
    # Check if dealer turn is necessary
    if all(hand.busted for hand in player.hands):
        dealer.hands[0].turn_over = True

    while not dealer.hands[0].turn_over:
        lower_total = 0
        for card in dealer.hands[0].cards:
            lower_total += card.value
        upper_total = dealer.hands[0].total()
        display_all_hands()

        if (upper_total >= 18) or (lower_total == 17 and upper_total == 17):
            dealer.hands[0].turn_over = True
        else:
            # Dealer has to hit
            if HUMAN_PLAYER:
                time.sleep(1)
            else:
                time.sleep(bot.speed / 5)
            dealer.hands[0].cards.append(shoe.deal())
            bot.update_count(dealer.hands[0].cards[-1], shoe.size())

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
            logger.hand_outcome = "player_blackjack"
            logger.win_loss = "WIN"
        # Check for dealer BJ loss
        elif (dealer.hands[0].blackjack) and (not hand.blackjack):
            hand.outcome["message"] = f"{s}LOSE! Dealer has blackjack!"
            logger.hand_outcome = "dealer_blackjack"
            logger.win_loss = "LOSS"
            # Return bet if insurance was taken
            if hand.insured:
                hand.outcome["bal_change"] += hand.bet_amount
                player.balance += int(hand.bet_amount / 2)
                hand.outcome["message"] = "Dealer Blackjack! Insurance paid 2:1"
        # Check for player bust loss
        elif hand.busted:
            hand.outcome["message"] = f"{s}BUSTED! :("
            logger.hand_outcome = "player_bust"
            logger.win_loss = "LOSS"
        # Check for dealer bust win
        elif dealer.hands[0].busted:
            hand.outcome["message"] = f"{s}WIN! Dealer busted!"
            hand.outcome["bal_change"] += hand.bet_amount * 2
            logger.hand_outcome = "dealer_bust"
            logger.win_loss = "WIN"
        # Check for player win by being closer to 21
        elif hand.total() > dealer.hands[0].total():
            hand.outcome["message"] = f"{s}WIN! You beat the dealer!"
            hand.outcome["bal_change"] += hand.bet_amount * 2
            logger.hand_outcome = "player_beat_dealer"
            logger.win_loss = "WIN"
        # Check for dealer win by being closer to 21
        elif hand.total() < dealer.hands[0].total():
            hand.outcome["message"] = f"{s}LOSE! Dealer beat you!"
            logger.hand_outcome = "dealer_beat_player"
            logger.win_loss = "LOSS"
        # Result is a push
        else:
            hand.outcome["message"] = f"{s}PUSH! You tied the dealer!"
            hand.outcome["bal_change"] += hand.bet_amount
            logger.hand_outcome = "player_tie_dealer"
            logger.win_loss = "PUSH"


def update_balance():
    for hand in player.hands:
        player.balance += hand.outcome["bal_change"]
    logger.balance = str(player.balance)


def display_outcomes():
    if (not HUMAN_PLAYER) and (bot.speed == 0):
        print(f"Playing Hand {logger.hand_number} OF {bot.max_hands}")
        return
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

    # Offer insurance if dealer is showing ace
    if dealer.hands[0].cards[0].value == 1:
        offer_insurance()

    # Check for blackjacks
    check_blackjacks()

    # ---- Player's turn ----

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

    if HUMAN_PLAYER:
        input("\n\nPress enter to continue...")
    else:
        time.sleep(bot.speed / 3)
    reset_game()


# ---- Main ----
clear_screen()

# Create player and dealer
player = Player()
dealer = Player(dealer=True)

# Create bot
bot = Bot()

# Create shoe
shoe = Shoe()

# Ask if player wants to make a log file
if HUMAN_PLAYER:
    if input("Log file? (y/n)") == "y":
        log = True
    else:
        log = False
else:
    log = True

# Create logger
logger = Logger(make_file=log, bot=bot, human_player=HUMAN_PLAYER)


# Enter game loop while player has money
while player.balance >= MIN_BET:
    tmpbal = player.balance
    game_loop()
    # Update win streak
    if player.balance > tmpbal:
        player.streak += 1
    elif player.balance < tmpbal:
        player.streak = 0
    logger.streak = player.streak
    if log:
        logger.write_to_file()

    if (not HUMAN_PLAYER) and (logger.hand_number >= bot.max_hands):
        break
clear_screen()

if player.balance < MIN_BET:
    print("You ran out of money!")
else:
    print(f"Bot finished playing {bot.max_hands} hands")
    print(f"Final balance: {player.display_balance()}")
