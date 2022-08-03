from typing import Iterable, Tuple

import pytest
from woodoku.entity.score_agent import GROUP_POINTS, STREAK_POINTS, ScoreAgent

# Scoring Rules:
#   1. 1 point for each block placed
#   2. A single groups scores 18 points
#   3. Each streak adds 10 points on top of the previous streak
#   4. Each additional combo adds 28 points


# pytest setup
# tuples are (No. blocks placed, No. groups completed)
@pytest.fixture(name="scorekeeper")
def fixture_scorekeeper() -> ScoreAgent:
    return ScoreAgent()


# Question... (just wanna know if there is a better way)
# Is there any way to use Mock or MagicMock to set the private state instead of
# a hack like this or accessing the private variable
# for example: I want to set up so that before testing the scorekeeper has a
# score of 42 and current streak of 1
@pytest.fixture(name="setup_and_apply_winnings", autouse=True)
def fixture_setup_and_apply_winnings(
    init_score: int,
    init_streak: int,
    winnings: Iterable[Tuple[int, int]],
    scorekeeper: ScoreAgent,
) -> None:
    """
    Automatically setup up scorekeeper and apply the winning to scorekeeper
    for any test with fixture/parameters

    Args:
        init_score (int): score to setup
        init_streak (int): streak to setup
        winnings (Iterable[Tuple[int, int]]): Contains a ordered list of winning
            information (block placed, groups completed) to calculate score
        scorekeeper (ScoreAgent): a new scorekeeper instance for this test
    """
    __score_agent_manual_setup(init_score, init_streak, scorekeeper)
    # apply the winnings
    for winning in winnings:
        scorekeeper.calculate_winning(*winning)


def __score_agent_manual_setup(
    init_score: int, init_streak: int, scorekeeper: ScoreAgent
) -> None:
    """setup the real world initial state if needed"""

    # get the score before setting up the streak by removing any score incurred
    # by the streaks first
    score_before_streak = (
        init_score
        # remove score added by blocks (init_streak * 1)
        - init_streak
        # remove score added by groups (init_streak * GROUP_POINTS)
        - init_streak * GROUP_POINTS
        # remove scores added by streaks (0 + 10 + 20... for a total init_streak
        # number of times i.e. [(n-1) * n]/2)
        - init_streak * (init_streak - 1) // 2 * STREAK_POINTS
    )
    if score_before_streak > 0:
        # add score_before_streak
        scorekeeper.calculate_winning(score_before_streak, 0)
        # loop `init_streak` times to setup streak
        for _ in range(init_streak):
            scorekeeper.calculate_winning(1, 1)
    assert (
        init_score == scorekeeper.get_score()
        and init_streak == scorekeeper.get_streak()
    ), "ScoreAgent setup failed"


