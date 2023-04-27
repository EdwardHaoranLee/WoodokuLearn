from os import path

# Shape config file path
CONFIG_FILE = path.join(path.dirname(__file__), "config.yaml")

# Board config
BOARD_SIZE = 9
MAX_SHAPE_SIZE = 5
NUM_SHAPES = 3

# The number of points for each action.
GROUP_POINTS = 18
STREAK_POINTS = 10
COMBO_POINTS = 28
