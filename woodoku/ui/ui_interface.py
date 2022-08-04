from abc import ABC, abstractmethod
from typing import List, Tuple

from woodoku.entity.woodoku_board import WoodokuBoard
from woodoku.entity.woodoku_shape import WoodokuShape


class UIInterface(ABC):
    @abstractmethod
    def show_start_game(self, board: WoodokuBoard) -> None:
        raise NotImplementedError()

    @abstractmethod
    def show_board(self, board: WoodokuBoard) -> None:
        """Show the board and score to user.

        Args:
            board (WoodokuBoard): The board
        """
        raise NotImplementedError()

    @abstractmethod
    def choose_shape(
        self, shapes: List[WoodokuShape], shape_availabilities: List[bool]
    ) -> int:
        """Show the UI to let user choose one of the shapes.

        Precondition: len(shapes) == len(shape_availabilities)

        Args:
            shapes (List[WoodokuShape]): All the shapes in this round, no matter if chosen before.
            shape_availabilities (List[bool]): List of bool representing if the shape in is still waiting to be chosen

        Returns:
            int: The index of shape chosen by the user.
        """
        raise NotImplementedError()

    @abstractmethod
    def put_shape_at(self) -> Tuple[int, int]:
        """
        Get the coords from user on where to put shape.

        Returns:
            int: (x, y) coordinates.
        """
        raise NotImplementedError()

    @abstractmethod
    def show_earned(self, score: int) -> None:
        """Show user the earned score after a successful placement.

        Args:
            score (int): The change in score
        """
        raise NotImplementedError()

    @abstractmethod
    def show_cannot_place(self) -> None:
        """
        If the current shape cannot be placed at user-inputted location, call this method.
        """
        raise NotImplementedError()

    @abstractmethod
    def show_result(
        self,
        board: WoodokuBoard,
        shapes: List[WoodokuShape],
        shape_availabilities: List[bool],
    ) -> None:
        """Show the final result to the user.

        Precondition: len(shapes) == len(shape_availabilities)

        Args:
            board (WoodokuBoard): The board
            shapes (List[WoodokuShape]): All the shapes in this round, no matter if chosen before.
            shape_availabilities (List[bool]): If the shape in <shapes> is still waiting to be chosen.
        """
        raise NotImplementedError()
