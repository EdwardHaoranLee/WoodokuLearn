from typing import List, Tuple

from ui.utils import *
from entity.woodoku_board import WoodokuBoard
from entity.woodoku_shape import WoodokuShape
from ui.ui_interface import UIInterface

NUM_SHAPES = 3


class CommandLineUI(UIInterface):

    def show_start_game(self, board: WoodokuBoard) -> None:
        print(orange("\nWelcome to Wooduku"))
        print(board)

    def show_board(self, board: WoodokuBoard) -> None:
        print(board)

    def choose_shape(self, shapes: List[WoodokuShape], shape_availability: List[bool]) -> int:
        shapes_str = ""
        for i, available in enumerate(shape_availability):
            if available:
                shapes_str += f"{i}.\n{str(shapes[i]).rstrip()}\n\n"
        print(shapes_str)
        val = get_input(int, range(2), f"Please choose one of the {orange('shapes')}:\n",
                        red("Please choose an integer value from 0 to 2. Try again"))
        return val

    def put_shape_at(self) -> Tuple[int, int]:
        confirmed = ''
        while confirmed != 'y':
            x = get_input(int, range(9), f"Enter a {orange('x coordinate')} on a 9X9 board:\n",
                          red("Please enter an integer x coordinate. Try again\n"))
            y = get_input(int, range(9), f"Enter a {orange('y coordinate')} on a 9X9 board:\n",
                          red("Please enter an integer y coordinate. Try again"))
            confirmed = input(f"Confirm your choice of position: x = {x}, y = {y}: (y/n)")
            if confirmed.strip() != 'y':
                print(red("Please enter either y or n. Try again"))
        return x, y

    def show_earned(self, score: int) -> None:
        print(orange(f"\n\nYou earned {score}. Nice job\n"))

    def show_cannot_place(self) -> None:
        print(red("You are not able to place the shape at the position you chose\n"))

    def show_result(self, board: WoodokuBoard, shapes: List[WoodokuShape], shape_availabilities: List[bool]) -> None:
        print(
            orange("""
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

            """)
        )
        self.show_board(board)
