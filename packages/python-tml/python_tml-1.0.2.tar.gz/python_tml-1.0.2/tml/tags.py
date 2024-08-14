foreground = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
    "bright-black": 90,
    "light-black": 90,
    "bright-red": 91,
    "light-red": 91,
    "bright-green": 92,
    "light-green": 92,
    "bright-yellow": 93,
    "light-yellow": 93,
    "bright-blue": 94,
    "light-blue": 94,
    "bright-magenta": 95,
    "light-magenta": 95,
    "bright-cyan": 96,
    "light-cyan": 96,
    "bright-white": 97,
    "light-white": 97,
}

background = {
    "on-black": 40,
    "on-red": 41,
    "on-green": 42,
    "on-yellow": 43,
    "on-blue": 44,
    "on-magenta": 45,
    "on-cyan": 46,
    "on-white": 47,
    "on-bright-black": 100,
    "on-light-black": 100,
    "on-bright-red": 101,
    "on-light-red": 101,
    "on-bright-green": 102,
    "on-light-green": 102,
    "on-bright-yellow": 103,
    "on-light-yellow": 103,
    "on-bright-blue": 104,
    "on-light-blue": 104,
    "on-bright-magenta": 105,
    "on-light-magenta": 105,
    "on-bright-cyan": 106,
    "on-light-cyan": 106,
}

attributes = {
    "bold": 1,
    "b": 1,
    "dark": 2,
    "italic": 3,
    "i": 3,
    "underline": 4,
    "u": 4,
    "blink": 5,
    "reverse": 7,
    "concealed": 8,
    "strike": 9,
}


def is_foreground(tag: str) -> bool:
    return tag in foreground


def is_background(tag: str) -> bool:
    return tag in background


def is_attribute(tag: str) -> bool:
    return tag in attributes
