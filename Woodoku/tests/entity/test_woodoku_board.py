import numpy as np
import pytest

from exceptions.exceptions import ShapeOutOfBoardError
from woodoku_board import WoodokuBoard
from woodoku_shape import WoodokuShape

N = 9


class TestWoodokuBoard:
    l_shape: WoodokuShape = WoodokuShape([(0, 0), (1, 0), (1, 1), (1, 2)])
    horizontal_bar_shape: WoodokuShape = WoodokuShape([(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)])
    gun_shape: WoodokuShape = WoodokuShape([(0, 0), (0, 1), (0, 2), (1, 0)])
    vertical_two_block: WoodokuShape = WoodokuShape([(0, 0), (1, 0)])
    one_block: WoodokuShape = WoodokuShape([(0, 0)])

    @pytest.mark.parametrize('shape', [
        l_shape,
        horizontal_bar_shape,
        gun_shape
    ])
    def test_add_shape_on_empty_board(self, shape):
        """
        Add shape to valid position on the board and remove all blocks of the shape to test add_shape
        """
        board = WoodokuBoard()
        board.add_shape(shape, 5, 0)
        board._WoodokuBoard__representation.remove_blocks(shape.map_to_board_at(5, 0))
        assert (board._WoodokuBoard__representation._WoodokuBoardRepresentation__board == np.full((N, N), False)).all()

    @pytest.mark.parametrize('first_shape, first_position, sec_shape, sec_position', [
        (l_shape, (0, 0), gun_shape, (4, 0)),
        (horizontal_bar_shape, (1, 0), gun_shape, (2, 0)),
        (gun_shape, (3, 0), horizontal_bar_shape, (1, 0))
    ])
    def test_add_shape_on_board_without_conflict(self, first_shape, first_position, sec_shape, sec_position):
        """
        first_shape and first_location are chosen so that sec_shape will be NOT overlapped with first_shape when
        adding it at sec_location
        """
        board = WoodokuBoard()
        try:
            board.add_shape(first_shape, *first_position)
            board.add_shape(sec_shape, *sec_position)
        except ShapeOutOfBoardError as exc:
            assert False, f"shape with coordinates: {first_shape.get_coords} , {sec_shape} " \
                          f"and positions: {first_position}, {sec_position} raised an exception {exc}"

    @pytest.mark.parametrize('shape, location', [
        (l_shape, (0, 0)),
        (horizontal_bar_shape, (0, 3)),
        (gun_shape, (N - 3, 0)),
    ])
    def test_can_add_shape_at_location_on_empty_board_within_board(self, shape, location):
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
    def test_can_add_shape_at_location_on_empty_board_go_beyond_board(self, shape, location):
        """
        Add shape to an empty board where location goes beyond the game board
        """
        board = WoodokuBoard()
        with pytest.raises(ShapeOutOfBoardError):
            board.can_add_shape_at_location(shape, *location)

    @pytest.mark.parametrize('first_shape, first_location, sec_shape, sec_location', [
        (l_shape, (0, 0), l_shape, (1, 0)),
        (horizontal_bar_shape, (4, 3), gun_shape, (4, 4)),
        (gun_shape, (4, 0), horizontal_bar_shape, (5, 0)),
    ])
    def test_can_add_shape_at_occupied_location(self, first_shape, first_location, sec_shape, sec_location):
        """
        first_shape and first_location are chosen so that sec_shape will be overlapped with first_shape when
        adding it at sec_location
        """
        board = WoodokuBoard()
        board.add_shape(first_shape, *first_location)
        assert not board.can_add_shape_at_location(sec_shape, *sec_location)

    @pytest.mark.parametrize('shape', [
        l_shape,
        horizontal_bar_shape,
        gun_shape
    ])
    def test_can_add_shape_to_board_on_empty_board(self, shape):
        board = WoodokuBoard()
        assert board.can_add_shape_to_board(shape)

    @pytest.mark.parametrize('first_shape, first_location, sec_shape, sec_location', [
        (l_shape, (0, 0), l_shape, (1, 0)),
        (horizontal_bar_shape, (4, 3), gun_shape, (4, 4)),
        (gun_shape, (4, 0), horizontal_bar_shape, (5, 0)),
    ])
    def test_can_add_shape_to_board_on_conflicted_board(self, first_shape, first_location, sec_shape, sec_location):
        """
        first_shape and first_location are chosen so that sec_shape will be overlapped with first_shape when
        adding it at sec_location
        """
        board = WoodokuBoard()
        assert board.can_add_shape_to_board(first_shape, *first_location)
        assert not board.can_add_shape_to_board(sec_shape, *sec_location)

    def test_find_groups_a_row(self):
        """
        A first row should be the only group on the board
        """
        board = WoodokuBoard()
        board.add_shape(self.horizontal_bar_shape, 0, 0)
        board.add_shape(self.gun_shape, 0, 5)
        board.add_shape(self.vertical_two_block, 0, 8)
        info, group_blocks = board._WoodokuBoard__find_groups()
        assert info == {"row": 1, "column": 0, "box": 0}
        assert group_blocks == set([(0, col) for col in range(9)])

    def test_find_groups_almost_a_col(self):
        """
        A first column should be the only group on the board
        """
        board = WoodokuBoard()
        board.add_shape(self.gun_shape, 0, 1)
        board.add_shape(self.vertical_two_block, 2, 1)
        board.add_shape(self.gun_shape, 4, 1)
        board.add_shape(self.vertical_two_block, 6, 1)
        info, group_blocks = board._WoodokuBoard__find_groups()
        assert info == {"row": 0, "column": 0, "box": 0}

    def test_find_groups_a_col(self):
        board = WoodokuBoard()
        board.add_shape(self.gun_shape, 0, 1)
        board.add_shape(self.vertical_two_block, 2, 1)
        board.add_shape(self.gun_shape, 4, 1)
        board.add_shape(self.vertical_two_block, 6, 1)
        board.can_add_shape_at_location(self.l_shape, 7, 0)

        info, group_blocks = board._WoodokuBoard__find_groups()
        assert info == {"row": 0, "column": 1, "box": 0}
        assert group_blocks == set([(row, 1) for row in range(9)])
        assert False, f"\n{board._WoodokuBoard__representation._WoodokuBoardRepresentation__board}"

    def test_find_groups_a_three_by_three_block(self):
        """
        A 3X3 square at the right corner should be the only group on the board
        """
        board = WoodokuBoard()
        board.add_shape(self.gun_shape, 0, 0)
        board.add_shape(self.horizontal_bar_shape, 1, 1)
        board.add_shape(self.gun_shape, 2, 0)
        info, group_blocks = board._WoodokuBoard__find_groups()
        assert info == {"row": 0, "column": 0, "box": 1}
        assert group_blocks == set([(0, col) for col in range(9)])

    # TODO: implement it
    # def test_find_groups_a_col_and_a_row(self):

    # TODO: implement it
    # def test_find_groups_a_col_a_row_and_a_box(self):
