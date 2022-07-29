from typing import Callable, List, Tuple

from woodoku.ui.utils import get_input, red, orange
from woodoku.entity.woodoku_board import WoodokuBoard
from woodoku.entity.woodoku_shape import WoodokuShape
from woodoku.ui.ui_interface import UIInterface

NUM_SHAPES = 3


class CommandLineUI(UIInterface):
    def show_start_game(self, board: WoodokuBoard) -> None:
        print(orange("\nWelcome to Wooduku"))
        print(board)

    def show_board(self, board: WoodokuBoard) -> None:
        print(board)

    def choose_shape(
        self, shapes: List[WoodokuShape], shape_availability: List[bool]
    ) -> int:
        shapes_str = ""
        available_idx = []
        for i, available in enumerate(shape_availability):
            if available:
                shapes_str += f"{i}.\n{str(shapes[i]).rstrip()}\n\n"
                available_idx.append(i)
        print(shapes_str)
        val = get_input(
            int,
            available_idx,
            f"Please choose one of the {orange('shapes')}:\n",
            red(f"Please choose an integer value from {available_idx}. Try again"),
        )
        return val

    def put_shape_at(self) -> Tuple[int, int]:
        input_msg: Callable[[str], str] = lambda coord_name: (
            f"Enter a {orange(f'{coord_name} coordinate')} on a 9X9 board:"
        )
        again_msg: Callable[[str], str] = lambda coord_name: red(
            f"Please enter an integer {coord_name} coordinate. Try again"
        )
        while True:
            x = get_input(int, range(9), input_msg("x"), again_msg("x"))
            y = get_input(int, range(9), input_msg("y"), again_msg("y"))
            confirmation = input(
                f"Confirm your choice of position: x = {x}, y = {y}: (y/n)"
            )
            if confirmation.strip() == "y":
                break

            print(red("Please enter either y or n. Try again"))

        return x, y

    def show_earned(self, score: int) -> None:
        print(orange(f"\n\nYou earned {score}. Nice job\n"))

    def show_cannot_place(self) -> None:
        print(red("You are not able to place the shape at the position you chose\n"))

    def show_result(
        self,
        board: WoodokuBoard,
        shapes: List[WoodokuShape],
        shape_availabilities: List[bool],
    ) -> None:
        print(
            orange(
                """
             _____       ___       ___  ___   _____  
            /  ___|     /   |     /   |/   | |  ___| 
            | |        / /| |    / /|   /| | | |__   
            | |  _    / ___ |   / / |__/ | | |  __|  
            | |_| |  / /  | |  / /       | | | |___  
            \_____/ /_/   |_| /_/        |_| |_____|

             _____   _     _   _____   _____   
            /  _  \ | |   / / |  ___| |  _  \  
            | | | | | |  / /  | |__   | |_| |  
            | | | | | | / /   |  __|  |  _  /  
            | |_| | | |/ /    | |___  | | \ \  
            \_____/ |___/     |_____| |_|  \_\

            """
            )
        )
        self.show_board(board)
        print("You are left with the following shape(s):")
        shapes_str = ""
        for i, available in enumerate(shape_availabilities):
            if available:
                shapes_str += f"\n{str(shapes[i]).rstrip()}\n\n"
        print(shapes_str)
