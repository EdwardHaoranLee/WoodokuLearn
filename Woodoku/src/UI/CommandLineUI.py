from typing import List, Tuple

from Entity.WoodokuBoard import WoodokuBoard
from Entity.WoodokuShape import WoodokuShape
from UI.UIInterface import UIInterface


class CommandLineUI(UIInterface):

    def show_start_game(self, board: WoodokuBoard) -> None:
        pass

    def show_board(self, board: WoodokuBoard) -> None:
        pass

    def choose_shape(self, shapes: List[WoodokuShape], shape_availability: List[bool]) -> int:
        pass

    def put_shape_at(self) -> Tuple[int, int]:
        pass

    def show_earned(self, score: int) -> None:
        pass

    def show_cannot_place(self) -> None:
        pass

    def show_result(self, board: WoodokuBoard, shapes: List[WoodokuShape], shape_availabilities: List[bool]) -> None:
        pass
