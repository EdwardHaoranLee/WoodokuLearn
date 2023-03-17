from unittest.mock import MagicMock
import pytest

from woodoku.game import rotate_all_shapes, random_shapes, is_out_of_space
from woodoku.entity.woodoku_shape import WoodokuShape
from woodoku.entity.woodoku_board import WoodokuBoard


class TestGame:
    @pytest.mark.parametrize(
        "raw_shapes",
        [
            (
                [
                    WoodokuShape([(0, 0)]),
                    WoodokuShape([(0, 0), (1, 0), (2, 0)]),
                    WoodokuShape([(0, 1), (1, 0), (1, 1), (2, 1)]),
                    WoodokuShape([(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)]),
                    WoodokuShape([(0, 0), (0, 1), (0, 2), (1, 2)]),
                    WoodokuShape([(0, 0), (1, 1), (2, 2), (3, 3)]),
                ]
            ),
            ([WoodokuShape([(0, 0)])]),
        ],
    )
    def test_rotate_all_shapes(self, raw_shapes: list[WoodokuShape]) -> None:
        raw_rotated = rotate_all_shapes(raw_shapes)
        assert len(set(raw_rotated)) == len(raw_rotated)
        assert len(raw_rotated) >= len(raw_shapes)

        rotated = set(raw_rotated)
        for shape in raw_shapes:
            assert shape.rotate() in rotated
            assert shape.rotate().rotate() in rotated
            assert shape.rotate().rotate().rotate() in rotated

    @pytest.mark.parametrize(
        "shapes, num",
        [
            (
                [
                    WoodokuShape([(0, 0)]),
                    WoodokuShape([(0, 0), (1, 0), (2, 0)]),
                    WoodokuShape([(0, 1), (1, 0), (1, 1), (2, 1)]),
                ],
                2,
            ),
            (
                [
                    WoodokuShape([(0, 0)]),
                    WoodokuShape([(0, 0), (1, 0), (2, 0)]),
                    WoodokuShape([(0, 1), (1, 0), (1, 1), (2, 1)]),
                    WoodokuShape([(0, 0), (0, 1), (0, 2), (1, 1), (2, 0)]),
                    WoodokuShape([(0, 0), (0, 1), (0, 2), (1, 2)]),
                    WoodokuShape([(0, 0), (1, 1), (2, 2), (3, 3)]),
                ],
                5,
            ),
        ],
    )
    def test_random_shapes(self, shapes: list[WoodokuShape], num: int) -> None:
        selected = random_shapes(shapes, num)
        assert len(selected) == num

    def test_is_not_out_of_space(self) -> None:
        board = WoodokuBoard()
        board.can_add_shape_to_board = MagicMock(side_effect=[True, True])  # type: ignore[method-assign]
        # Assigning method type bug was not fixed by mypy team. Ref: https://github.com/python/mypy/issues/708

        assert not is_out_of_space(board, [WoodokuShape([(0, 0)]), WoodokuShape([(0, 0)])], [True, True])

    def test_is_not_out_of_space_2(self) -> None:
        board = WoodokuBoard()
        board.can_add_shape_to_board = MagicMock(side_effect=[True, False])  # type: ignore[method-assign]
        # Assigning method type bug was not fixed by mypy team. Ref: https://github.com/python/mypy/issues/708
        assert not is_out_of_space(board, [WoodokuShape([(0, 0)]), WoodokuShape([(0, 0)])], [True, True])

    def test_is_out_of_space(self) -> None:
        board = WoodokuBoard()
        board.can_add_shape_to_board = MagicMock(side_effect=[False, False])  # type: ignore[method-assign]
        # Assigning method type bug was not fixed by mypy team. Ref: https://github.com/python/mypy/issues/708
        assert is_out_of_space(board, [WoodokuShape([(0, 0)]), WoodokuShape([(0, 0)])], [True, True])
