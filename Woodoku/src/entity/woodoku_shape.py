from typing import List, Tuple


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
    __coords: List[Tuple[int, int]]

    def __init__(self, coords: List[Tuple[int, int]]):
        self.__coords = coords

    def get_coords(self) -> List[Tuple[int, int]]:
        return self.__coords

    def map_to_board_at(self, x: int, y: int) -> List[Tuple[int, int]]:
        return [(x + row, y + col) for (row, col) in self.get_coords()]
