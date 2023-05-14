# Blackjack Game

## Introduction

This is a command-line program that simulates a realistic game of Blackjack. The game is played against the dealer (computer), and the objective is to have a hand with a higher total value than the dealer's, without exceeding 21. Aces can have a value of 1 or 11, and face cards have a value of 10.

## Requirements and Setup
To use color, you must have Rich installed. This can be done by running the command `pip install -r requirements.txt` from the code folder
This program requires Python 3.7 or higher to run.

## How to Play
### Download all files to a specific folder, install requirements as needed
### To start the game, run the file `game.py` from the command line

The program will first ask if you would like to create a log file. Entering `y` will make a text file in a subfolder called `/gamelogs/`. This file records the result of each hand played, in a csv format. 

You will then be prompted to enter a bet amount. This amount must be greater than [`MIN_BET`](/README.md/#constants-2), and may not be greater than your current balance. ___Typing `quit` on this prompt will close the program.___

Next, you will be dealt two cards, and the dealer will be dealt one card face up and one card face down.

If you are dealt a blackjack (Ace and 10 valued card), the game is over and you are paid 3:2 on your bet amount. 

If the dealer's visable card is an Ace - you will be prompted if you would like to purchase insurance or not. This allows you to insurre your bet against the dealer having a blackjack. Insurnace costs 1/2 your bet amount. After you accept or decline, the dealer will check for a blakjack. If they don't have a blackjack - the game continues as normal and your insurnace money (if purchased) is lost. If they do have a blackjack, you will immeditly lose your hand bet amount. If you purchased insurance, it is paied at a ratio of 2:1, meaning the end result of the hand is a push.

If no blackjacks are dealt:
You now have the option to hit (receive another card) or stand (keep your current hand). On the first two cards you are dealt, you also have the option to double (balance permitting), meaning you double your bet amount and will exactly one additional card. If you receive two cards with the same value, you will have the option to split your hand into two separate hands.

___You also have the option to type `help` and the bot will tell you which action it recommends based on it's current playing strategy.___

Once you have decided to stand, have a total of 21, or bust (exceed 21) the dealer will reveal their face-down card and continue drawing cards until their total is 17 or higher. The dealer must hit on soft 17. If you bust on your turn, the dealer will not draw any cards.

If you hand total is more than the dealers, or the dealer busts, you win and your bet is paid at 1:1. If the dealer hand total is more than yours, or you bust, your bet is lost. If you and the dealer have the same total, the resilt is a PUSH and your original bet is returned.

After each round, you will be prompted for a new bet amount. If you run out of money, the game will automatically end.

## Bot Functionality

### Intro

This program includes the ability to have a computer (bot) play hands based on pre-defined strategies. This allows a large number of hands to be played rapidly, allowing for data colletion regarding different playing strategies.

### Human or Bot Toggle

In order to switch between playing the game yourself and the bot playing, change the `HUMAN_PLAYER` constant near the top of `game.py`.
<br>A value of `True` means a human is playing and the game will prompt you for actions.
<br>A value of `False` means the bot is the player and all prompts are replaced with bot decision making

### Bot Parameters

___ALL Parameters are at the top of `bot.py`___

#### Betting Strategy

This changes how the bot determines the amount it should bet each round

Options
- `flat`
  - Always bets the same amount, equal to `MIN_BET` 
- `modfib`
  - Increases the bet amount based on the current win streak, by multiplying the base bet (`MIN_BET`) by a modified fibbonaci sequence of *"1, 1, 2, 3, 5, 5, 7, 10"*
  - Example (HAND/BET/Result): 1/$10/WIN, 2/$10/WIN, 3/$20/WIN, 4/$30/LOSS, 5/$10/LOSS, 6/$10/WIN, 7/$10/WIN, 8/$20/WIN, 9/$30/WIN, 10/$50/WIN, 11/$50/LOSS, 12/$10/...

#### Action Strategy

Picks weather to hit, stay, double, or split.

Options
- `basic`
  - Follow standard basic strategy. [This](https://wizardofodds.com/blackjack/images/bj_4d_h17.gif) version was used
- `no_bust`
  - Never bust. Always hits with a (soft) total of 11 or less. Otherwise, always stays.
- `dealer_hitting`
  - Follow the same strategy as the dealer. Always hits with less than 17, stays with 18 or more. Hits on soft 17.

#### Insurance Strategy
Decides weather to take insurance or not when offered.

- `never`
  - Never takes insurance. 
- `always`
  - Always takes insurance when offered.

## Classes

### Card

`card.py`
Represents a single playing card. It has attributes for the name, suit, value, and whether or not the card is hidden (for the dealer's second card).

#### Constants
- `CARD_SUITS` - list of suit icons used for the cards
- `CARD_NAMES` - list of card display names as strings

#### Attributes
- `name` - string representing the card name (ex: "Ace", "King", "8")
- `suit` - string representing the card suit (ex: "♥", "♦", "♣", "♠")
- `value` - integer representing the card value (ex: 1 for Ace, 10 for face cards)
- `hidden` - boolean representing whether the card is hidden or not (default is False)

Methods
There are no methods defined in this class other than the __repr__ method which returns a string representation of the card in the format "[name of suit]".

### Shoe

`shoe.py`
Represents a collection of cards, ready to be used in the game. Cards are stored in the shoe and dealt when needed. Once the shoe has less than 40 cards left, it is re-built.

#### Constants
- `NUM_DECKS` - integer to set the number of 52 card decks that should be added to the show when built


#### Attributes
- `cards` - list of Card objects

#### Methods
- build() - Builds a shoe with `NUM_DECKS` of cards, each containing 52 cards with 13 different card names and 4 different suits. This method creates a new Card object for each card and appends it to the cards list.
- shuffle() - Shuffles the cards in the shoe using the random.shuffle() method.
- display() - Prints the list of Card objects in the cards list. Used only for debugging purposes.
- size() - Returns the number of Card objects in the cards list.
- deal() - Removes the first card from the cards list and returns it as a Card object.
- clear() - Clears all Card objects from the cards list. Used before re-building the shoe.

### Hand

`hand.py`
Represents a single blackjack hand for the player or dealer.

#### Constants
`MIN_BET` - integer minimum bet allowed for the hand

#### Attributes
- `cards` - list of Card objects
- `bet_amount` - integer size of player bet for the hand
- `busted` - boolean if the hand value is > 21
- `turn_over` - boolean if  the hand should be allowed to make another action decision
- `blackjack` - boolean if the hand was dealt as a blackjack
- `insured` - boolean if the was insured when the dealer is showing an ace
- `allow_hit`/`allow_stay`/`allow_split`/`allow_double` - boolean flags for allowed actions
- `outcome` - dictonary that stores a message with the win/loss result of the hand and the amount the player blance should be adjusted a result

##### Methods
- display(use_color=True) - print all cards in hand via ASCII art. Set use_color to false to turn off color display.
- total() - Calculates the total value of the hand, with aces counted as their maximum allowed
- bust_check() - If the hand totale is >21, updates the busted attribute and ends the turn
- update_options() - Updates the allowed action flags based on game inormation
- get_action() - Prompts the user for an action based on the allowed action flags


### Player

`player.py`
Represents the player (bot or human) and dealer

#### Constants
- `STARTING_BALANCE` - integer amount of money player should start with

#### Attributes
- `hands` - list of hands the player has. Used for splits.
- `balance` - integer for how much money the player has left
- `streak` - integer keeping track of how many hands in a row have been won
- `name` - string "PLAYER" or "DEALER"

#### Methods
- display_balance() - returns string with the players balance prefixed with '$'
- display_hands() - prints all of the players hands

### Logger

`logger.py`
Back-end class that makes the log file

#### Attributes
- `balance`- integer to strore balance info
- `hand_outcome` - string to store how the hand was won or lost
- `win_loss` - string to record win/loss/push
- `strak` - integer to store player win streak
- `hand number` - integer to keep track of how many hands have been played
- `filepath` - string containing the path of the file being written to
- `human_player` - boolean to tell logger if human or bot is playing
- `bot` - Bot class attribute to get bot strategy info

#### Methods
- make_file_path() - returns a string with the file path to be used based on current time, play style, and existing file conflicts
- initial_write() - Creates the file and write the first row with data headings
- write_to_file() - Adds a line to the log file with game data


### Bot

`bot.py`
Class for the bot to store info and make decisions

#### Constants
- `BETTING_STRATEGY` - string to set the desired betting strategy
- `ACTION_STRATEGY` - string to set the desired action decision making strategy
- `INSURANCE_STRATEGY` - string to set the desired insurance taking strategy
- `MAX_NUM_HANDS` - integer for how many hands the bot will play before stopping
- `BOT_SPEED` - integer for how fast the cards should be visually displayed. Set to 0 for instant.

#### Attributes
- All constants stored in attributes with same name

#### Methods
- choose_bet_amount() - returns an integer bet amount based on current strategy
- choose_hand_action() - returns a string represeting hit, stay, double, or split based on current strategy
- choose_insurance_action() - returns a boolean for if instuance will be taken or not based on current strategy
