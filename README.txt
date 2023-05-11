Blackjack game
This code implements a Blackjack game. The game is played with a standard deck of cards, and the rules follow standard Blackjack rules. The game begins with the player and the dealer each being dealt two cards, with one of the dealer's cards being hidden. The player can then choose to "hit" (take another card) or "stay" (keep their current hand). The player can also "double down" (double their bet and take one more card) if they have a two-card hand. Additionally, if the player is dealt two cards of the same rank, they can "split" their hand into two separate hands, with each hand receiving a second card and a second bet equal to the first. The dealer must hit until they have a total of 17 or higher, and must stay if they have a total of 17 or higher.

Files
blackjack.py: The main Python script containing the code for the game.
Usage
Run the blackjack.py script to start the game.

Rules
The game is played with a standard deck of 52 cards.
The goal is to get a hand with a higher total than the dealer's hand, without going over 21.
Cards 2 through 10 are worth their face value. Jack, Queen, and King are worth 10. Ace is worth 1 or 11, whichever is more advantageous to the player.
The player and the dealer each start with two cards. The player can see their own cards, but can only see one of the dealer's cards.
The player can choose to "hit" (take another card) or "stay" (keep their current hand). The player can also "double down" (double their bet and take one more card) if they have a two-card hand. Additionally, if the player is dealt two cards of the same rank, they can "split" their hand into two separate hands, with each hand receiving a second card and a second bet equal to the first.
The dealer must hit until they have a total of 17 or higher, and must stay if they have a total of 17 or higher.
If the player's hand goes over 21, they "bust" and lose their bet.
If the dealer's hand goes over 21, the player wins their bet.
If the player and dealer have the same total, it is a "push" and the player keeps their bet.
If the player's hand is closer to 21 than the dealer's hand, the player wins their bet.
If the dealer's hand is closer to 21 than the player's hand, the player loses their bet.