from Entity.WoodokuShape import WoodokuShape
from Entity.ScoreAgent import ScoreAgent
from typing import Dict, List, Tuple


class WoodokuBoardRepresentation:
    """A data class representing the low-level implementation of the board

    The top-left block's coordinate is (0, 0).
    The last block on the top row is (0, n - 1).
    The first block on the bottom row is (n - 1, 0).
    The bottom-right block's coordinate is (n - 1, n - 1).
    """
    def __init__(self):
        pass

    def __str__(self):
        pass

    def add_blocks(self, blocks_coord: List[Tuple[int, int]]) -> None:
        pass

    def remove_blocks(self, blocks_coord: List[Tuple[int, int]]) -> None:
        pass

    def is_occupied(self, blocks_coord: List[Tuple[int, int]]) -> bool:
        """Check if each coord has a block on it. If all of those coords are
        occupied, return true. Otherwise, false.

        Args:
            blocks_coord (List[Tuple[int, int]]): list or coordinates to check 

        Returns:
            bool: if any coordinates in `blocks_coord` is occupied
        """
        pass


class WoodokuBoard:
    """A 9x9 Woodoku Board

    Raises:
        CanNotAddShapeError: still cannot add shape after checking the board
    """
    __scoreAgent: ScoreAgent
    __representation: WoodokuBoardRepresentation

    def __init__(self):
        pass

    def __str__(self):
        pass

    def initialize(self):
        pass

    def can_add_shape_to_board(self, shape: WoodokuShape) -> bool:
        """Check if the woodoku shape can fit into the board. If all current
        shapes are not be able to add, the game fails.

        Args:
            shape (WoodokuShape): a woodoku shape for validation 

        Returns:
            bool: if the `shape` fits the board
        """
        pass


    def can_add_shape_at_location(self, shape: WoodokuShape, x: int, y: int) -> bool:
        """Check if the woodoku `shape` can be placed into the board at location
        `(x, y)` coordinates as the left upper corner of the shape.

        Args:
            shape (WoodokuShape): The shape needed to be checked
            x (int): x coordinate 
            y (int): y coordinate 

        Returns:
            bool: if `shape` can be added to `(x,y)`
        """
        pass

    def add_shape(self, shape: WoodokuShape, x: int, y: int) -> None:
        """Add the shape to woodoku at coordinate (x, y). Only called if the shape
        can be added. If unable to add, raise exception.

        This method includes actions:
        1. Clear winning row/column/3x3 block
        2. Call scoreAgent to calculate score

        Args:
            shape (WoodokuShape): The shape to be added
            x (int): x coordinate
            y (int): y coordinate
        """
        pass

    def get_score(self) -> int:
        pass

    def __find_winning_blocks(self) -> Dict[str, int]:
        """Check current board and see if there is any winning blocks such as
        complete rows, columns or 3x3 block.

        Returns:
            A dictionary mapping from name of the winning block to the number of
            winning block. e.g. { "row": 1, "column": 2, "3x3 block": 0 }
        """
        pass

    def __get_row_all_coords(self, row_num: int) -> List[Tuple[int, int]]:
        pass

    def __get_column_all_coords(self, column_num: int) -> List[Tuple[int, int]]:
        pass

    def __get_3x3_all_coords(self, index: int) -> List[Tuple[int, int]]:
        """The index of 3x3 block is as following:
        _____________
        | 0 | 1 | 2 |
        | 3 | 4 | 5 |
        | 6 | 7 | 8 |
        _____________

        Args:
            index (int): The index of 3x3 block as list above

        Returns:
            List[Tuple[int, int]]: All the coordinates in that 3x3 block
        """
        pass
