RED = (255, 0, 0)       # warning
GREEN = (0, 255, 0)     # block
ORANGE = (255, 128, 0)  # score

BLOCK = chr(0x25a0)
TOP_RIGHT = chr(0x2510)
TOP_LEFT = chr(0x250c)
HORIZONTAL = chr(0x2500)
BOTTOM_LEFT = chr(0x2514)
BOTTOM_RIGHT = chr(0x2518)
VERTICAL = chr(0x2502)
LEFT_JOIN = chr(0x251C)
RIGHT_JOIN = chr(0x2524)
CROSS = chr(0x253C)
BOTTOM_JOIN = chr(0x2534)
TOP_JOIN = chr(0x252C)


def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text)


def red(text):
    return colored(*RED, text)


def green(text):
    return colored(*GREEN, text)


def orange(text):
    return colored(*ORANGE, text)


def inbetween(start: str, in_between: str, end: str, horizontal_bar: str) -> str:
    row_str = f"{start}"
    for col in range(8):
        line = horizontal_bar
        line += in_between
        row_str += line
    row_str += horizontal_bar
    row_str += end
    return row_str