class TestScoreAgent:
    # pylint: disable=too-many-arguments, unused-argument
    # Disabled since, test requires these arguments and unused arguments are
    # either implicitly used or it's a pytest format problem
    @pytest.mark.parametrize(
        ("init_score", "init_streak", "winnings", "expected_score"),
        [
            (0, 0, [(1, 0)], 1),
            (0, 0, [(1, 0), (2, 0), (3, 0), (5, 0), (3, 0)], 14),
            (0, 0, [(5, 0), (1, 0), (1, 0), (1, 0), (7, 0)], 15),
        ],
    )
    def test_block_placement(
        self,
        init_score: int,
        init_streak: int,
        winnings: Iterable[Tuple[int, int]],
        expected_score: int,
        scorekeeper: ScoreAgent,
    ) -> None:
        assert scorekeeper.get_score() == expected_score

    @pytest.mark.parametrize(
        ("init_score", "init_streak", "winnings", "expected_score"),
        [
            (0, 0, [(2, 1)], 20),
            (0, 0, [(1, 1), (4, 0)], 23),
            (0, 0, [(1, 1), (4, 0), (7, 1)], 48),
            (0, 0, [(1, 1), (4, 0), (1, 0), (5, 1)], 47),
            (0, 0, [(6, 0), (4, 0), (1, 0), (5, 1), (2, 0)], 36),
        ],
    )
    def test_group_block_interchange(
        self,
        winnings: Iterable[Tuple[int, int]],
        expected_score: int,
        scorekeeper: ScoreAgent,
    ) -> None:
        """test group winning and block winning in a interchanging fashion i.e. no streak"""
        assert scorekeeper.get_score() == expected_score

    @pytest.mark.parametrize(
        ("init_score", "init_streak", "winnings", "expected_score"),
        [
            (0, 0, [(3, 0), (1, 1), (3, 1)], 53),
            (
                0,
                0,
                [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 0), (2, 1), (3, 1)],
                26 + 7 * 18 + 10 + 20 + 30 + 40 + 10,
            ),
            (
                0,
                0,
                [(1, 1), (2, 1), (3, 1), (1, 0), (1, 1), (2, 1), (3, 1)],
                13 + 6 * 18 + 10 + 20 + 10 + 20,
            ),
        ],
    )
    def test_streaks(
        self,
        winnings: Iterable[Tuple[int, int]],
        expected_score: int,
        scorekeeper: ScoreAgent,
    ) -> None:
        """test how streaks behave"""
        assert scorekeeper.get_score() == expected_score

    @pytest.mark.parametrize(
        ("init_score", "init_streak", "winnings", "expected_score"),
        [
            (0, 0, [(1, 0), (3, 2), (2, 0), (1, 3)], 7 + 2 * 18 + 3 * 28),
            (0, 0, [(5, 5), (3, 0), (2, 0), (8, 3)], 18 + 2 * 18 + 6 * 28),
        ],
    )
    def test_combos(
        self,
        winnings: Iterable[Tuple[int, int]],
        expected_score: int,
        scorekeeper: ScoreAgent,
    ) -> None:
        """test how single combos behave"""
        assert scorekeeper.get_score() == expected_score

    @pytest.mark.parametrize(
        ("init_score", "init_streak", "winnings", "expected_score"),
        [
            (
                0,
                0,
                [(1, 1), (3, 2), (2, 2), (1, 0), (1, 3)],
                8 + 4 * 18 + 4 * 28 + 10 + 20,
            ),
            (
                0,
                0,
                [
                    (5, 5),
                    (4, 0),
                    (3, 0),
                    (2, 0),
                    (2, 1),
                    (8, 3),
                    (2, 1),
                    (3, 2),
                    (4, 0),
                    (2, 1),
                    (1, 1),
                ],
                36 + 7 * 18 + 7 * 28 + 10 + 20 + 30 + 10,
            ),
        ],
    )
    def test_combo_streak(
        self,
        winnings: Iterable[Tuple[int, int]],
        expected_score: int,
        scorekeeper: ScoreAgent,
    ) -> None:
        """test how single combos behave"""
        assert scorekeeper.get_score() == expected_score

    @pytest.mark.parametrize(
        ("init_score", "init_streak", "winnings", "expected_score"),
        [
            (1, 0, [(1, 0)], 2),
            (3, 0, [(4, 0)], 7),
            (5, 0, [(3, 0)], 8),
            (14, 0, [(5, 1)], 37),
            (82, 0, [(3, 1)], 103),
            (103, 1, [(4, 1)], 135),
            (327, 0, [(5, 3)], 406),
            (406, 1, [(5, 1)], 439),
            (478, 1, [(3, 1)], 509),
            (58, 0, [(3, 3)], 135),
            (135, 1, [(1, 1)], 164),
            (164, 2, [(3, 1)], 205),
            (132, 0, [(3, 2)], 181),
            (226, 0, [(2, 2)], 274),
            (73, 1, [(4, 2)], 133),
            (27, 0, [(3, 1)], 48),
            (48, 1, [(4, 1)], 80),
            (184, 2, [(5, 1)], 227),
            (227, 3, [(4, 1)], 279),
        ],
    )
    def test_real_game_scenarios(
        self,
        init_score: int,
        init_streak: int,
        winnings: Iterable[Tuple[int, int]],
        expected_score: int,
        scorekeeper: ScoreAgent,
    ) -> None:
        """expect to behave the same as the real world game scoring logs collected manually"""
        assert scorekeeper.get_score() == expected_score
