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
    for any test with with fixture/parameters

    Args:
        init_score (int): score to setup
        init_streak (int): streak to setup
        winnings (Iterable[Tuple[int, int]]): Contains a ordered list of winning
            information (block placed, groups completed) to calculate score
        scorekeeper (ScoreAgent): a new scorekeeper instance for this test
    """
    # setup the real world initial state if needed
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
        scorekeeper.calculate_winning(score_before_streak, 0)
        # init_streak + init_streak * 18 + init_streak
        for _ in range(init_streak):
            scorekeeper.calculate_winning(1, 1)
    # elif init_score > 0 and not init_streak:
    # scorekeeper.calculate_winning(init_score, 0)
    assert init_score == scorekeeper.get_score()

    # apply the winnings
    for winning in winnings:
        scorekeeper.calculate_winning(*winning)
