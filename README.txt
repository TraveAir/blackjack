Blackjack

Introduction
This is a command-line program that implements a simple version of Blackjack. The game is played against the computer dealer, and the objective is to have a hand with a higher total value than the dealer's, without exceeding 21. Aces can have a value of 1 or 11, and face cards have a value of 10.

Requirements
This program requires Python 3.7 or higher to run.

How to Play
To start the game, run the script game.py from the command line. The game will then prompt you to enter your bet amount. The minimum bet amount is 5.

You will then be dealt two cards, and the dealer will be dealt one card face up and one card face down. You will have the option to hit (receive another card) or stand (keep your current hand). If you receive two cards with the same value, you will have the option to split your hand into two separate hands.

Once you have decided to stand, the dealer will reveal their face-down card and continue drawing cards until their total is 17 or higher. The game will then compare your hand to the dealer's hand to determine the winner.

If your hand exceeds 21, you will bust and lose your bet. If the dealer busts, you will win your bet. If your hand and the dealer's hand have the same total, the game will end in a tie (push).

After each round, you will have the option to continue playing or quit the game. If you run out of money, the game will automatically end.

Classes

Card
Represents a single card in a deck
Properties:
name: card name, printed on screen
suit: card suit
value: card value, 10 for face cards
hidden: hidden flag for dealer's second card

Shoe
Represents a shoe (i.e., multiple decks) of cards
Properties:
cards: list of cards in shoe
Methods:
build(): builds shoe with NUM_DECKS decks of cards
shuffle(): shuffles the shoe
display(): displays shoe for debugging
size(): gets the size of the shoe
deal(): deals the first card in the shoe
clear(): clears all cards in the shoe

Hand
Represents a single playable hand
Properties:
cards: list of cards in hand
bet_amount: bet amount for hand
busted: flag for whether the hand has busted (i.e., total value exceeds 21)
turn_over: flag for whether the hand's turn is over (i.e., player has stood or hand has busted)
blackjack: flag for whether the hand has a Blackjack (i.e., initial two cards have a total value of 21)
allow_split: flag for whether the hand can be split
allow_double: flag for whether the hand can be doubled down
Methods:
display(): displays all cards in hand via ASCII art
total(): gets the total value of the hand

Variables
NUM_DECKS: number of decks in shoe
STARTING_BALANCE: starting balance for player
MIN_BET: minimum bet amount
CARD_SUITS: list of card suits
CARD_NAMES: list of card names
