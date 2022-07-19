from WoodokuBoard import WoodokuBoardRepresentation
import numpy as np
N = 3


class TestWoodokuBoardRepresentation:
    def test_add_blocks_add_one_block(self):
        board = WoodokuBoardRepresentation(N)
        board.add_blocks([(0, 0)])

    def test_add_blocks_add_multiple_blocks(self):
        pass

    def test_remove_blocks_remove_one_block(self):
        pass

    def test_remove_blocks_remove_multiple_block(self):
        pass


