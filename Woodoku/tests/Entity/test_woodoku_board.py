from typing import Tuple

import pytest

from Exceptions.Exceptions import ShapeOutOfBoardError
from WoodokuBoard import _WoodokuBoardRepresentation
import numpy as np

N = 9


class TestWoodokuRepresentation:
    one_block_lst = [(0, 0)]
    three_block_lst = [(1, 3), (5, 8), (0, 7)]
    five_block_lst = three_block_lst + [(2, 1), (0, 7)]

    def board_after_adding(self, rep: _WoodokuBoardRepresentation, lst: list):
        rep.add_blocks(lst)
        return rep.board()

    def board_after_removing(self, rep: _WoodokuBoardRepresentation, lst: list):
        rep.remove_blocks(lst)
        return rep.board()

    def test_add_blocks_add_one_block(self):
        board = self.board_after_adding(_WoodokuBoardRepresentation(), self.one_block_lst)

        expect = np.full((N, N), False)
        x, y = self.one_block_lst[0]
        expect[x, y] = True
        assert (board == expect).all(), f'test fail because board =\n {board}, \n\n while expect =\n {expect}'

    def test_add_blocks_add_three_blocks(self):
        board = self.board_after_adding(_WoodokuBoardRepresentation(), self.three_block_lst)

        expect = np.full((N, N), False)
        for row, col in self.three_block_lst:
            expect[row, col] = True
        assert (board == expect).all(), f'test fail because board =\n {board}, \n\n while expect =\n {expect}'

    def test_remove_blocks_remove_one_block(self):
        rep = _WoodokuBoardRepresentation()
        rep.add_blocks(self.one_block_lst)
        board_removed = self.board_after_removing(rep, self.one_block_lst)

        expect = np.full((N, N), False)
        assert (board_removed == expect).all(), f'test fail because board =\n {board_removed}, \n\n while expect =\n {expect}'

    def test_remove_blocks_remove_five_block(self):
        rep = _WoodokuBoardRepresentation()
        rep.add_blocks(self.five_block_lst)
        board_removed = self.board_after_removing(rep, self.five_block_lst)

        expect = np.full((N, N), False)
        assert (board_removed == expect).all(), f'test fail because board =\n {board_removed}, \n\n while expect =\n {expect}'

    # add five blocks and remove three of them
    def test_remove_blocks_remove_three_block(self):
        rep = _WoodokuBoardRepresentation()
        rep.add_blocks(self.five_block_lst)
        board_removed = self.board_after_removing(rep, self.three_block_lst)

        expect = np.full((N, N), False)
        for row, col in self.five_block_lst:
            if (row, col) not in self.three_block_lst:
                expect[row, col] = True

        assert (board_removed == expect).all(), f'test fail because board =\n {board_removed}, \n\n while expect =\n {expect}'

    def test_is_occupied_on_empty_board(self):
        rep = _WoodokuBoardRepresentation()
        assert not rep.is_occupied(self.one_block_lst)
        assert not rep.is_occupied(self.three_block_lst)
        assert not rep.is_occupied(self.five_block_lst)

    def test_is_occupied_with_empty_lst(self):
        rep = _WoodokuBoardRepresentation()
        assert rep.is_occupied([])

    def test_is_occupied_with_all_one_occupied(self):
        rep = _WoodokuBoardRepresentation()
        rep.add_blocks(self.one_block_lst)
        assert rep.is_occupied(self.one_block_lst)

    def test_is_occupied_with_all_three_occupied(self):
        rep = _WoodokuBoardRepresentation()
        rep.add_blocks(self.three_block_lst)
        assert rep.is_occupied(self.three_block_lst)

    def test_is_occupied_with_two_out_of_five_occupied(self):
        rep = _WoodokuBoardRepresentation()
        rep.add_blocks(self.five_block_lst)
        rep.remove_blocks(self.three_block_lst)
        assert not rep.is_occupied(self.five_block_lst)

    def test_is_not_occupied_on_empty_board(self):
        rep = _WoodokuBoardRepresentation()
        assert rep.is_not_occupied(self.one_block_lst)
        assert rep.is_not_occupied(self.three_block_lst)
        assert rep.is_not_occupied(self.five_block_lst)

    def test_is_not_occupied_with_empty_list(self):
        rep = _WoodokuBoardRepresentation()
        assert rep.is_not_occupied([])

    def test_is_not_occupied_with_all_occupied(self):
        rep = _WoodokuBoardRepresentation()
        rep.add_blocks(self.five_block_lst)
        assert not rep.is_not_occupied(self.five_block_lst)

    def test_is_not_occupied_with_some_occupied(self):
        rep = _WoodokuBoardRepresentation()
        rep.add_blocks(self.five_block_lst)
        rep.remove_blocks(self.three_block_lst)
        assert not rep.is_not_occupied(self.five_block_lst)

    def test_is_not_occupied_with_all_occupied(self):
        rep = _WoodokuBoardRepresentation()
        rep.add_blocks(self.five_block_lst)
        rep.remove_blocks(self.five_block_lst)
        assert rep.is_not_occupied(self.five_block_lst)
