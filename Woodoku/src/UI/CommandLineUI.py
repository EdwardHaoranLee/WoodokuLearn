from abc import ABC
from typing import List

from Woodoku.src.Entity.WoodokuBoard import WoodokuBoard
from Woodoku.src.Entity.WoodokuShape import WoodokuShape
from Woodoku.src.UI.InterfaceUI import InterfaceUI


class CommandLineUI(ABC, InterfaceUI):

    def start_game(self, board: WoodokuBoard) -> None:
        pass

    def choose_shape(self, shapes: List[WoodokuShape], shape_availability: List[bool]) -> int:
        pass

    def show_board(self, board: WoodokuBoard) -> None:
        pass

    def show_result(self, board: WoodokuBoard, shapes: List[WoodokuShape], shape_availabilities: List[bool]) -> None:
        pass
