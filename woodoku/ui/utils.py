from typing import Iterable, Type, TypeVar

T = TypeVar("T", str, int)

RED = (255, 0, 0)  # warning, boundary of 3X3 blocks
GREEN = (0, 255, 0)  # block
ORANGE = (255, 128, 0)  # score

BLOCK = chr(0x25A0)
TOP_RIGHT = chr(0x2510)
TOP_LEFT = chr(0x250C)
HORIZONTAL = chr(0x2500)
BOLD_HORIZONTAL = chr(0x2501)
BOTTOM_LEFT = chr(0x2514)
BOTTOM_RIGHT = chr(0x2518)
VERTICAL = chr(0x2502)
LEFT_JOIN = chr(0x251C)
RIGHT_JOIN = chr(0x2524)
CROSS = chr(0x253C)
BOTTOM_JOIN = chr(0x2534)
TOP_JOIN = chr(0x252C)
BOLD_LEFT_JOIN = chr(0x2521)
VERTICAL_CROSS = chr(0x2542)
BOLD_RIGHT_JOIN = chr(0x2543)
BOLD_VERTICAL = chr(0x2503)
BOLD_TOP_JOIN = chr(0x2530)
BOLD_BOTTOM_JOIN = chr(0x2538)
ALL_BOLD_CROSS = chr(0x254B)
HORIZONTAL_BOLD_CROSS = chr(0x253F)


def __colored(r: int, g: int, b: int, text: str) -> str:
    return f"\033[38;2;{r};{g};{b}m{text}\033[38;2;255;255;255m"


def red(text: str) -> str:
    return __colored(*RED, text)


def green(text: str) -> str:
    return __colored(*GREEN, text)


def orange(text: str) -> str:
    return __colored(*ORANGE, text)


def inbetween(
        start: str, in_between: str, bold_in_between: str, end: str, horizontal_bar: str
) -> str:
    """Return a string which is further printed out in the terminal as a horizontal line.
    """
    # The string starts with the start strings followed with eight iterations of horizontal_bar and in_between.
    row_str = f"{start}"
    for col in range(8):
        line = horizontal_bar
        if col in (2, 5):  # the borders of every 3X3 blocks is at col = 2 and col = 5 and thus need to be bolded
            line += bold_in_between
        else:
            line += in_between
        row_str += line

    # The string ends with end string
    row_str += horizontal_bar
    row_str += end
    return row_str


def get_input(
        convert: Type[T],
        valid: Iterable[T],
        input_msg: str,
        again_msg: str,
) -> T:
    """Ask for user input of the requested type `T`, will keep asking until a
    valid value is entered

    Args:
        convert (Type[T]): The class of the data requested (used for conversion
            e.g. int for integer)
        valid (Iterable[T]): A collection of values to validate the user input
            against
        input_msg (str): Initial input request message
        again_msg (str): Try Again message

    Returns:
        T: Validated value
    """
    # do while pattern in python
    while True:
        try:
            choice = convert(input(input_msg))
            if choice in valid:
                break
            print(again_msg)
        except ValueError:
            print(again_msg)
    return choice
