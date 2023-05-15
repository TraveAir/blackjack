import datetime
import os
from bot import Bot


class Logger:
    balance = ""
    hand_outcome = ""
    win_loss = ""
    streak = 0
    hand_number = 0
    true_count = 0

    def __init__(self, make_file, bot, human_player):
        self.filepath = ""
        self.human_player = human_player
        self.bot = bot
        if make_file:
            self.filepath = self.make_file_path()
            self.initial_write()

    def make_file_path(self) -> str:
        base_path = os.path.dirname(os.path.realpath(__file__)) + "/gamelogs/"
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        current_time = datetime.datetime.now()

        file_name = current_time.strftime("%m%d.%H%M")
        if self.human_player:
            file_name += "_Player"
        else:
            file_name += (
                f"____{self.bot.betting_strategy}____{self.bot.action_strategy}"
            )

        pth = base_path + file_name
        x = 1
        s = ""
        while os.path.exists(pth + f"{s}.txt"):
            s = f"({x})"
            x += 1

        pth += f"{s}.txt"

        return pth

    def initial_write(self):
        with open(self.filepath, "w") as f:
            f.write("Hand Number,Balance,Win/Loss,Win Streak,True Count,Hand Outcome\n")

    def write_to_file(self):
        s = f"{self.hand_number},{self.balance},{self.win_loss},{self.streak},{self.true_count},{self.hand_outcome}"
        with open(self.filepath, "a") as f:
            f.write(s + "\n")
