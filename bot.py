from hand import Hand
from hand import MIN_BET

BETTING_STRATEGY = "no_bust"
MAX_NUM_HANDS = 1000
BOT_SPEED = 3


class Bot:
    """Automated player using specified strategy
    Strategy Options:
    - flat_bet: Always bet the minimim, follow basic strategy
    - dealer_hitting: Always bet the minimum, hit/stay like the dealer would
    - no_bust: Always bet the minimum, hit if no chance of busting
    """

    def __init__(self):
        self.strategy = BETTING_STRATEGY
        self.max_hands = MAX_NUM_HANDS
        self.speed = BOT_SPEED

    def choose_bet_amount(self, player) -> int:
        return MIN_BET

    def choose_hand_action(self, player, current_hand) -> str:
        """Picks action based on strategy and returns 1/2/3/4
        Reference:
            1: Hit
            2: Stay
            3: Double
            4: Split"""
        if self.strategy == "no_bust":
            """----- NO BUST -----
            Always hit if no chance of busting, otherwise stay"""
            if current_hand.total() >= 18:
                return "2"
            else:
                # Must check for aces being counted as 11 by hand.total()
                tot = 0
                for card in current_hand.cards:
                    tot += card.value
                if tot <= 11:
                    return "1"
                else:
                    return "2"
        elif self.strategy == "dealer_hitting":
            """----- DEALER HITTING -----
            Always hit with 16 or less, otherwise stay"""
            if current_hand.total() <= 16:
                return "1"
            else:
                return "2"
        # ---DEFAULT---
        return "2"
