from __future__ import annotations

from typing import List, Tuple, Set


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

    __coords: Set[Tuple[int, int]]

    def __init__(self, coords: List[Tuple[int, int]]):
        self.__coords = set(self.__standardize(coords))

    @staticmethod
    def __standardize(coords) -> Set[Tuple[int, int]]:
        """Pushes shape to top left corner if it has not done so

        Args:
            coords: the coordinates of the shape, cornered at top left or not.

        Returns:
            The adjusted, at-top-left-corner coordinates.
        """
        smallest_x = min(list(x for x, _ in coords))
        smallest_y = min(list(y for _, y in coords))
        return set(list((x - smallest_x, y - smallest_y) for x, y in coords))

    def get_coords(self) -> List[Tuple[int, int]]:
        return list(self.__coords)

    def map_to_board_at(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Maps the shape coordinates to map coordinates

        Args:
            x (int): The top left x coordinate of the shape on the board
            y (int): The top left y coordinate of the shape on the board

        Returns:
            List[Tuple[int, int]]: List of coordinates of shape on the board
        """
        return [(x + row, y + col) for (row, col) in self.get_coords()]

    def rotate(self) -> WoodokuShape:
        """
        Rotate this shape by 90 degree clockwise.

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

    def __eq__(self, other: any):
        if not isinstance(other, WoodokuShape):
            return False

        if len(other.get_coords()) != len(self.__coords):
            return False

        for coord in self.__coords:
            if coord not in other.get_coords():
                return False

        return True

    def __hash__(self):
        return hash("WoodokuShape Salt" + str(self.__coords))
