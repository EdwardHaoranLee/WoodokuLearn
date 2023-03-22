from __future__ import annotations
from jaxtyping import Int, Float

import numpy as np


from woodoku import game
from woodoku.entity.woodoku_board import WoodokuBoard, BOARD_SIZE
from woodoku.entity.woodoku_shape import MAX_SHAPE_SIZE, WoodokuShape

OBSERBATION_N = BOARD_SIZE * BOARD_SIZE + MAX_SHAPE_SIZE * MAX_SHAPE_SIZE * 3 + 1


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
    shape: tuple[int] = (OBSERBATION_N,)

    def __init__(self, data: Float[np.ndarray, "OBSERBATION_N"]) -> None:
        self.data = data

    @staticmethod
    def from_game(board: WoodokuBoard, shapes: list[WoodokuShape]) -> Observation:
        """
        generate an observation from the game.
        """
        data: Float[np.ndarray, "OBSERBATION_N"] = np.zeros(OBSERBATION_N)
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

        Returns:

        """
        raise NotImplementedError


observation_space_d = Observation.shape
action_space_d = Action.shape


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
        self._woodoku_board = WoodokuBoard()
        self._all_shapes = game.read_shapes_from_file(game.CONFIG_FILE)
        self._shapes = game.random_shapes(self._all_shapes, game.NUM_SHAPES)
        self._availability = [True] * game.NUM_SHAPES

    def reset(self) -> tuple[Observation, bool, int]:
        """
        Reset the woodoku game env to initial Observation and return the initial Observation.
        """
        raise NotImplementedError

    def step(self, action: Action) -> tuple[Observation, int, bool]:
        """
        Take a step on current env with an action.
        Args:
            action: The action to take.

        Returns:
            A tuple of the Observation, reward (points earned) and whether the game is ended.
        """
        raise NotImplementedError

    def _observe(self) -> Observation:
        """
        Convert self to an observation.
        Returns:
            The observation.
        """
        raise NotImplementedError
