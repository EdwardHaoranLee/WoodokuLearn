import numpy as np
from numpy import ndarray
from entity.woodoku_shape import WoodokuShape
from entity.score_agent import ScoreAgent
from typing import Dict, List, Tuple, Set
from exceptions.exceptions import ShapeOutOfBoardError

# the length of the square game board
N = 9


class _WoodokuBoardRepresentation:
    """Private data class representing the low-level implementation of the board

    The top-left block's coordinate is (0, 0).
    The last block on the top row is (0, n - 1).
    The first block on the bottom row is (n - 1, 0).
    The bottom-right block's coordinate is (n - 1, n - 1).

    _board: an 2d array to record the occupancy of each position on the game board. The value is set to True when
    the position occupied
    """
    __board: ndarray

    def __init__(self):
        self.__board = np.full((N, N), False)

    def board(self):
        return self.__board

    def add_blocks(self, blocks_coord: List[Tuple[int, int]]) -> None:
        """
        Mark each position specified in blocks_coord as True to indicate that the position is occupied.

        :param blocks_coord: a list of (x,y) tuples to be added to the board
        :return:
        """
        for row, col in blocks_coord:
            self.__board[row, col] = True

    def remove_blocks(self, blocks_coord: List[Tuple[int, int]]) -> None:
        """
        Mark each position specified in blocks_coord as False to indicate that the position is not occupied.

        :param blocks_coord: a list of (x,y) tuples to be added to the board
        :return:
        """
        for row, col in blocks_coord:
            self.__board[row, col] = False

    def is_occupied(self, blocks_coord: List[Tuple[int, int]]) -> bool:
        """Check if each block has is occupied. If all of those blocks are
        occupied, return true. Otherwise, false.

        Args:
            blocks_coord (List[Tuple[int, int]]): list of blocks to check

        Returns:
            bool: if all blocks in `blocks_coord` is occupied
        """
        for row, col in blocks_coord:
            if not self.__board[row, col]:
                return False
        return True

    def is_not_occupied(self, blocks_coord: List[Tuple[int, int]]) -> bool:
        """Check if each block is empty. If all of those blocks are empty,
        return true. Otherwise, false.

        Args:
            blocks_coord (List[Tuple[int, int]]): list of blocks to check

        Returns:
            bool: if all blocks in `blocks_coord` is empty
        """
        for row, col in blocks_coord:
            if self.__board[row, col]:
                return False
        return True

    def __validate(block: Tuple[int, int]) -> None:
        """validate if block is within the 9x9 board. raise Error if not.

        Args:
            block (Tuple[int, int]): The block to be validated

        Raises:
            ShapeOutOfBoardError: when some block is not valid 
        """
        x, y = block
        if not (0 <= x <= N - 1 and 0 <= y <= N - 1):
            raise ShapeOutOfBoardError(x, y)

    def __str__(self) -> str:
        raise NotImplementedError()


