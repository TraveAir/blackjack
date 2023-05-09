# -*- coding: utf-8 -*-
"""
Created on Sun May  7 18:47:39 2023

@author: Travis
"""
import random
import time

shoe = []
player_hand = []
dealer_hand = []
streak = 0
balance = 0
bet_amount = 0
NUM_DECKS = 6
player_doubled = False
player_split_count = 0

#Create Card Class
class Card:
    def __init__(self, name, value, suit):
        self.name = name
        self.value = value
        self.suit = suit
        
    def __repr__(self):
        return f"{self.name} of {self.suit}"

#Build the 52 card deck
def build_deck():
    tmp = []
    for x in range(4):
        if x == 0:
            suit = "Spades"
        elif x == 1:
            suit = "Clubs"
        elif x == 2:
            suit = "Hearts"
        else:
            suit = "Diamonds"
        for y in range(13):
            if y < 9:
                value = y+2
                name = str(value)
            elif y == 9:
                name = "Jack"
                value = 10
            elif y == 10:
                name = "Queen"
                value = 10
            elif y == 11:
                name = "King"
                value = 10
            else:
                name = "Ace"
                value = 1
                
            tmp.append(Card(name, value, suit))
    return tmp
        
def build_shoe():
    #Creates a show with NUM_DUCKS number of decks in it
    
    #make a deck of 52 cards
    tmp = build_deck()
    
    #add the deck to the show NUM_DECKS number of times
    for x in range(NUM_DECKS):
        shoe.extend(tmp)
        
    #Shuffle the shoe
    random.shuffle(shoe)
    #Shuffle it some more
    random.shuffle(shoe)
    #MORE
    random.shuffle(shoe)

def deal_card(hand):
    #Move the first card in the shoe to hand
    hand.append(shoe.pop(0))
        
#Print players' cards. Reveal both dealer cards? Show Total?
def print_hands(reveal, total):
    dline = "\n==================="
    print(f"\n\n{dline}")
    print("DEALER: ", end="")
    if reveal:
        for card in dealer_hand:
            print(f"[{card.name}] ", end="")
    else:
        print(f"DEALER: [{dealer_hand[0].name}] [?]", end="")
    if total:
        print(f" -> Total = {total_hand(dealer_hand)}", end="")
    print("\n---------------")
    print("PLAYER: ", end="")
    for card in player_hand:
        print(f"[{card.name}] ", end="")
    if total:
        print(f" -> Total = {total_hand(player_hand)}", end="")
    print(dline)
        
    
    
#Total card values in hand
def total_hand(hand):
    #Set total to 0
    total = 0
    
    #Count number of aces in deck
    num_aces = len([card for card in hand if card.value == 1])
    
    #Total all cards value
    for card in hand:
        total += card.value
    
    #Check if each ace should be 11 or 1
    for _ in range(num_aces):
        if total + 10 <= 21:
            total+= 10
    return total


def check_shoe():
    #If shoe has <52 cards, rebuild it
    if len(shoe) < 52:
        shoe.clear()
        build_shoe()

def check_bj(hand):
    if total_hand(hand) == 21:
        return True
    else:
        return False
    
def check_bust(hand):
    if total_hand(hand) > 21:
        return True
    else:
        return False

def get_bet_amount(balance, streak):
    #Returns the amount the player wants to bet
    print(f"Win Streak: {streak}")
    print(f"Current Balance: {balance}")
    bet_amount = int(input("Enter Bet Amount: "))
    while (bet_amount > balance) or (bet_amount == 0):
        print("Invalid Amount!")
        bet_amount = int(input("Enter Bet Amount: "))
    return bet_amount

def get_player_action():
    if ((bet_amount * 2) <= balance) and (len(player_hand) == 2):
        double_allowed = True
        if player_hand[0].value == player_hand[1].value:
            split_allowed = True
        else:
            split_allowed = False
    else:
        double_allowed = False
        split_allowed = False
        
    print("1:Hit | 2:Stay ", end="")
    if (double_allowed):
        print(" | 3:Double ", end="")
    if (split_allowed):
        print(" | 4:Split ", end="")
    return input()
        
        
        
def player_turn():
    still_turn = True
    while still_turn:
        print_hands(False, False)
        if check_bust(player_hand):
            break
        
        player_action = get_player_action()
        
        if player_action == '1':
            deal_card(player_hand)
        elif player_action == '2':
            break
        elif player_action == '3':
            player_doubled = True
            deal_card(player_hand)
            break
            
        
#Main Game
def main_game():
    #Check for valid shoe
    check_shoe()
    
    #Get bet amount
    bet_amount = get_bet_amount()
    
    #Deal 2 cards to player and dealer
    for _ in range(2):
        deal_card(player_hand)
        deal_card(dealer_hand)       
    
    #Check for Blackjacks
    player_bj = check_bj(player_hand)
    dealer_bj = check_bj(dealer_hand)
    
    #If no blackjacks, give player their turn
    if not(player_bj) or not(dealer_bj):
        player_turn()
        
                
    #Dealers Turn
    print_hands(True, False)
    while not(player_bust) and not(player_BJ):
        print_hands(True, False)
        if total_hand(dealer_hand) >= 17:
            break
        time.sleep(1.5)
        deal_card(dealer_hand)

    #Determine Winner
    print_hands(True, True)
          
    if player_BJ:
        print("Blackjack!!! You Win!!!")
        bet_amount = int(bet_amount * 1.5)
        balance += bet_amount
    elif player_bust:
        print("You Bust! Dealer Wins :(")
        balance -= bet_amount
    elif total_hand(dealer_hand) > 21:
        print("Dealer Busts! Winner!!")
        balance += bet_amount
    elif (21 - total_hand(player_hand) < (21 - total_hand(dealer_hand))):
        print("You Win!!")
        balance += bet_amount
    elif (21 - total_hand(dealer_hand) < (21 - total_hand(player_hand))):
        print("Dealer Wins :(")
        balance -= bet_amount
    else:
        print("Game is a Push")
        
    input("\nPress enter to continue...\n\n\n\n")

    player_hand.clear()
    dealer_hand.clear()
    
    return balance

#Start Game
balance = 100
while balance > 0:
    starting_balance = balance
    balance = main_game()
    if (balance > starting_balance):
        win_streak += 1
    elif (balance < starting_balance):
        win_streak = 0
print("You are out of money moron")
