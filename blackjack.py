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
win_streak = 0
NUM_DECKS = 6

#Create Card Class
class Card:
    def __init__(self, name, value, suit):
        self.name = name
        self.value = value
        self.suite = suit

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
    for x in range(NUM_DECKS):
        tmp = build_deck()
        for y in tmp:
            shoe.append(y)
#Give a card to player or dealer
def deal_card(turn):
    card = random.choice(shoe)
    turn.append(card)
    shoe.remove(card)
        
#Print players' cards. Reveal both dealer cards?
def print_hands(reveal):
    if reveal:
        print("\n\n\n===================")
        print("DEALER: ", end="")
        for x in range(len(dealer_hand)):
            print(f"[{dealer_hand[x].name}] ", end="")
        print("\n---------------")
        print("PLAYER: ", end="")
        for x in range(len(player_hand)):
            print(f"[{player_hand[x].name}] ", end="")
        print("\n===================")
    else:
        print("\n\n\n===================")
        print(f"DEALER: [{dealer_hand[0].name}] [?]")
        print("---------------")
        print("PLAYER: ", end="")
        for x in range(len(player_hand)):
            print(f"[{player_hand[x].name}] ", end="")
        print("\n===================")
        
        
def print_hands_with_totals():
    print("\n\n\n===================")
    print("DEALER: ", end="")
    for x in range(len(dealer_hand)):
        print(f"[{dealer_hand[x].name}] ", end="")
    print(f" | Total: {total_hand(dealer_hand)}", end="")
    print("\n---------------")
    print("PLAYER: ", end="")
    for x in range(len(player_hand)):
        print(f"[{player_hand[x].name}] ", end="")
    print(f" | Total: {total_hand(player_hand)}", end="")
    print("\n===================")
    
#Total cards in hand
def total_hand(hand):
    num_aces = 0
    total = 0
    for card in hand:
        #check if card is an ace
        if card.value == 1:
            num_aces += 1
    
#    num_aces = len([card for card in hand if card.value == 1])
    
    for card in hand:
        total += card.value
    
    for _ in range(num_aces):
        if total + 10 <= 21:
            total+= 10
    return total

#Main Game
def main_game(balance, streak):
    #make the shoe if needed
    if len(shoe) < 50:
        shoe.clear()
        build_shoe()

    #Deal 2 cards to player and dealer
    for _ in range(2):
        deal_card(player_hand)
        deal_card(dealer_hand)
        

        
    #Players Turn

    #Define Variables
    player_BJ = False
    player_turn = True
    player_bust = False
    
    #Get Bet Amount
    print(f"Win Streak: {streak}")
    print(f"Current Balance: {balance}")
    bet_amount = int(input("Enter Bet Amount: "))
    while (bet_amount > balance) or (bet_amount == 0):
        print("Invalid Amount!")
        bet_amount = int(input("Enter Bet Amount: "))

    #Check for dealer BlackJack
    if total_hand(dealer_hand) == 21:
        player_turn = False
        
    #Check for player BlackJack
    if (total_hand(player_hand) == 21):
        player_BJ = True
        player_turn = False
        print_hands(True)

    #Give Player Chance to Act    
    while player_turn:
        print_hands(False)
        if (total_hand(player_hand) > 21):
            player_bust = True
            break
        elif (total_hand(player_hand) == 21):
            break
        if ((bet_amount * 2) <= balance) and (len(player_hand) == 2):
            allow_double = True
        else:
            allow_double = False
        if allow_double:
            player_action = input("1: Hit | 2: Stay | 3: Double: ")
        else:
            player_action = input("1: Hit | 2: Stay: ")
        if (player_action == '3') and (not(allow_double)):
            print("Double not allowed!!!!")
            player_action = '1'
        if player_action == '3':        
            bet_amount += bet_amount
            deal_card(player_hand)
            if (total_hand(player_hand) > 21):
                player_bust = True
            player_turn = False
        elif player_action == '2':
            player_turn = False
        else:
            deal_card(player_hand)
                
    #Dealers Turn
    print_hands(True)
    while not(player_bust) and not(player_BJ):
        print_hands(True)
        if total_hand(dealer_hand) >= 17:
            break
        time.sleep(1.5)
        deal_card(dealer_hand)

    #Determine Winner
    print_hands_with_totals()
          
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
player_balance = 100
while player_balance > 0:
    starting_balance = player_balance
    player_balance = main_game(player_balance, win_streak)
    if (player_balance > starting_balance):
        win_streak += 1
    elif (player_balance < starting_balance):
        win_streak = 0
print("You are out of money moron")
