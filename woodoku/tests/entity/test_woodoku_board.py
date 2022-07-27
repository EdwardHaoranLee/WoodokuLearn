import numpy as np
import pytest
from numpy import ndarray

from entity.woodoku_board import _WoodokuBoardRepresentation

N = 9

# pylint: disable=protected-access


class TestWoodokuRepresentation:
    one_block_lst = [(0, 0)]
    three_block_lst = [(1, 3), (5, 8), (0, 7)]
    five_block_lst = three_block_lst + [(2, 1), (0, 8)]

    def board_after_adding(
        self, rep: _WoodokuBoardRepresentation, lst: list
    ) -> ndarray:
        rep.add_blocks(lst)
        return rep._WoodokuBoardRepresentation__board

    def board_after_removing(
        self, rep: _WoodokuBoardRepresentation, lst: list
    ) -> ndarray:
        rep.remove_blocks(lst)
        return rep._WoodokuBoardRepresentation__board

    @pytest.mark.parametrize(
        "lst",
        [
            one_block_lst,
            three_block_lst,
            five_block_lst,
        ],
    )
    def test_add_blocks_add_list_of_blocks(self, lst: list) -> None:
        board = self.board_after_adding(_WoodokuBoardRepresentation(), lst)

        expect = np.full((N, N), False)
        for row, col in lst:
            expect[row, col] = True
        assert (board == expect).all()

    @pytest.mark.parametrize(
        "lst",
        [
            one_block_lst,
            three_block_lst,
            five_block_lst,
        ],
    )
    def test_remove_blocks_remove_list_of_blocks(self, lst: list) -> None:
        rep = _WoodokuBoardRepresentation()
        rep.add_blocks(lst)
        board_removed = self.board_after_removing(rep, lst)

        expect = np.full((N, N), False)
        assert (board_removed == expect).all()

    # add five blocks and remove three of them
    def test_remove_blocks_remove_three_block(self) -> None:
        rep = _WoodokuBoardRepresentation()
        rep.add_blocks(self.five_block_lst)
        board_removed = self.board_after_removing(rep, self.three_block_lst)

        expect = np.full((N, N), False)
        for row, col in self.five_block_lst:
            if (row, col) not in self.three_block_lst:
                expect[row, col] = True

        assert (
            board_removed == expect
        ).all(), f"test fail because board =\n {board_removed}, \n\n while expect =\n {expect}"

    def test_is_occupied_on_empty_board(self) -> None:
        rep = _WoodokuBoardRepresentation()
        assert not rep.is_occupied(self.one_block_lst)
        assert not rep.is_occupied(self.three_block_lst)
        assert not rep.is_occupied(self.five_block_lst)

    def test_is_occupied_with_empty_lst(self) -> None:
        rep = _WoodokuBoardRepresentation()
        assert rep.is_occupied([])

    def test_is_occupied_with_all_one_occupied(self) -> None:
        rep = _WoodokuBoardRepresentation()
        rep.add_blocks(self.one_block_lst)
        assert rep.is_occupied(self.one_block_lst)

    def test_is_occupied_with_all_three_occupied(self) -> None:
        rep = _WoodokuBoardRepresentation()
        rep.add_blocks(self.three_block_lst)
        assert rep.is_occupied(self.three_block_lst)

    def test_is_occupied_with_two_out_of_five_occupied(self) -> None:
        rep = _WoodokuBoardRepresentation()
        rep.add_blocks(self.five_block_lst)
        rep.remove_blocks(self.three_block_lst)
        assert not rep.is_occupied(self.five_block_lst)

    def test_is_not_occupied_on_empty_board(self) -> None:
        rep = _WoodokuBoardRepresentation()
        assert rep.is_not_occupied(self.one_block_lst)
        assert rep.is_not_occupied(self.three_block_lst)
        assert rep.is_not_occupied(self.five_block_lst)

    def test_is_not_occupied_with_empty_list(self) -> None:
        rep = _WoodokuBoardRepresentation()
        assert rep.is_not_occupied([])

    def test_is_not_occupied_with_all_occupied(self) -> None:
        rep = _WoodokuBoardRepresentation()
        rep.add_blocks(self.five_block_lst)
        assert not rep.is_not_occupied(self.five_block_lst)

    def test_is_not_occupied_with_some_occupied(self) -> None:
        rep = _WoodokuBoardRepresentation()
        rep.add_blocks(self.five_block_lst)
        rep.remove_blocks(self.three_block_lst)
        assert not rep.is_not_occupied(self.five_block_lst)

    def test_is_not_occupied_with_blocks_added_then_removed(self) -> None:
        rep = _WoodokuBoardRepresentation()
        rep.add_blocks(self.five_block_lst)
        rep.remove_blocks(self.five_block_lst)
        assert rep.is_not_occupied(self.five_block_lst)
