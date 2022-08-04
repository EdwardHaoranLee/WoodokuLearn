import random
from os import _exit as os_exit, path
from sys import exit as sys_exit
from typing import List

import yaml

from woodoku.entity.woodoku_board import WoodokuBoard
from woodoku.entity.woodoku_shape import WoodokuShape
from woodoku.ui.command_line_ui import CommandLineUI
from woodoku.ui.ui_interface import UIInterface

# get the current absolute path to config.yaml at runtime
CONFIG_FILE = path.join(path.dirname(__file__), "config.yaml")
NUM_SHAPES = 3


def read_shapes_from_file(filepath: str) -> List[WoodokuShape]:
    raw_shapes = []
    with open(filepath, encoding="utf-8") as config:
        raw_shapes_list = yaml.safe_load(config)["raw_shapes"]
        for row in raw_shapes_list:
            tuple_row = [tuple(x) for x in row]
            raw_shapes.append(WoodokuShape(tuple_row))  # type: ignore[arg-type]
            # ignore mypy being confused about config.yml import data

    return raw_shapes


def rotate_all_shapes(raw_shapes: List[WoodokuShape]) -> List[WoodokuShape]:
    """
    Rotate each shape in <raw_shapes> for three times, then gather all of them.

    Args:
        raw_shapes: The default shape without any rotation.

    Returns:
        The original shapes and all the rotated shapes (non-repeated).
    """
    shapes = set()

    # All the raw shape itself was added first, then rotates three times and add to set after each rotate.
    # Duplicates are eliminated by set operation.
    for shape in raw_shapes:
        shapes.add(shape)
        new_shape = shape
        for _ in range(NUM_SHAPES):
            new_shape = new_shape.rotate()
            shapes.add(new_shape)

    return list(shapes)


def random_shapes(shapes: List[WoodokuShape], num: int) -> List[WoodokuShape]:
    """Choose `num` non-repeated random shapes from `shapes`.

    Args:
        shapes (List[WoodokuShape]): All shapes available to choose in the game
        num (int): Number of shapes to choose for this round

    Returns:
        List[WoodokuShape]: The shapes for this round.
    """
    return list(random.choices(shapes, k=num))


def is_out_of_space(
    board: WoodokuBoard, shapes: List[WoodokuShape], shape_availability: List[bool]
) -> bool:
    for i, shape in enumerate(shapes):
        if shape_availability[i] and board.can_add_shape_to_board(shape):
            return False

    return True


def game(ui: UIInterface) -> None:
    try:
        board = WoodokuBoard()

        # Generating all possible shapes that might appear in game.
        all_shapes = rotate_all_shapes(read_shapes_from_file(CONFIG_FILE))

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
