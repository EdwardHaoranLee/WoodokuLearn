from __future__ import annotations

from typing import Any, Iterable
from jaxtyping import Float
import numpy as np
from config import MAX_SHAPE_SIZE

from woodoku.ui.utils import BLOCK, green

ROW_PADDING = 10
BLOCK_PADDING = 3


class WoodokuShape:
    """A Woodoku shape to be place on the Woodoku board

    Example:
        === Markdown Form ===
        |       |  	 	| ■ 	|
        |---	|:---:	|---	|
        | ■ 	| ■ 	| ■ 	|

        OR

        === Text Form ===
                 ---
                | 0 |
         --- --- ---
        | 0 | 0 | 0 |
         --- --- ---

         This is represented by [(0,2), (1,0), (1,1), (1,2)]
         Note that (0,0) and (0,1) is not in the list
    """

    __coords: set[tuple[int, int]]

    def __init__(self, coords: list[tuple[int, int]]):
        self.__coords = set(self.__standardize(coords))

    def get_shape_data(self) -> Float[np.ndarray, "MAX_SHAPE_SIZE*MAX_SHAPE_SIZE"]:  # type: ignore[type-arg]
        """Returns the shape data of this shape

        Returns:
            Float[np.ndarray, "MAX_SHAPE_SIZE*MAX_SHAPE_SIZE"]: The shape data of this shape
        """
        shape_data = np.zeros((MAX_SHAPE_SIZE, MAX_SHAPE_SIZE))
        for x, y in self.__coords:
            shape_data[x][y] = 1.0

        return shape_data

    @staticmethod
    def __standardize(coords: Iterable[tuple[int, int]]) -> set[tuple[int, int]]:
        """Pushes shape to top left corner if it has not done so

        Args:
            coords: the coordinates of the shape, cornered at top left or not.

        Returns:
            The adjusted, at-top-left-corner coordinates.
        """
        smallest_x = min(list(x for x, _ in coords))
        smallest_y = min(list(y for _, y in coords))
        return set(list((x - smallest_x, y - smallest_y) for x, y in coords))

    def get_coords(self) -> list[tuple[int, int]]:
        return list(self.__coords)

    def map_to_board_at(self, x: int, y: int) -> list[tuple[int, int]]:
        """Maps the shape coordinates to map coordinates

        Args:
            x (int): The top left x coordinate of the shape on the board
            y (int): The top left y coordinate of the shape on the board

        Returns:
            list[tuple[int, int]]: list of coordinates of shape on the board
        """
        return [(x + row, y + col) for (row, col) in self.get_coords()]

    def rotate(self) -> WoodokuShape:
        """
        Rotate this shape by 90 degree counter-clockwise.

        Returns: The rotated shape.

        """
        boarder_size = max(list(sum(self.__coords, ())))

        new_coords = [(boarder_size - y, x) for x, y in self.__coords]

        return WoodokuShape(new_coords)

    def __len__(self) -> int:
        """Return the size of this shape

        Returns:
            int: The size of this shape
        """
        return len(self.__coords)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, WoodokuShape):
            return False

        if len(other.get_coords()) != len(self.__coords):
            return False

        for coord in self.__coords:
            if coord not in other.get_coords():
                return False

        return True

    def __hash__(self) -> int:
        return hash("WoodokuShape Salt" + str(self.__coords))

    def __str__(self) -> str:
        """each block in a WoodokuShape is drawn drawn using box-drawing characters
        https://www.unicode.org/charts/PDF/U2500.pdf
        """
        result = ""
        # by observation, each shape is at most 5 blocks height or 5 blocks long
        for row in range(MAX_SHAPE_SIZE):
            row_str = ""
            for col in range(MAX_SHAPE_SIZE):
                if (row, col) in self.__coords:
                    row_str += f"{green(BLOCK)}" + " " * (BLOCK_PADDING - 1)
                else:
                    row_str += " " * (BLOCK_PADDING)
            result += row_str + " " * ROW_PADDING + "\n"
        return result
