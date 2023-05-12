from card import Card

V_BAR = "┃"
H_BAR = "━"
TOP_LEFT = "┏"
TOP_RIGHT = "┓"
BOTTOM_LEFT = "┗"
BOTTOM_RIGHT = "┛"
SPACER = "  "


# For list of valid colors, see:
#   https://rich.readthedocs.io/en/latest/appendix/colors.html#appendix-colors
BLACK_CARD_COLOR = "bright_yellow"
RED_CARD_COLOR = "red"
HIDDEN_CARD_COLOR = "cyan"


def display_hand(cards: list[Card], width: int = 9, use_color: bool = True):
    """
    Print cards in a players hand, in a row, using ASCII art.

    If `use_color` is True, the [rich library](https://rich.readthedocs.io/en/latest/) is required.
    """

    # this import is only needed if we're using color
    if use_color:
        from rich import print

    # helper function to wrap text in 'rich' color tags
    # it is a closure, so it has access to use_color
    # see: https://rich.readthedocs.io/en/latest/markup.html#syntax
    def colorize_text(text: str, color: str):
        if use_color:
            return f"[bold {color}]{text}[/bold {color}]"
        return text

    # make basic building blocks
    card_top = f"{TOP_LEFT}{H_BAR * width}{TOP_RIGHT}"
    card_bottom = f"{BOTTOM_LEFT}{H_BAR * width}{BOTTOM_RIGHT}"
    card_inner = f"{V_BAR}{' ' * width}{V_BAR}"

    # ----- make top, bottom, and inner rows -----
    #
    # Eg,
    #   top_row:
    #   "┏━━━━━━━━━┓  ┏━━━━━━━━━┓"

    #   inner_row:
    #   "┃         ┃  ┃         ┃"

    #   bottom_row:
    #   "┗━━━━━━━━━┛  ┗━━━━━━━━━┛"

    top_row = ""
    bottom_row = ""
    inner_row = ""

    for card in cards:
        color = get_card_color(card)
        top_row += SPACER + colorize_text(card_top, color)
        bottom_row += SPACER + colorize_text(card_bottom, color)
        inner_row += SPACER + colorize_text(card_inner, color)

    # ----- make upper and lower number rows -----
    #
    # Eg,
    #   upper_num_row:
    #   "┃ 10      ┃  ┃ 10      ┃"
    #
    #   lower_num_row:
    #   "┃      10 ┃  ┃      10 ┃"

    upper_num_row = ""
    lower_num_row = ""

    for card in cards:
        # "char" is the first character of the card name, or the full name if it's a 10
        char = card.name[0]
        if card.name == "10":
            char = card.name
        if card.hidden:
            char = "?"

        # make card section
        start = f"{V_BAR} {char}"
        end = f"{char} {V_BAR}"
        card_upper_num = start + card_inner[len(start) :]
        card_lower_num = card_inner[: -len(end)] + end

        # add card section to row
        color = get_card_color(card)
        upper_num_row += SPACER + colorize_text(card_upper_num, color)
        lower_num_row += SPACER + colorize_text(card_lower_num, color)

    # ----- make suit row -----
    #
    # Eg,
    #   suit_row:
    #   "┃   ♥     ┃  ┃   ♥     ┃"

    suit_row = ""

    for card in cards:
        # determine suit, "?" if hidden
        suit = card.suit
        if card.hidden:
            suit = "?"

        # make card section
        index = len(card_inner) // 2
        card_suit_section = card_inner[:index] + suit + card_inner[index + 1 :]

        # add card section to row
        color = get_card_color(card)
        suit_row += SPACER + colorize_text(card_suit_section, color)

    # ----- print output -----
    output = [
        top_row,
        upper_num_row,
        inner_row,
        suit_row,
        inner_row,
        lower_num_row,
        bottom_row,
    ]
    print("\n".join(output))


def get_card_color(card: Card) -> str:
    """
    Determine card color based on suit and hidden status
    """

    if card.hidden:
        return HIDDEN_CARD_COLOR

    color_map = {
        "♥": RED_CARD_COLOR,
        "♦": RED_CARD_COLOR,
        "♣": BLACK_CARD_COLOR,
        "♠": BLACK_CARD_COLOR,
    }

    color = color_map.get(card.suit, BLACK_CARD_COLOR)
    return color
