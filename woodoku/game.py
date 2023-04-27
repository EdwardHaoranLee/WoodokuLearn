from os import _exit as os_exit, path
from sys import exit as sys_exit
from config import CONFIG_FILE, NUM_SHAPES

from woodoku.entity.woodoku_board import WoodokuBoard
from woodoku.ui.command_line_ui import CommandLineUI
from woodoku.ui.ui_interface import UIInterface
from woodoku.utils import get_all_shapes_from_file, is_out_of_space, random_shapes

# get the current absolute path to config.yaml at runtime


def game(ui: UIInterface) -> None:
    try:
        board = WoodokuBoard()

        # Generating all possible shapes that might appear in game.
        all_shapes = get_all_shapes_from_file(CONFIG_FILE)

        ui.show_start_game(board)

        score = 0

        while True:
            # Select NUM_SHAPES shapes from all possible shapes.
            shapes = random_shapes(all_shapes, NUM_SHAPES)

            # All selected shapes are available to be chosen.
            shape_availability = [True] * NUM_SHAPES

            # When there is any shape in this round still waiting to be chosen.
            while any(shape_availability):
                if is_out_of_space(board, shapes, shape_availability):
                    ui.show_result(board, shapes, shape_availability)
                    return

                ui.show_board(board)

                # Let user choose shape.
                shape_index = ui.choose_shape(shapes, shape_availability)

                # Let user place at location.
                x, y = ui.put_shape_at()

                # Check if the chosen shape can be placed at location.
                if board.can_add_shape_at_location(shapes[shape_index], x, y):
                    shape_availability[shape_index] = False

                    board.add_shape(shapes[shape_index], x, y)

                    new_score = board.get_score()
                    ui.show_earned(new_score - score)
                    score = new_score

                else:
                    ui.show_cannot_place()
    except KeyboardInterrupt:
        ui.show_result(board, shapes, shape_availability)
        try:
            sys_exit(1)
        except SystemExit:
            os_exit(1)


if __name__ == "__main__":
    game(CommandLineUI())
