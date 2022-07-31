from time import sleep
from typing import Callable, List, Tuple

from art import text2art
from woodoku.entity.woodoku_board import BOARD_SIZE, WoodokuBoard
from woodoku.entity.woodoku_shape import (
    BLOCK_PADDING,
    MAX_SHAPE_SIZE,
    ROW_PADDING,
    WoodokuShape,
)
from woodoku.ui.ui_interface import UIInterface
from woodoku.ui.utils import get_input, orange, red

NUM_SHAPES = 3


class CommandLineUI(UIInterface):
    def show_start_game(self, board: WoodokuBoard) -> None:
        print(orange(text2art("Woodoku!", "3d_diagonal")))

    def show_board(self, board: WoodokuBoard) -> None:
        print(board)

    def choose_shape(
        self, shapes: List[WoodokuShape], shape_availabilities: List[bool]
    ) -> int:
        assert len(shapes) == len(shape_availabilities), "Precondition violated"
        self.__show_available_shapes(shapes, shape_availabilities)

        available_indices = [
            i for i, available in enumerate(shape_availabilities) if available
        ]
        val = get_input(
            int,
            available_indices,
            f"Please choose one of the {orange('shapes')}:\n",
            red(f"Please choose an integer value from {available_indices}. Try again"),
        )
        return val

    def put_shape_at(self) -> Tuple[int, int]:
        input_msg: Callable[[str], str] = lambda coord_name: (
            f"Enter a {orange(f'{coord_name} coordinate')} on a 9X9 board:\n"
        )
        again_msg: Callable[[str], str] = lambda coord_name: red(
            f"Please enter an integer {coord_name} coordinate. Try again\n"
        )
        while True:
            x = get_input(int, range(BOARD_SIZE), input_msg("x"), again_msg("x"))
            y = get_input(int, range(BOARD_SIZE), input_msg("y"), again_msg("y"))
            confirmation = get_input(
                str,
                ["y", "n", "", "yes", "no"],
                f"Confirm your choice of position: x = {x}, y = {y}: (Enter/y/n)\n",
                red("Please enter either y or n. Try again"),
            )
            if confirmation in ["", "y", "yes"]:
                break

        return x, y

    def show_earned(self, score: int) -> None:
        print(f"\n\nYou scored {orange(str(score))}. Nice!\n")

    def show_cannot_place(self) -> None:
        print(red("\n❌ You cannot place the shape at the position you chose\n"))

    def show_result(
        self,
        board: WoodokuBoard,
        shapes: List[WoodokuShape],
        shape_availabilities: List[bool],
    ) -> None:
        assert len(shapes) == len(shape_availabilities), "Precondition violated"
        print()
        print(orange(text2art("Game\nOver", "rnd-xlarge")))
        sleep(2)

        self.show_board(board)
        print("You are left with the following shape(s):\n")
        self.__show_available_shapes(shapes, shape_availabilities)

    def __show_available_shapes(
        self, shapes: List[WoodokuShape], shape_availabilities: List[bool]
    ) -> None:
        """Helper to show the shape ui horizontally

        Args:
            shapes (List[WoodokuShape]): Shapes for this round
            shape_availabilities (List[bool]): Availability for these shapes
        """
        shape_str_lst = []
        for i, available in enumerate(shape_availabilities):
            if available:
                shape_str = (
                    f"{i}.".ljust(BLOCK_PADDING * MAX_SHAPE_SIZE + ROW_PADDING) + "\n"
                )
                shape_str += f"{str(shapes[i])}"
                # store the shape string split by rows
                shape_str_lst.append(shape_str[:-1].split("\n"))

        # use zip to repackage shapes and access the row parts for each shape
        for shapes_row in zip(*shape_str_lst):
            for shape_part in shapes_row:
                print(shape_part, end="")
            print()