class WoodokuBoard:
    """A 9x9 Woodoku Board"""

    __scoreAgent: ScoreAgent
    __representation: _WoodokuBoardRepresentation

    def __init__(self):
        self.__scoreAgent = ScoreAgent()
        self.__representation = _WoodokuBoardRepresentation()

    def can_add_shape_to_board(self, shape: WoodokuShape) -> bool:
        """Check if the woodoku shape can fit into the board. If all current
        shapes are not be able to add, the game fails.

        scans the board in a random fashion to average the complexity

        Args:
            shape (WoodokuShape): a woodoku shape for validation

        Returns:
            bool: if the `shape` fits the board
        """
        rng = np.random.default_rng()
        all_blocks = [(i, j) for i in range(9) for j in range(9)]
        rng.shuffle(all_blocks)

        for row, col in all_blocks:
            if self.can_add_shape_at_location(shape, x=row, y=col):
                return True

        return False

    def can_add_shape_at_location(self, shape: WoodokuShape, x: int, y: int) -> bool:
        """Check if the woodoku `shape` can be placed into the board at location
        `(x, y)` coordinates as the left upper corner of the shape.

        Args:
            shape (WoodokuShape): The shape needed to be checked
            x (int): x coordinate
            y (int): y coordinate
        Raises: 
            ShapeOutOfBoundError: if any block in `blocks` is invalid

        Returns:
            bool: if `shape` can be added to `(x,y)`
        """
        blocks = shape.map_to_board_at(x, y)
        return self.__representation.is_not_occupied(blocks)

    def add_shape(self, shape: WoodokuShape, x: int, y: int) -> None:
        """Add the shape to woodoku at coordinate (x, y). Only called if the shape
        can be added at `(x,y)`.

        This method includes actions:
        1. Clear winning row/column/3x3 box
        2. Call scoreAgent to calculate score

        Args:
            shape (WoodokuShape): The shape to be added
            x (int): x coordinate
            y (int): y coordinate
        """
        # add shape to block
        shape_blocks = shape.map_to_board_at(x, y)
        self.__representation.add_blocks(shape_blocks)

        # determine groups and clear the groups
        group_info, group_blocks = self.__find_groups()
        self.__scoreAgent.calculate_winning(group_info)
        self.__representation.remove_blocks(group_blocks)

    def get_score(self) -> int:
        return self.__scoreAgent.get_score()

    def __find_groups(self) -> Tuple[Dict[str, int], Set[Tuple[int, int]]]:
        """Check current board and see if there is any groups such as
        complete rows, columns or 3x3 box and report them. 

        Terminology Reference:
        [Wikipedia Sudoku Glossary](https://en.wikipedia.org/wiki/Glossary_of_Sudoku#Terminology_and_grid_layout)

        Returns:
            Tuple[Dict[str, int], Set[Tuple[int,int]]]:
                1. A dictionary mapping from name of the group to the number of groups.
                e.g. { "row": 1, "column": 2, "box": 0 }
                2. Set of block coordinates for the group

        """
        info = {"row": 0, "column": 0, "box": 0}
        rep = self.__representation
        group_blocks = set()  # use set to handle overlapping group removal
        for index in range(9):
            row_blocks = self.__get_row_coords(index)
            col_blocks = self.__get_col_coords(index)
            box_blocks = self.__get_box_coords(index)

            if rep.is_occupied(row_blocks):
                info["row"] += 1
                group_blocks.update(row_blocks)

            if rep.is_occupied(col_blocks):
                info["column"] += 1
                group_blocks.update(col_blocks)

            if rep.is_occupied(box_blocks):
                info["box"] += 1
                group_blocks.update(box_blocks)

        return info, group_blocks

    def __get_row_coords(self, row_index: int) -> List[Tuple[int, int]]:
        return [(row_index, col) for col in range(9)]

    def __get_col_coords(self, col_index: int) -> List[Tuple[int, int]]:
        return [(row, col_index) for row in range(9)]

    def __get_box_coords(self, index: int) -> List[Tuple[int, int]]:
        """The index of 3x3 box is as following:
        | 0 	| 1 	| 2 	|
        |---	|---	|---	|
        | 3 	| 4 	| 5 	|
        | 6 	| 7 	| 8 	|

        Args:
            index (int): The index of 3x3 box as list above

        Returns:
            List[Tuple[int, int]]: All the coordinates in that 3x3 box

        """
        # map to 3x3 coordinates
        # index -> 3x3 coordinates
        #  0 -> 0,0
        #  1 -> 0,1
        #  2 -> 0,2
        #  3 -> 1,0
        #  4 -> 1,1
        #  5 -> 1,2
        #  6 -> 2,0
        #  7 -> 2,1
        #  8 -> 2,2
        x, y = index // 3, index % 3

        # map to 9x9 coordinates
        x, y = x * 3, y * 3
        return [(row, col) for row in range(x, x + 3) for col in range(y, y + 3)]

    def __str__(self) -> str:
        # TODO: include score in print out, should be implemented along with CommandLineUI
        pass
