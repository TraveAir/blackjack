from hand import Hand, MIN_BET
from card import Card
from player import Player

BETTING_STRATEGY = "mitcount"
ACTION_STRATEGY = "basic"
INSURANCE_STRATEGY = "never"

# Bot will stop playing after this many hands
MAX_NUM_HANDS = 5000

# How fast cards are displayed on screen, lower is faster, 0 is instant
BOT_SPEED = 0


class Bot:
    """Automated player using specified strategy
    BETTING_STRATEGY OPTIONS:
    - flat: Always bet the minimim
    - modfib: Bet a modified fibonacci sequence: 1, 1, 2, 3, 5, 5, 7, 10
    - mitcount: Count cards: Bet with MIT strategy of (TC-1)*min_bet

    ACTION_STRATEGY OPTIONS:
    - dealer_hitting: Hit with 16 or less, otherwise stay
    - no_bust: Hit if no chance of busting
    - basic: Basic strategy

    INSURANCE_STRATEGY OPTIONS:
    - always: Always take insurance
    - never: Never take insurance
    """

    def __init__(self):
        self.betting_strategy = BETTING_STRATEGY
        self.action_strategy = ACTION_STRATEGY
        self.insurance_strategy = INSURANCE_STRATEGY
        self.max_hands = MAX_NUM_HANDS
        self.speed = BOT_SPEED
        self.running_count = 0
        self.true_count = 0

    def choose_bet_amount(self, player: Player) -> int:
        """Returns bet amount based on BETTING_STRATEGY"""
        if self.betting_strategy == "flat":
            """----- FLAT BET -----
            Always bet the minimum"""
            return MIN_BET
        elif self.betting_strategy == "modfib":
            """----- MODIFIED FIBONACCI -----
            Multiplies MIN_BET based on win sequence"""
            fib_sequence = {0: 1, 1: 1, 2: 2, 3: 3, 4: 5, 5: 5, 6: 7, 7: 10}
            spot_in_sequence = player.streak % 8
            return MIN_BET * fib_sequence[spot_in_sequence]
        elif self.betting_strategy == "mitcount":
            """----- MIT COUNT -----
            When TC is less than 2, bet minimum. Otherwise, bet (TC-1)*min_bet"""
            if self.true_count < 2:
                return MIN_BET
            else:
                if player.balance < (self.true_count - 1) * 10:
                    return player.balance
                return (self.true_count - 1) * 10
        # ---DEFAULT---
        else:
            return MIN_BET

    def choose_hand_action(self, hand: Hand, dealer_showing: Card) -> str:
        """Picks action based on ACTION_STRATEGY and returns 1/2/3/4
        Reference:
            1: Hit
            2: Stay
            3: Double
            4: Split"""
        ret_table = {"hit": "1", "stay": "2", "double": "3", "split": "4"}
        # Calculate upper and lower totals
        lower_total = 0
        for card in hand.cards:
            lower_total += card.value
        upper_total = hand.total()

        if self.action_strategy == "basic":
            """----- BASIC STRATEGY -----
            Follows https://wizardofodds.com/blackjack/images/bj_4d_h17.gif
            """
            # ---SPLITTING---
            if hand.allow_split and hand.cards[0].value not in [5, 10]:
                if hand.cards[0].value in [1, 8]:
                    # Always split aces and 8s
                    return ret_table["split"]
                elif hand.cards[0].value == 9:
                    if dealer_showing in [7, 10, 1]:
                        return ret_table["stay"]
                    else:
                        return ret_table["split"]
                elif hand.cards[0].value in [2, 3, 7]:
                    if dealer_showing in [2, 3, 4, 5, 6, 7]:
                        return ret_table["split"]
                    else:
                        return ret_table["hit"]
                elif hand.cards[0].value == 6:
                    if dealer_showing in [2, 3, 4, 5, 6]:
                        return ret_table["split"]
                    else:
                        return ret_table["hit"]
                else:  # 4s
                    if dealer_showing in [5, 6]:
                        return ret_table["split"]
                    else:
                        return ret_table["hit"]

            # ---SOFT HANDS---
            elif lower_total != upper_total:
                if upper_total >= 20:
                    return ret_table["stay"]
                elif upper_total == 19:
                    if (dealer_showing == 6) and (hand.allow_double):
                        return ret_table["double"]
                    else:
                        return ret_table["stay"]
                elif upper_total == 18:
                    if dealer_showing in [9, 10, 1]:
                        return ret_table["hit"]
                    elif dealer_showing in [2, 3, 4, 5, 6] and hand.allow_double:
                        return ret_table["double"]
                    else:
                        return ret_table["stay"]
                elif upper_total == 17:
                    if dealer_showing in [3, 4, 5, 6] and hand.allow_double:
                        return ret_table["double"]
                    else:
                        return ret_table["hit"]
                elif (upper_total == 16) or (upper_total == 15):
                    if dealer_showing in [4, 5, 6] and hand.allow_double:
                        return ret_table["double"]
                    else:
                        return ret_table["hit"]
                else:
                    if dealer_showing in [5, 6] and hand.allow_double:
                        return ret_table["double"]
                    else:
                        return ret_table["hit"]

            # ---HARD HANDS---
            else:
                if upper_total >= 17:
                    return ret_table["stay"]
                elif upper_total in [13, 14, 15, 16]:
                    if dealer_showing in [7, 8, 9, 10, 1]:
                        return ret_table["hit"]
                    else:
                        return ret_table["stay"]
                elif upper_total == 12:
                    if dealer_showing in [4, 5, 6]:
                        return ret_table["stay"]
                    else:
                        return ret_table["hit"]
                elif upper_total == 11:
                    if hand.allow_double:
                        return ret_table["double"]
                    else:
                        return ret_table["hit"]
                elif upper_total == 10:
                    if dealer_showing in [2, 3, 4, 5, 6, 7, 8, 9] and hand.allow_double:
                        return ret_table["double"]
                    else:
                        return ret_table["hit"]
                elif upper_total == 9:
                    if dealer_showing in [3, 4, 5, 6] and hand.allow_double:
                        return ret_table["double"]
                    else:
                        return ret_table["hit"]
                else:
                    return ret_table["hit"]

        elif self.action_strategy == "no_bust":
            """----- NO BUST -----
            Always hit if no chance of busting, otherwise stay"""
            if lower_total <= 11:
                return ret_table["hit"]
            else:
                return ret_table["stay"]
        elif self.action_strategy == "dealer_hitting":
            """----- DEALER HITTING -----
            Always hit with 16 or less, otherwise stay. Hit on soft 17"""
            if (upper_total >= 18) or (lower_total == 17 and upper_total == 17):
                return ret_table["stay"]
            else:
                return ret_table["hit"]
        # ---DEFAULT---
        return ret_table["stay"]

    def choose_insurance_action(self, hand: Hand) -> bool:
        """Returns True or False based on INSURANCE_STRATEGY"""
        if self.insurance_strategy == "always":
            return True
        else:
            # ---DEFAULT---
            return False

    def update_count(self, card: Card, shoe_size: int):
        """Updates running count and true count based on card value"""
        if card.value in [2, 3, 4, 5, 6]:
            self.running_count += 1
        elif card.value in [10, 1]:
            self.running_count -= 1
        self.true_count = self.running_count // (shoe_size / 52)
