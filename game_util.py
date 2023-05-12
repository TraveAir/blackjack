def display_hand(cards):
    card_size = 9
    hline = ""
    vline = "|"
    vspacer = ""
    hspacer = ""
    s = ""

    for _ in range(card_size):
        hline = f"{hline}-"
        vline = f"{vline} "
    vline = f"{vline}|"

    for card in cards:
        vspacer = f"{vspacer}\t{vline}"
        hspacer = f"{hspacer}\t {hline}"

    print(hspacer)
    print(vspacer)

    for card in cards:
        if card.name == "10":
            s = f"{s}\t{vline[:2]}{card.name}{vline[4:]}"
        else:
            s = f"{s}\t{vline[:2]}{card.name[0]}{vline[3:]}"
    print(s)
    s = ""

    print(vspacer)

    for card in cards:
        index = len(vline) // 2
        s = f"{s}\t{vline[:index]}{card.suit}{vline[index+1:]}"
    print(s)
    s = ""

    print(vspacer)

    for card in cards:
        index = len(vline) - 3
        if card.name == "10":
            s = f"{s}\t{vline[:index-1]}{card.name}{vline[index+1:]}"
        else:
            s = f"{s}\t{vline[:index]}{card.name[0]}{vline[index+1:]}"
    print(s)
    s = ""

    print(vspacer)
    print(hspacer)
