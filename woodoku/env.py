from __future__ import annotations
from jaxtyping import Int, Float

import numpy as np

from config import BOARD_SIZE, CONFIG_FILE, MAX_SHAPE_SIZE, NUM_SHAPES, OBSERVATION_N
from woodoku.entity.woodoku_board import WoodokuBoard
from woodoku.entity.woodoku_shape import WoodokuShape
from woodoku.utils import get_all_shapes_from_file, is_out_of_space, random_shapes


class Observation:
    """
    The class representing the of the game.

    The Observation space is a 1D array that has the following length. One board representation, three shapes to
    choose from and one integer representing the number of streaks.

    The board representation part will be integer 0 or 1 indicating whether that block is occupied. Each shape will also
    be 0 or 1 and will reflect the actual shape, and will be totally empty if is not available to choose. Last integer
    will simply be the number of streaks so far.
    """

    # size is (157, )
    shape: tuple[int] = (OBSERVATION_N,)

    def __init__(self, data: Float[np.ndarray, "OBSERVATION_N"]) -> None:
        self.data = data

    @staticmethod
    def from_game(board: WoodokuBoard, shapes: list[WoodokuShape]) -> Observation:
        """
        generate an observation from the game.
        """
        data: Float[np.ndarray, "OBSERVATION_N"] = np.zeros(OBSERVATION_N)

        data[: BOARD_SIZE * BOARD_SIZE] = board.get_board_data()
        for i, shape in enumerate(shapes):
            data[
                BOARD_SIZE * BOARD_SIZE
                + i * MAX_SHAPE_SIZE * MAX_SHAPE_SIZE : BOARD_SIZE * BOARD_SIZE
                + (i + 1) * MAX_SHAPE_SIZE * MAX_SHAPE_SIZE
            ] = shape.get_shape_data()

        data[-1] = board.get_streak()
        return Observation(data)


class Action:
    """
    The class representing the action. (wrapper around numpy NDarray)

    The first dimension is integer between 0 and 2, inclusive, representing which shape to choose. The second and the
    third dimensions are both integer between 0 and 8, inclusive, representing the x, y coordinates to place.
    """

    shape: tuple[int] = (3,)
    space: tuple[tuple[int, int], tuple[int, int], tuple[int, int]] = (
        (0, 3),
        (0, 9),
        (0, 9),
    )

    # TODO: add jax typing
    def __init__(self, data: Int[np.ndarray, "3"]) -> None:
        self.data = data

    @staticmethod
    def random_action() -> Action:
        """
        Generate a random action within the possible action space.

        Returns: a random action.
        """
        shape_choice = np.random.randint(0, 3)
        x_coord = np.random.randint(0, 9)
        y_coord = np.random.randint(0, 9)

        return Action(np.array([shape_choice, x_coord, y_coord]))


observation_space_d = Observation.shape
action_space_d = Action.shape


# TODO: add documentation for reward function
class WoodokuGameEnv:
    """
    A woodoku game environment.

    The environment is a wrapper around the WoodokuGame class. It provides the interface for the agent to interact with
    the game.
    """

    _woodoku_board: WoodokuBoard
    _all_shapes: list[WoodokuShape]
    _shapes: list[WoodokuShape]
    _availability: list[bool]

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> Observation:
        """
        Reset the woodoku game env to initial Observation and return the initial Observation.
        """
        self._woodoku_board = WoodokuBoard()
        self._all_shapes = get_all_shapes_from_file(CONFIG_FILE)
        self._shapes = random_shapes(self._all_shapes, NUM_SHAPES)
        self._availability = [True] * NUM_SHAPES
        self._available_count = NUM_SHAPES
        self._cur_score = 0

        return self._observe()

    def step(self, action: Action) -> tuple[Observation, int, bool]:
        """
        Take a step on current env with an action.
        Args:
            action: The action to take.

        Returns:
            A tuple of the Observation, reward (points earned) and whether the game is ended.
        """

        # Check if the game has already ended
        # When there is still available shapes in this round waiting to be placed
        if is_out_of_space(self._woodoku_board, self._shapes, self._availability):
            return (
                self._observe(),
                0,
                True,
            )  # TODO: possibly need to tune the reward as negative reward

        shape_choice, x, y = action.data[0], action.data[1], action.data[2]

        # penalize action choosing an unavailable shape
        if not self._availability[shape_choice]:
            return self._observe(), -5, True

        # penalize action for choosing an occupied location
        if not self._woodoku_board.can_add_shape_at_location(self._shapes[shape_choice], x, y):
            return self._observe(), -5, True

        self._woodoku_board.add_shape(self._shapes[shape_choice], x, y)
        self._availability[shape_choice] = False
        self._available_count -= 1

        reward = self._get_score_gain()
        self._cur_score = self._woodoku_board.get_score()

        # if all shapes are used up, reset the shapes for the next round
        if self._available_count == 0:
            self._shapes = random_shapes(self._all_shapes, NUM_SHAPES)
            self._availability = [True] * NUM_SHAPES
            self._available_count = NUM_SHAPES

        return self._observe(), reward, False

    def _get_score_gain(self) -> int:
        """
        Get the score gain from the current action.

        Returns:
            The score gain.
        """
        return self._woodoku_board.get_score() - self._cur_score

    def _observe(self) -> Observation:
        """
        Convert self to an observation.
        Returns:
            The observation.
        """
        return Observation.from_game(self._woodoku_board, self._shapes)
