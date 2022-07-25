from typing import List, Tuple

from elements import *
from entity.woodoku_board import WoodokuBoard
from entity.woodoku_shape import WoodokuShape
from ui.ui_interface import UIInterface

NUM_SHAPES = 3


class CommandLineUI(UIInterface):

    def show_start_game(self, board: WoodokuBoard) -> None:
        print("\nWelcome to Wooduku")
        print(board)

    def show_board(self, board: WoodokuBoard) -> None:
        print(board)

    def choose_shape(self, shapes: List[WoodokuShape], shape_availability: List[bool]) -> int:
        shapes_str = ""
        for idx, avai in enumerate(shape_availability):
            if avai:
                shapes_str += f"{idx}.\n{str(shapes[idx]).rstrip()}\n\n"
        print(shapes_str)
        val = ""
        while not isinstance(val, int) or val not in range(NUM_SHAPES):
            val = input(f"Please choose one of the {orange('shapes')}:\n")
            try:
                val = int(val)
                if val not in range(NUM_SHAPES):
                    raise ValueError
            except ValueError:
                print(red("Please choose an integer value from 0 to 2. Try again"))
        return val

    def put_shape_at(self) -> Tuple[int, int]:
        confirmed = False
        while not confirmed:
            x = ""
            y = ""
            while not isinstance(x, int):
                try:
                    x = int(input(f"Enter a {orange('x coordinate')} on a 9X9 board:\n"))
                except ValueError:
                    print(red("Please enter an integer x coordinate. Try again\n"))
            while not isinstance(y, int):
                try:
                    y = int(input(f"Enter a {orange('y coordinate')} on a 9X9 board:\n"))
                except ValueError:
                    print(red("Please enter an integer y coordinate. Try again"))

            confirmed = input(f"Confirm your choice of position: x = {x}, y = {y}: (y/n)")
            while not isinstance(confirmed, bool):
                try:
                    confirmed = True if confirmed == 'y' else False
                    if not confirmed:
                        break
                except ValueError:
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
