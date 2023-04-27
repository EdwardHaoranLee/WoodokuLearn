import random
import yaml
from config import NUM_SHAPES

from woodoku.entity.woodoku_board import WoodokuBoard
from woodoku.entity.woodoku_shape import WoodokuShape

# get the current absolute path to config.yaml at runtime


def _read_shapes_from_file(filepath: str) -> list[WoodokuShape]:
    raw_shapes = []
    with open(filepath, encoding="utf-8") as config:
        raw_shapes_list = yaml.safe_load(config)["raw_shapes"]
        for row in raw_shapes_list:
            tuple_row = [tuple(x) for x in row]
            raw_shapes.append(WoodokuShape(tuple_row))  # type: ignore[arg-type]
            # ignore mypy being confused about config.yml import data

    return raw_shapes


def _rotate_all_shapes(raw_shapes: list[WoodokuShape]) -> list[WoodokuShape]:
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


def get_all_shapes_from_file(config_path: str) -> list[WoodokuShape]:
    """
    rotate all shape to gather the entire set of shapes
    """

    return _rotate_all_shapes(_read_shapes_from_file(config_path))


def random_shapes(shapes: list[WoodokuShape], num: int) -> list[WoodokuShape]:
    """Choose `num` non-repeated random shapes from `shapes`.

    Args:
        shapes (list[WoodokuShape]): All shapes available to choose in the game
        num (int): Number of shapes to choose for this round

    Returns:
        list[WoodokuShape]: The shapes for this round.
    """
    return list(random.choices(shapes, k=num))


def is_out_of_space(board: WoodokuBoard, shapes: list[WoodokuShape], shape_availability: list[bool]) -> bool:
    for i, shape in enumerate(shapes):
        if shape_availability[i] and board.can_add_shape_to_board(shape):
            return False

    return True
