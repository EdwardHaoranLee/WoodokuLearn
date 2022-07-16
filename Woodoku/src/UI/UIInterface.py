from abc import ABC, abstractmethod
from typing import List, Tuple

from Entity.WoodokuBoard import WoodokuBoard
from Entity.WoodokuShape import WoodokuShape


class UIInterface(ABC):

    @abstractmethod
    def show_start_game(self, board) -> None:
        raise NotImplementedError()

    @abstractmethod
    def show_board(self, board: WoodokuBoard) -> None:
        """
        Show the board and score to user.

        :param board: The board
        """
        raise NotImplementedError()

    @abstractmethod
    def choose_shape(self, shapes: List[WoodokuShape], shape_availability: List[bool]) -> int:
        """
        Precondition: len(shapes) == len(shape_availability)

        Show the UI to let user choose one of the shapes.

        :param shapes: All the shapes in this round, no matter if chosen before.
        :param shape_availability: List of bool representing if the shape in is still waiting to be chosen
        :return: The index of shape chosen by the user.
        """
        raise NotImplementedError()

    @abstractmethod
    def put_shape_at(self) -> Tuple[int, int]:
        """
        Get the coords from user on where to put shape.

        :return: (x, y) coordinates.
        """
        raise NotImplementedError()

    @abstractmethod
    def show_earned(self, score: int) -> None:
        """
        Show user the earned score after a successful placement.

        :param score: The change in score.
        """
        raise NotImplementedError()

    @abstractmethod
    def show_cannot_place(self) -> None:
        """
        If the current shape cannot be placed at user-inputted location, call this method.
        """
        raise NotImplementedError()

    @abstractmethod
    def show_result(self, board: WoodokuBoard, shapes: List[WoodokuShape], shape_availabilities: List[bool]) -> None:
        """
        Precondition: len(shapes) == len(shape_availability)

        Show the final result to the user.

        :param board: The board
        :param shapes: All the shapes in this round, no matter if chosen before.
        :param shape_availabilities: If the shape in <shapes> is still waiting to be chosen.
        """
        raise NotImplementedError()
