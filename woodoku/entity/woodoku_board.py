from typing import Iterable, List, Set, Tuple

import numpy as np
from art import text2art
from numpy.typing import NDArray
from woodoku.entity.score_agent import ScoreAgent
from woodoku.entity.woodoku_shape import WoodokuShape
from woodoku.exceptions.shape_out_of_board_error import ShapeOutOfBoardError
from woodoku.ui.utils import (
    ALL_BOLD_CROSS,
    BLOCK,
    BOLD_BOTTOM_JOIN,
    BOLD_HORIZONTAL,
    BOLD_TOP_JOIN,
    BOLD_VERTICAL,
    BOTTOM_JOIN,
    BOTTOM_LEFT,
    BOTTOM_RIGHT,
    CROSS,
    HORIZONTAL,
    HORIZONTAL_BOLD_CROSS,
    LEFT_JOIN,
    RIGHT_JOIN,
    TOP_JOIN,
    TOP_LEFT,
    TOP_RIGHT,
    VERTICAL,
    VERTICAL_CROSS,
    green,
    inbetween,
    orange,
    red,
)

# the length of the square game board
BOARD_SIZE = 9


class _WoodokuBoardRepresentation:
    """Private data class representing the low-level implementation of the board

    The top-left block's coordinate is (0, 0).
    The last block on the top row is (0, n - 1).
    The first block on the bottom row is (n - 1, 0).
    The bottom-right block's coordinate is (n - 1, n - 1).

    _board: an 2d array to record the occupancy of each position on the game board. The value is set to True when
    the position occupied
    """

    _board: NDArray[np.bool8]

    def __init__(self) -> None:
        self._board = np.full((BOARD_SIZE, BOARD_SIZE), False)

    def add_blocks(self, blocks_coord: Iterable[Tuple[int, int]]) -> None:
        """
        Mark each position specified in blocks_coord as True to indicate that the position is occupied.

        Args:
             blocks_coord: a list of (x,y) tuples to be added to the board

        Raises:
            ShapeOutOfBoundError: if any block in `blocks` is invalid
        """
        for row, col in blocks_coord:
            self.__validate((row, col))
            self._board[row, col] = True

    def remove_blocks(self, blocks_coord: Iterable[Tuple[int, int]]) -> None:
        """
        Mark each position specified in blocks_coord as False to indicate that the position is not occupied.

        Args:
         blocks_coord: a list of (x,y) tuples to be added to the board

        Raises:
            ShapeOutOfBoundError: if any block in `blocks` is invalid
        """
        for row, col in blocks_coord:
            self.__validate((row, col))
            self._board[row, col] = False

    def is_occupied(self, blocks_coord: Iterable[Tuple[int, int]]) -> bool:
        """Check if each block has is occupied. If all of those blocks are
        occupied, return true. Otherwise, false.

        Args:
            blocks_coord (List[Tuple[int, int]]): list of blocks to check

        Returns:
            bool: if all blocks in `blocks_coord` is occupied

        Raises:
            ShapeOutOfBoundError: if any block in `blocks` is invalid
        """
        for row, col in blocks_coord:
            self.__validate((row, col))
            if not self._board[row, col]:
                return False
        return True

    def is_not_occupied(self, blocks_coord: Iterable[Tuple[int, int]]) -> bool:
        """Check if each block is empty. If all of those blocks are empty,
        return true. Otherwise, false.

        Args:
            blocks_coord (List[Tuple[int, int]]): list of blocks to check

        Returns:
            bool: if all blocks in `blocks_coord` is empty

        Raises:
            ShapeOutOfBoundError: if any block in `blocks` is invalid
        """
        for row, col in blocks_coord:
            self.__validate((row, col))
            if self._board[row, col]:
                return False
        return True

    @staticmethod
    def __validate(block: Tuple[int, int]) -> None:
        """validate if block is within the 9x9 board. raise Error if not.

        Args:
            block (Tuple[int, int]): The block to be validated

        Raises:
            ShapeOutOfBoardError: when some block is not valid
        """
        x, y = block
        if not (0 <= x <= BOARD_SIZE - 1 and 0 <= y <= BOARD_SIZE - 1):
            raise ShapeOutOfBoardError(x, y)

    def __str__(self) -> str:
        """
        A string representation of a 9X9 game board where each line and block are drawn using box-drawing characters
        https://www.unicode.org/charts/PDF/U2500.pdf

        The board consists of ten horizontal lines starting from the far left of the board to the far right and
         nine rows of vertical lines where each line in a row separates columns on the board.

         To print out smooth joins, left and right borders, the first and the last box-drawing characters in a
         horizontal line are concatenated separately from the rest.
         Similarly, to print out smooth corners, top and bottom borders, the first and last lines are concatenated
         separately with delicately chosen joins.

         To highlight every non-overlapping 3X3 blocks, two vertical and two horizontal lines are bolded
         and colored red.
        """
        result = ""
        horizontal_bar = HORIZONTAL * 5
        bold_horizontal_bar = BOLD_HORIZONTAL * 5

        for row in range(2 * BOARD_SIZE):
            # the first line of the board is concatenated using delicately chosen joins and corners for smooth corners
            # and top border
            row_str = "   "  # print some space to match the first column
            if row == 0:
                row_str = f"  {green('y')}   "
                row_str += "     ".join(
                    [f"{y}" for y in range(BOARD_SIZE)]
                )  # print y coordinates
                row_str += "\n"
                row_str += f"{green('x')}  "  # print the first row
                row_str += inbetween(
                    TOP_LEFT, TOP_JOIN, BOLD_TOP_JOIN, TOP_RIGHT, horizontal_bar
                )

            # every even indexed row corresponds to a horizontal line on the board
            elif row % 2 == 0:
                # every six indexed row corresponds to a boundary of 3X3 blocks, and thus need to be bolded
                if row % 3 == 0:
                    row_str += inbetween(
                        LEFT_JOIN,
                        HORIZONTAL_BOLD_CROSS,
                        red(ALL_BOLD_CROSS),
                        RIGHT_JOIN,
                        red(bold_horizontal_bar),
                    )
                else:
                    row_str += inbetween(
                        LEFT_JOIN, CROSS, VERTICAL_CROSS, RIGHT_JOIN, horizontal_bar
                    )

            # every odd indexed row consists of vertical lines separating columns on the board
            else:
                # this else block can't be replaced by calling helper function inbetween(...), since traversing
                # boardRepresentation relies on the loop invariant "row"
                row_str = f"{row // 2}  {VERTICAL}"  # print x coordinate
                for col in range(BOARD_SIZE):
                    pos = "     "
                    if self._board[row // 2, col]:
                        pos = f"  {green(BLOCK)}  "
                    # since the vertical line at index 0 is drawn separately, the border of every 3X3 blocks is
                    # at col = 2 and col = 5
                    if col in (2, 5):
                        pos += red(BOLD_VERTICAL)
                    else:
                        pos += VERTICAL
                    row_str += pos
            row_str += "\n"
            result += row_str
        # the last line of the board is concatenated using delicately chosen joins and corners for smooth corners and
        # bottom border of the board
        row_str = "   "  # print some empty space to match the row above
        row_str += inbetween(
            BOTTOM_LEFT, BOTTOM_JOIN, BOLD_BOTTOM_JOIN, BOTTOM_RIGHT, horizontal_bar
        )
        result += row_str
        return result


class WoodokuBoard:
    """A 9x9 Woodoku Board"""

    __score_agent: ScoreAgent
    _representation: _WoodokuBoardRepresentation

    def __init__(self) -> None:
        self.__score_agent = ScoreAgent()
        self._representation = _WoodokuBoardRepresentation()

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
        all_blocks = [(i, j) for i in range(9) for j in range(BOARD_SIZE)]
        rng.shuffle(all_blocks)

        for row, col in all_blocks:
            try:
                if self.can_add_shape_at_location(shape, x=row, y=col):
                    return True
            except ShapeOutOfBoardError:
                # exceptions are ignored when checking can_add_shape_to_board
                # as it is only for internal checking and avoids checking shapes that are out of the board
                pass
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
        try:
            return self._representation.is_not_occupied(blocks)
        except ShapeOutOfBoardError:
            return False

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
        self._representation.add_blocks(shape_blocks)

        # determine groups and clear the groups
        groups, group_blocks = self._find_groups()
        self.__score_agent.calculate_winning(len(shape), groups)
        self._representation.remove_blocks(group_blocks)

    def get_score(self) -> int:
        return self.__score_agent.get_score()

    def _find_groups(self) -> Tuple[int, Set[Tuple[int, int]]]:
        """Check current board and see if there is any groups such as
        complete rows, columns or 3x3 box and report them.

        Terminology Reference:
        [Wikipedia Sudoku Glossary](https://en.wikipedia.org/wiki/Glossary_of_Sudoku#Terminology_and_grid_layout)

        Returns:
            Tuple[int, Set[Tuple[int,int]]]:
                1. Number of groups that is complete
                2. Set of block coordinates for the group
        """
        groups = 0
        rep = self._representation
        group_blocks = set()  # use set to handle overlapping group removal
        for index in range(BOARD_SIZE):
            row_blocks = self._get_row_coords(index)
            col_blocks = self._get_col_coords(index)
            box_blocks = self._get_box_coords(index)

            if rep.is_occupied(row_blocks):
                groups += 1
                group_blocks.update(row_blocks)

            if rep.is_occupied(col_blocks):
                groups += 1
                group_blocks.update(col_blocks)

            if rep.is_occupied(box_blocks):
                groups += 1
                group_blocks.update(box_blocks)

        return groups, group_blocks

    @staticmethod
    def _get_row_coords(row_index: int) -> List[Tuple[int, int]]:
        return [(row_index, col) for col in range(BOARD_SIZE)]

    @staticmethod
    def _get_col_coords(col_index: int) -> List[Tuple[int, int]]:
        return [(row, col_index) for row in range(BOARD_SIZE)]

    @staticmethod
    def _get_box_coords(index: int) -> List[Tuple[int, int]]:
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
        streak = self.__score_agent.get_streak()
        combo = self.__score_agent.get_combo()
        bonus = ""

        if streak >= 2:
            bonus += f"Streak:{streak}x!"

        if combo > 0:
            bonus += "\n" if bonus else ""
            bonus += f"Combo:{combo}x!"

        if bonus:
            bonus = str(text2art(f"{bonus}", "starwars"))
        score = str(
            text2art(f"Score:{str(self.__score_agent.get_score())}", "starwars")
        )
        return orange(score + bonus) + str(self._representation) + "\n"
