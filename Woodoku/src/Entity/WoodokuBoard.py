import numpy as np
from numpy import ndarray
from WoodokuShape import WoodokuShape
from ScoreAgent import ScoreAgent
from typing import Dict, List, Tuple

N = 9

class WoodokuBoardRepresentation:
    """
    The actual low-level implementation of the board. Data class.

    The top-left block's coordinate is (0, 0).
    The last block on the top row is (0, n - 1).
    The first block on the bottom row is (n - 1, 0).
    The bottom-right block's coordinate is (n - 1, n - 1).
    """
    board: ndarray

    def __init__(self):
        self.board = np.full((N, N), False)

    def __str__(self):
        pass

    def add_blocks(self, blocks_coord: List[Tuple[int, int]]) -> None:
        """
        Mark each position specified in blocks_coord as True to indicate that the position is occupied.

        :param blocks_coord: a list of (x,y) tuples to be added to the board
        :return:
        """
        for row, col in blocks_coord:
            self.board[row, col] = True

    def remove_blocks(self, blocks_coord: List[Tuple[int, int]]) -> None:
        """
        Mark each position specified in blocks_coord as False to indicate that the position is not occupied.

        :param blocks_coord: a list of (x,y) tuples to be added to the board
        :return:
        """
        for row, col in blocks_coord:
            self.board[row, col] = False

    def is_occupied(self, blocks_coord: List[Tuple[int, int]]) -> bool:
        """
        Check if each coord has block on it. If all of those coords are occupied, return true. Otherwise, false.

        :param blocks_coord:
        :return:
        """
        pass
        # will open a new pr to rewrite this method


class WoodokuBoard:
    __scoreAgent: ScoreAgent
    __representation: WoodokuBoardRepresentation

    def __init__(self):
        pass

    def __str__(self):
        pass

    def initialize(self):
        pass

    def can_add_shape_to_board(self, shape: WoodokuShape) -> bool:
        """
        Check if the woodoku shape can fit into the board. If all current shapes are not be able to add, the game fails.
        :return: if can fit.
        """
        pass

    def can_add_shape_at_location(self, shape: WoodokuShape, x: int, y: int) -> bool:
        """
        Check if the woodoku shape can be placed into the board at location (x, y) coordinates as the left upper corner
        of the shape.
        :param shape: the shape
        :param x: x coordinate
        :param y: y coordinate
        :return: if can be placed at location.
        """
        pass

    def add_shape(self, shape: WoodokuShape, x: int, y: int) -> None:
        """
        Add the shape to woodoku at coordinate (x, y). This method should be called after checking the addibility. If
        unable to add, raise exception.

        This method includes actions:
        1. Clear winning row/column/3x3 block
        2. Call scoreAgent to calculate score

        :param shape: The shape
        :param x: x coordinate
        :param y: y coordinate
        :return: none
        """
        pass

    def get_score(self) -> int:
        pass

    def __find_winning_blocks(self) -> Dict[str, int]:
        """
        Check current board and see if there is any winning blocks such as complete rows, columns or 3x3 block.
        :return: A dictionary mapping from name of the winning block to the number of winning block.
            e.g. { "row": 1, "column": 2, "3x3 block": 0 }
        """
        pass

    def __get_row_all_coords(self, row_num: int) -> List[Tuple[int, int]]:
        pass

    def __get_column_all_coords(self, column_num: int) -> List[Tuple[int, int]]:
        pass

    def __get_3x3_all_coords(self, index: int) -> List[Tuple[int, int]]:
        """
        The index of 3x3 block is as following:
        _____________
        | 0 | 1 | 2 |
        | 3 | 4 | 5 |
        | 6 | 7 | 8 |
        _____________

        :param index: the index as above
        :return: All the coords in this 3x3 block.
        """
        pass
