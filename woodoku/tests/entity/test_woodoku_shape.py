import pytest

from woodoku.entity.woodoku_shape import WoodokuShape


class TestWoodokuShape:
    @pytest.mark.parametrize(
        "coords, coords_standardized",
        [
            ([(0, 0)], [(0, 0)]),
            ([(1, 0)], [(0, 0)]),
            ([(0, 1)], [(0, 0)]),
            ([(1, 1)], [(0, 0)]),
            ([(1, 1), (2, 1), (3, 1)], [(0, 0), (1, 0), (2, 0)]),
            ([(3, 6), (4, 6), (5, 6), (4, 5)], [(0, 1), (1, 0), (1, 1), (2, 1)]),
        ],
    )
    def test_standardize(self, coords, coords_standardized):
        assert set(WoodokuShape(coords).get_coords()) == set(coords_standardized)

    @pytest.mark.parametrize(
        "coords_before_rotate, coords_after_rotate",
        [
            ([(0, 0)], [(0, 0)]),
            ([(0, 0), (0, 1), (0, 2)], [(0, 0), (1, 0), (2, 0)]),
            ([(0, 0), (0, 1), (1, 0)], [(0, 0), (1, 0), (1, 1)]),
            ([(0, 0), (1, 0), (2, 0), (2, 1)], [(1, 0), (1, 1), (1, 2), (0, 2)]),
            ([(0, 0), (1, 0), (0, 1), (0, 2)], [(0, 0), (1, 0), (2, 0), (2, 1)]),
        ],
    )
    def test_rotate(self, coords_before_rotate, coords_after_rotate):
        assert set(WoodokuShape(coords_before_rotate).rotate().get_coords()) == set(
            coords_after_rotate
        )

    @pytest.mark.parametrize(
        "coords",
        [
            ([(0, 0)]),
            ([(0, 0), (0, 1), (0, 2)]),
            ([(0, 0), (0, 1), (1, 0)]),
            ([(0, 0), (1, 0), (2, 0), (2, 1)]),
            ([(0, 0), (1, 0), (0, 1), (0, 2)]),
            ([(0, 1), (1, 0), (1, 1), (2, 1)]),
        ],
    )
    def test_rotate_to_itself(self, coords):
        shape = WoodokuShape(coords)
        new_shape = shape.rotate().rotate().rotate().rotate()

        assert set(shape.get_coords()) == set(new_shape.get_coords())

    @pytest.mark.parametrize(
        "coords1, coords2",
        [
            ([(0, 0)], [(0, 0)]),
            ([(0, 0)], [(0, 1)]),
            ([(0, 0), (0, 1), (0, 2)], [(0, 0), (0, 2), (0, 1)]),
            ([(1, 1), (2, 1), (3, 1)], [(1, 0), (0, 0), (2, 0)]),
            ([(3, 6), (4, 6), (5, 6), (4, 5)], [(0, 1), (1, 0), (1, 1), (2, 1)]),
        ],
    )
    def test_eq(self, coords1, coords2):
        assert WoodokuShape(coords1) == WoodokuShape(coords2)
        assert hash(WoodokuShape(coords1)) == hash(WoodokuShape(coords2))

    @pytest.mark.parametrize(
        "coords1, coords2",
        [
            ([(0, 0), (0, 1), (0, 2)], [(0, 0), (0, 1)]),
            ([(1, 1), (2, 1), (3, 1)], [(0, 0), (1, 0)]),
            ([(3, 6), (4, 6), (5, 6), (4, 5)], [(0, 1), (1, 0), (1, 1)]),
        ],
    )
    def test_not_eq_part(self, coords1, coords2):
        assert WoodokuShape(coords1) != WoodokuShape(coords2)
        assert hash(WoodokuShape(coords1)) != hash(WoodokuShape(coords2))

    @pytest.mark.parametrize(
        "coords1, coords2",
        [
            ([(0, 0), (0, 1), (0, 2)], [(0, 1), (0, 1), (1, 2)]),
            ([(1, 1), (2, 1), (3, 1)], [(0, 0), (2, 0), (2, 0)]),
            ([(3, 6), (4, 6), (5, 6), (4, 5)], [(0, 1), (1, 1), (1, 1), (2, 1)]),
        ],
    )
    def test_not_eq_diff_coord(self, coords1, coords2):
        assert WoodokuShape(coords1) != WoodokuShape(coords2)
        assert hash(WoodokuShape(coords1)) != hash(WoodokuShape(coords2))

    @pytest.mark.parametrize(
        "coords1, x, y, coords2",
        [
            ([(0, 0)], 0, 0, [(0, 0)]),
            ([(0, 0)], 1, 0, [(1, 0)]),
            ([(0, 0), (1, 0), (2, 0)], 1, 1, [(1, 1), (2, 1), (3, 1)]),
            ([(0, 1), (1, 0), (1, 1), (2, 1)], 3, 5, [(3, 6), (4, 6), (5, 6), (4, 5)]),
        ],
    )
    def test_map_to_board_at(self, coords1, x, y, coords2):
        assert set(WoodokuShape(coords1).map_to_board_at(x, y)) == set(coords2)
