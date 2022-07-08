from typing import List, Tuple


class WoodokuShape:
    __coords: List[Tuple[int, int]]

    def __init__(self, coords: List[Tuple[int, int]]):
        self.__coords = coords

    def get_coords(self) -> List[Tuple[int, int]]:
        return self.__coords
