from os import path

# Shape config file path
CONFIG_FILE = path.join(path.dirname(__file__), "woodoku", "config.yaml")


# Board config
BOARD_SIZE = 9
MAX_SHAPE_SIZE = 5
NUM_SHAPES = 3

# The number of points for each action.
GROUP_POINTS = 18
STREAK_POINTS = 10
COMBO_POINTS = 28

OBSERVATION_N = BOARD_SIZE * BOARD_SIZE + MAX_SHAPE_SIZE * MAX_SHAPE_SIZE * 3 + 1

# reward config
REWARD_INVALID_SHAPE = -3
REWARD_INVALID_LOCATION = -5
