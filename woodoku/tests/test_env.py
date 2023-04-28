import numpy as np
import pytest

from woodoku.env import Action, Observation, WoodokuGameEnv


def to_action(shape_choice: int, x: int, y: int) -> Action:
    return Action(np.array([shape_choice, x, y], dtype=np.int_))


class TestWoodokuGameEnv:
    @pytest.mark.parametrize(
        "choices, expected",
        [
            ([(0, 4, 4)], False),
            ([(0, 0, 0)], False),
            ([(0, 0, 0), (1, 0, 4), (2, 4, 0), (2, 4, 4)], False),  # placing 4 shape far apart should not end the game
            ([(0, 0, 0), (0, 4, 4)], False),  # choosing an unavailable shape
            # it is really hard to end the game without knowing what shapes are given, so there will be no such test case
        ],
    )
    def test_step_ends(self, choices: list[tuple[int, int, int]], expected: bool) -> None:
        env = WoodokuGameEnv()
        actions = [to_action(*choice) for choice in choices]
        for action in actions:
            _, _, done = env.step(action)
        assert done == expected

    @pytest.mark.parametrize(
        "choices, expected",
        [
            ([(0, 4, 4)], True),
            ([(0, 0, 0)], True),
            ([(0, 0, 0), (1, 1, 4), (2, 4, 1)], True),  # placing 4 shape far apart should not end the game
            ([(0, 0, 0), (0, 4, 4)], False),  # choosing an unavailable shape
            ([(0, 0, 0), (1, 0, 0), (2, 0, 0), (1, 0, 0)], False),  # placing shapes repeatedly on the same location
        ],
    )
    def test_step_is_all_positive_reward(self, choices: list[tuple[int, int, int]], expected: bool) -> None:
        env = WoodokuGameEnv()
        actions = [to_action(*choice) for choice in choices]
        all_positive = True
        for action in actions:
            _, reward, _ = env.step(action)
            if reward < 0:
                all_positive = False
        assert all_positive == expected

    def test_reset(self) -> None:
        env = WoodokuGameEnv()
        obs = env.reset()
        assert isinstance(obs, Observation)
