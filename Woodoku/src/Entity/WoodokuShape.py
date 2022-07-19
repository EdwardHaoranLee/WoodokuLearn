from __future__ import annotations

from typing import List, Tuple, Set


class WoodokuShape:
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

    def rotate(self) -> WoodokuShape:
        """
        Rotate this shape by 90 degree clockwise.

        Returns: The rotated shape.

        """
        pass
