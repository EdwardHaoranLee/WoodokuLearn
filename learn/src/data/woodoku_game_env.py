from __future__ import annotations

from typing import Tuple, List
import torch

from woodoku import game
from woodoku.entity.woodoku_board import WoodokuBoard, BOARD_SIZE
from woodoku.entity.woodoku_shape import MAX_SHAPE_SIZE, WoodokuShape


class Observation:
    """
    The class representing the observation.

    The observation space is a 1D tensor that has the following length. One board representation and three shapes to
    choose from.

    The board representation part will be integer 0 or 1 indicating whether that block is occupied. Each shape will also
    be 0 or 1 and will reflect the actual shape, and will be totally empty if is not available to choose.
    """

    dimension: Tuple[int] = (
        BOARD_SIZE * BOARD_SIZE + MAX_SHAPE_SIZE * MAX_SHAPE_SIZE * 3,
    )
    data: torch.Tensor

    def __init__(self) -> None:
        self.data = torch.zeros(self.dimension)

    def from_game(self, board: WoodokuBoard, shapes: List[WoodokuShape]) -> None:
        """
        Update self.data based on the woodoku board and the shapes.

        Args:
            board: The Woodoku Board.
            shapes: The shapes to choose.
        """
        pass


class Action:
    """
    The class representing the action.

    The first dimension is integer between 0 and 2, inclusive, representing which shape to choose. The second and the
    third dimensions are both integer between 0 and 8, inclusive, representing the x, y coordinates to place.
    """

    dimension: Tuple[int] = (3,)
    range: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]] = (
        (0, 3),
        (0, 9),
        (0, 9),
    )
    data: Tuple[int, int, int]

    @staticmethod
    def random_action() -> Action:
        """
        Generate a random action within the range.

        Returns:

        """
        pass


class WoodokuGameEnv:
    _woodoku_board: WoodokuBoard
    _all_shapes: List[WoodokuShape]
    _shapes: List[WoodokuShape]
    _availability: List[bool]

    def __init__(self) -> None:
        self._woodoku_board = WoodokuBoard()
        self._all_shapes = game.read_shapes_from_file(game.CONFIG_FILE)
        self._shapes = game.random_shapes(self._all_shapes, game.NUM_SHAPES)
        self._availability = [True] * game.NUM_SHAPES

    def reset(self) -> None:
        """
        Reset the woodoku game env to initial state.
        """
        pass

    def step(self, action: Action) -> Tuple[Observation, int, bool]:
        """
        Take a step on current env with an action.
        Args:
            action: The action to take.

        Returns:
            A tuple of the state (observation), reward (points earned) and whether the game is ended.
        """
        pass

    @staticmethod
    def observation_space_d() -> Tuple[int, ...]:
        return Observation.dimension

    @staticmethod
    def action_space_d() -> Tuple[int, ...]:
        return Action.dimension

    def _observe(self) -> Observation:
        """
        Convert self to an observation.
        Returns:
            The observation.
        """
        pass
