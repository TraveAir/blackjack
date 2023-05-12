Blackjack

Introduction
This is a command-line program that implements a version of Blackjack. The game is played against the computer dealer, and the objective is to have a hand with a higher total value than the dealer's, without exceeding 21. Aces can have a value of 1 or 11, and face cards have a value of 10.

Requirements
This program requires Python 3.7 or higher to run.

How to Play
To start the game, run the script game.py from the command line. The game will then prompt you to enter your bet amount. The minimum bet amount is set in the game.py file.

You will then be dealt two cards, and the dealer will be dealt one card face up and one card face down. You will have the option to hit (receive another card) or stand (keep your current hand). If you receive two cards with the same value, you will have the option to split your hand into two separate hands.

Once you have decided to stand, the dealer will reveal their face-down card and continue drawing cards until their total is 17 or higher. The game will then compare your hand to the dealer's hand to determine the winner.

If your hand exceeds 21, you will bust and lose your bet. If the dealer busts, you will win your bet. If your hand and the dealer's hand have the same total, the game will end in a tie (push).

After each round, you will have the option to continue playing or quit the game. If you run out of money, the game will automatically end.

Classes


Card Class
The Card class represents a single playing card in a standard deck of 52 cards. It is used in the Hand class for blackjack game simulation.

Attributes:
name: the name of the card, which can be a string representation of a number, a face card or an Ace.
suit: the suit of the card, which can be Hearts, Diamonds, Clubs or Spades.
value: the value of the card, which can be an integer from 2 to 10 for numbered cards, 10 for face cards and 1 or 11 for an Ace.
hidden: a boolean flag indicating if the card is hidden. This flag is used for the second card of the dealer in the game of blackjack.



Hand Class
This class is used to represent a single playable blackjack hand and a dealer's hand. It contains attributes and methods to manage the cards in the hand, the bet amount, the status of the hand, and allowed actions.

Attributes
cards: A list of cards in the hand
bet_amount: The amount of money bet on the hand
busted: A boolean flag indicating if the hand is busted or not
turn_over: A boolean flag indicating if the hand is over or not
blackjack: A boolean flag indicating if the hand is a blackjack or not
allow_hit: A boolean flag indicating if a player can hit or not
allow_stay: A boolean flag indicating if a player can stay or not
allow_split: A boolean flag indicating if a player can split or not
allow_double: A boolean flag indicating if a player can double down or not
outcome: A dictionary with two keys: "message" and "bal_change", representing the message of the outcome and the amount of money the player's balance should change after the game.
Methods
__init__(): Initializes the class instance with the above attributes.
__repr__(): Returns a string representation of the hand.
display(): Prints to the console all the cards in the hand via ASCII art.
total(): Returns the total value of the cards in the hand.
bust_check(): Checks if the hand is busted and sets the "busted" and "turn_over" flags accordingly.
update_options(player): Updates the allowed action flags based on the hand and the player's status.
get_action(): Gets the player's action and returns the action number. It loops until a valid action is chosen.
Dependencies
game_util: A module that provides utility functions for the game.
card: A class that represents a single playing card.



Shoe Class

The Shoe class represents a container for a group of playing cards, known as a shoe. It is used in the game of blackjack for simulating card decks.

Attributes:
cards: a list of Card objects representing the cards in the shoe.

Methods:
init(): Initializes a new instance of the Shoe class, building the card deck with the specified number of decks and shuffling the cards.
build(): Creates the shoe by adding the specified number of decks of cards to the cards list.
shuffle(): Shuffles the cards in the shoe randomly.
display(): Displays the cards in the shoe, primarily used for debugging purposes.
size(): Returns the number of cards remaining in the shoe.
deal(): Removes and returns the top card from the shoe. Raises a ValueError if the shoe is empty.
clear(): Removes all the cards from the shoe.



Player Class
This class represents a player and dealer in the Blackjack game, and contains their hands and balance.

Properties
hands: A list of Hand objects, representing the hands of the player.
balance: A float representing the balance of the player.
streak: An integer representing the current win streak of the player.
name: A string representing the name of the player. If the Player object is created with dealer=True, the name is set to "DEALER", otherwise it's set to "PLAYER".
Methods
display_hands(total=False): Displays all hands for the player, along with their total value if total=True. If total=False, the hand totals are not displayed. If there is only one hand, the "HAND #" is not displayed.
