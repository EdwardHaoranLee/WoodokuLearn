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
        self.__coords = set(coords)

    def __eq__(self, other: any):
        if not isinstance(other, WoodokuShape):
            return False

        if len(other.__coords) != len(self.__coords):
            return False

        for coord in self.__coords:
            if coord not in other.__coords:
                return False

        return True

    def __hash__(self):
        hash('WoodokuShape Salt' + str(self.__coords))

    def get_coords(self) -> List[Tuple[int, int]]:
        return list(self.__coords)

    def map_to_board_at(self, x: int, y: int) -> List[Tuple[int, int]]:
        return [(x + row, y + col) for (row, col) in self.get_coords()]

    def rotate(self) -> WoodokuShape:
        """
        Rotate this shape by 90 degree clockwise.

        Returns: The rotated shape.

        """
        pass
