import random
from typing import Tuple

import numpy as np
import pytest

from exceptions.exceptions import ShapeOutOfBoardError
from woodoku_board import WoodokuBoard
from woodoku_shape import WoodokuShape


class TestWoodokuBoard:
    l_shape: WoodokuShape = WoodokuShape([(0, 0), (1, 0), (1, 1), (1, 2)])
    horizontal_bar_shape: WoodokuShape = WoodokuShape([(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)])
    gun_shape: WoodokuShape = WoodokuShape([(0, 0), (0, 1), (0, 2), (1, 0)])
    vertical_two_block: WoodokuShape = WoodokuShape([(0, 0), (1, 0)])
    one_block: WoodokuShape = WoodokuShape([(0, 0)])

    @pytest.mark.parametrize('row', [row for row in range(9)])
    def test_find_groups_a_row(self, row) -> None:
        """
        row should be the only group on the board
        """
        board = WoodokuBoard()
        board_with_a_row_occupied = np.full((9, 9), False)
        board_with_a_row_occupied[row] = np.full((9,), True)
        board._WoodokuBoard__representation._WoodokuBoardRepresentation__board = board_with_a_row_occupied

        group, group_blocks = board._WoodokuBoard__find_groups()
        assert group == 1
        assert group_blocks == set([(row, col) for col in range(9)])

    @pytest.mark.parametrize('col', [col for col in range(9)])
    def test_find_groups_a_col(self, col) -> None:
        """
        col column should be the only group on the board
        """
        board = WoodokuBoard()
        board_with_a_col_occupied = np.full((9, 9), False)
        board_with_a_col_occupied[:, col] = np.full((9,), True)
        board._WoodokuBoard__representation._WoodokuBoardRepresentation__board = board_with_a_col_occupied

        group, group_blocks = board._WoodokuBoard__find_groups()
        assert group == 1
        assert group_blocks == set([(row, col) for row in range(9)])

    @pytest.mark.parametrize('index', [index for index in range(9)])
    def test_find_groups_3_by_3(self, index) -> None:
        """
        The box created according to index is the only group on the board
        """
        board = WoodokuBoard()
        box_coordinate = board._WoodokuBoard__get_box_coords(index)
        for x, y in box_coordinate:
            board._WoodokuBoard__representation._WoodokuBoardRepresentation__board[x, y] = True

        group, group_blocks = board._WoodokuBoard__find_groups()
        assert group == 1
        assert group_blocks == set(box_coordinate)

    @pytest.mark.parametrize('row, col, index', [
        (random.randint(0, 8), random.randint(0, 8), random.randint(0, 8))
     ])
    def test_find_groups_a_col_a_row_and_a_three_by_three_block(self, row, col, index):
        """
        three groups is expected to be found
        """
        board = WoodokuBoard()
        repo = np.full((9, 9), False)
        repo[row] = np.full((9,), True)                               # add a row to the board
        repo[:, col] = np.full((9,), True)                            # add a column to the board
        box_coordinate = board._WoodokuBoard__get_box_coords(index)   # add a box to the board
        for x, y in box_coordinate:
            repo[x, y] = True

        board._WoodokuBoard__representation._WoodokuBoardRepresentation__board = repo
        group, group_blocks = board._WoodokuBoard__find_groups()
        assert group == 3

        expected_set = set([(row, i) for i in range(9)])
        expected_set.update([(i, col) for i in range(9)])
        expected_set.update(box_coordinate)
        assert group_blocks == expected_set

    @pytest.mark.parametrize('shape', [
        l_shape,
        horizontal_bar_shape,
        gun_shape
    ])
    def test_add_shape_on_empty_board(self, shape: WoodokuShape) -> None:
        """
        Add shape to valid position on the board and remove all blocks of the shape to test add_shape
        """
        board = WoodokuBoard()
        board.add_shape(shape, 5, 0)
        board._WoodokuBoard__representation.remove_blocks(shape.map_to_board_at(5, 0))
        assert (board._WoodokuBoard__representation._WoodokuBoardRepresentation__board == np.full((9, 9), False)).all()

    @pytest.mark.parametrize('first_shape, first_position, sec_shape, sec_position', [
        (l_shape, (0, 0), gun_shape, (4, 0)),
        (horizontal_bar_shape, (1, 0), gun_shape, (2, 0)),
        (gun_shape, (3, 0), horizontal_bar_shape, (1, 0))
    ])
    def test_add_shape_without_conflict(self, first_shape: WoodokuShape, first_position: Tuple[int, int],
                                                 sec_shape: WoodokuShape, sec_position: Tuple[int, int]) -> None:
        """
        first_shape and first_location are chosen so that sec_shape will be NOT overlapped with first_shape when
        adding it at sec_location and no group will form
        """
        board = WoodokuBoard()
        board.add_shape(first_shape, *first_position)
        board.add_shape(sec_shape, *sec_position)

        expected = np.full((9, 9), False)
        for x, y in first_shape.map_to_board_at(*first_position):
            expected[x, y] = True
        for x, y in sec_shape.map_to_board_at(*sec_position):
            expected[x, y] = True
        assert (board._WoodokuBoard__representation._WoodokuBoardRepresentation__board == expected).all()

    def test_add_shape_with_a_row_formed(self) -> None:
        """
        a row group should be removed by add_shape
        """
        board = WoodokuBoard()
        board.add_shape(self.horizontal_bar_shape, 0, 0)
        board.add_shape(self.gun_shape, 0, 5)
        board.add_shape(self.vertical_two_block, 0, 8)
        group, group_blocks = board._WoodokuBoard__find_groups()
        assert group == 0
        assert group_blocks == set([])

    def test_find_groups_almost_a_col(self) -> None:
        """
        No column is formed
        """
        board = WoodokuBoard()
        board.add_shape(self.gun_shape, 0, 1)
        board.add_shape(self.vertical_two_block, 2, 1)
        board.add_shape(self.gun_shape, 4, 1)
        board.add_shape(self.vertical_two_block, 6, 1)
        group, group_blocks = board._WoodokuBoard__find_groups()
        assert group == 0

    def test_add_shape_with_a_col_formed(self) -> None:
        """
        A column group should be removed by add_shape
        """
        board = WoodokuBoard()
        board.add_shape(self.gun_shape, 0, 1)
        board.add_shape(self.vertical_two_block, 2, 1)
        board.add_shape(self.gun_shape, 4, 1)
        board.add_shape(self.vertical_two_block, 6, 1)
        board.add_shape(self.l_shape, 7, 0)
        group, group_blocks = board._WoodokuBoard__find_groups()
        assert group == 0
        assert group_blocks == set([])

    def test_add_shape_with_a_three_by_three_block_formed(self) -> None:
        """
        A 3X3 block group should be removed by add_shape
        """
        board = WoodokuBoard()
        board.add_shape(self.gun_shape, 0, 0)
        board.add_shape(self.horizontal_bar_shape, 1, 1)
        board.add_shape(self.gun_shape, 2, 0)
        group, group_blocks = board._WoodokuBoard__find_groups()
        assert group == 0
        assert group_blocks == set([])

    @pytest.mark.parametrize('shape, location', [
        (l_shape, (0, 0)),
        (horizontal_bar_shape, (0, 3)),
        (gun_shape, (6, 0)),
    ])
    def test_can_add_shape_at_location_on_empty_board_within_board(self, shape: WoodokuShape,
                                                                   location: Tuple[int, int]) -> None:
        """
        Add shape to an empty board where each location to add is at the edge of the game board
        """
        board = WoodokuBoard()
        assert board.can_add_shape_at_location(shape, *location)

    @pytest.mark.parametrize('shape, location', [
        (l_shape, (6, 8)),
        (horizontal_bar_shape, (4, 3)),
        (gun_shape, (4, 0)),
    ])
    def test_can_add_shape_at_location_on_empty_board_go_beyond_board(self, shape: WoodokuShape,
                                                                      location: Tuple[int, int]) -> None:
        """
        Add shape to an empty board where location goes beyond the game board
        """
        board = WoodokuBoard()
        with pytest.raises(ShapeOutOfBoardError):
            board.can_add_shape_at_location(shape, *location)

    @pytest.mark.parametrize('first_shape, first_position, sec_shape, sec_position', [
        (l_shape, (0, 0), l_shape, (1, 0)),
        (horizontal_bar_shape, (4, 3), gun_shape, (4, 4)),
        (gun_shape, (4, 0), horizontal_bar_shape, (5, 0)),
    ])
    def test_can_add_shape_at_occupied_location(self, first_shape: WoodokuShape, first_position: Tuple[int, int],
                                                sec_shape: WoodokuShape, sec_position: Tuple[int, int]) -> None:
        """
        first_shape and first_location are chosen so that sec_shape will be overlapped with first_shape when
        adding it at sec_location
        """
        board = WoodokuBoard()
        board.add_shape(first_shape, *first_position)
        assert not board.can_add_shape_at_location(sec_shape, *sec_position)

    @pytest.mark.parametrize('shape', [
        l_shape,
        horizontal_bar_shape,
        gun_shape
    ])
    def test_can_add_shape_to_board_on_empty_board(self, shape: WoodokuShape) -> None:
        board = WoodokuBoard()
        assert board.can_add_shape_to_board(shape)

    @pytest.mark.parametrize('shape', [
        l_shape,
        horizontal_bar_shape,
        gun_shape,
        vertical_two_block
    ])
    def test_can_add_shape_to_board_on_crowded_board_fail(self, shape) -> None:
        """
        The board is designed that all positions are occupied except the left diagonal
        """
        board = WoodokuBoard()
        repo = np.full((9, 9), True)
        for x, y in [(i, i) for i in range(9)]:
            repo[x, y] = False
        board._WoodokuBoard__representation._WoodokuBoardRepresentation__board = repo
        assert not board.can_add_shape_to_board(shape)

    def test_can_add_shape_to_board_on_crowded_board_success(self) -> None:
        """
        The board is designed that all positions are occupied except the left diagonal
        """
        board = WoodokuBoard()
        repo = np.full((9, 9), True)
        for x, y in [(i, i) for i in range(9)]:
            repo[x, y] = False
        board._WoodokuBoard__representation._WoodokuBoardRepresentation__board = repo
        assert board.can_add_shape_to_board(self.one_block)

