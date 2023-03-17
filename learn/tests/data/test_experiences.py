import pytest
import numpy as np
from jaxtyping import install_import_hook, Int, Float
from typeguard import typechecked

with install_import_hook("learn", "typeguard.typechecked"):
    from learn.src.data.experiences import ExperienceReplay
    from woodoku.env import observation_space_d, action_space_d


@pytest.mark.parametrize("length", [(5)])
def test_init_experience(length: int) -> None:
    exp = ExperienceReplay(length)
    assert exp.state.shape == (length,) + observation_space_d
    assert exp.action.shape == (length,) + action_space_d
    assert exp.reward.shape == (length,)


@pytest.mark.parametrize(
    "experience",
    [
        (
            np.ones(observation_space_d, dtype=np.float_),
            np.ones(action_space_d, dtype=np.int_),
            8.0,
            np.zeros(observation_space_d, dtype=np.float_),
        )
    ],
)
@typechecked
def test_experience_collect_once(
    experience: tuple[Float[np.ndarray, "*state"], Int[np.ndarray, "*action"], float, Float[np.ndarray, "*state"]]
) -> None:
    exp = ExperienceReplay(10)
    exp.collect(experience)
    assert np.array_equal(exp.state[0], experience[0])
    assert exp.reward[0] == experience[2]
    assert exp.index == 1


@pytest.mark.parametrize(
    "experience",
    [
        (
            np.ones(observation_space_d, dtype=np.float_),
            np.ones(action_space_d, dtype=np.int_),
            8.0,
            np.zeros(observation_space_d, dtype=np.float_),
        )
    ],
)
@typechecked
def test_experience_collect_multi(
    experience: tuple[Float[np.ndarray, "*state"], Int[np.ndarray, "*action"], float, Float[np.ndarray, "*state"]]
) -> None:
    exp = ExperienceReplay(8)
    exp.collect(experience)
    exp.collect(experience)
    exp.collect(experience)
    assert np.array_equal(exp.state[0], experience[0])
    assert exp.reward[0] == experience[2]
    assert np.array_equal(exp.state[2], experience[0])
    assert np.array_equal(exp.action[2], experience[1])
    assert exp.index == 3


@pytest.mark.parametrize(
    "experience",
    [
        (
            np.ones(observation_space_d, dtype=np.float_),
            np.ones(action_space_d, dtype=np.int_),
            8.0,
            np.zeros(observation_space_d, dtype=np.float_),
        )
    ],
)
@typechecked
def test_experience_wraps(
    experience: tuple[Float[np.ndarray, "*state"], Int[np.ndarray, "*action"], float, Float[np.ndarray, "*state"]]
) -> None:
    exp = ExperienceReplay(4)
    for _ in range(5):
        exp.collect(experience)
    assert exp.index == 1

    for _ in range(7):
        exp.collect(experience)
    assert exp.index == 0


@pytest.mark.parametrize(
    "length, count, batch_size, experience",
    [
        (
            10,
            4,
            8,
            (
                np.ones(observation_space_d, dtype=np.float_),
                np.ones(action_space_d, dtype=np.int_),
                8.0,
                np.zeros(observation_space_d, dtype=np.float_),
            ),
        ),
        (
            8,
            12,
            4,
            (
                np.ones(observation_space_d, dtype=np.float_),
                np.ones(action_space_d, dtype=np.int_),
                8.0,
                np.zeros(observation_space_d, dtype=np.float_),
            ),
        ),
        (
            12,
            8,
            4,
            (
                np.ones(observation_space_d, dtype=np.float_),
                np.ones(action_space_d, dtype=np.int_),
                8.0,
                np.zeros(observation_space_d, dtype=np.float_),
            ),
        ),
    ],
)
@typechecked
def test_sample_from_experience(
    length: int,
    count: int,
    batch_size: int,
    experience: tuple[Float[np.ndarray, "*state"], Int[np.ndarray, "*action"], float, Float[np.ndarray, "*state"]],
) -> None:
    exp = ExperienceReplay(length)
    for _ in range(count):
        exp.collect(experience)

    samples = exp.sample_from_experience(batch_size)
    assert samples[0].shape == (min(exp.index, batch_size),) + observation_space_d
    assert samples[1].shape == (min(exp.index, batch_size),) + action_space_d
    assert samples[2].shape == (min(exp.index, batch_size),)
