import datetime
import os


class Logger:
    balance = ""
    hand_outcome = ""
    win_loss = ""
    streak = 0
    hand_number = 0

    def __init__(self, make_file):
        self.filepath = ""
        if make_file:
            self.filepath = self.make_file_path()

    def make_file_path(self) -> str:
        base_path = os.path.dirname(os.path.realpath(__file__)) + "/gamelogs/"
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        current_time = datetime.datetime.now()

        file_name = current_time.strftime("%m%d.%H%M")

        pth = base_path + file_name
        x = 1
        s = ""
        while os.path.exists(pth + f"{s}.txt"):
            s = f"({x})"
            x += 1

        pth += f"{s}.txt"

        return pth

    def write_to_file(self):
        s = f"{self.hand_number},{self.balance},{self.win_loss},{self.streak},{self.hand_outcome}"
        with open(self.filepath, "a") as f:
            f.write(s + "\n")
