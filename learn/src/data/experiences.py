import numpy as np

from jaxtyping import Float, Int, jaxtyped

import torch
from typeguard import typechecked
from woodoku.env import observation_space_d, action_space_d


class ExperienceReplay:
    """
    A class to store experiences replay buffer for WoodokuLearn reinforcement learning training.

    Experiences are stored in a circular buffer, such that old experiences are automatically expired once the buffer is
    full.

    States need to be stored as float and passed through NN
    Actions can be discrete here so we use int
    Rewards although discrete in this case, but we will need to operate reward with float, so we will use float from the start

    Attributes:
        length: The length of the buffer.
        index: The index to store the next experience.
        is_full: Whether the buffer is full.
        state: The state array.
        action: The action array.
        reward: The reward array.
        next_state: The next state array.
    """

    def __init__(self, length: int) -> None:
        self.length = length
        self.index = 0
        self.is_full = False
        self.state = np.zeros((length, *observation_space_d))
        self.action = np.zeros((length, *action_space_d), dtype=np.int_)
        self.reward = np.zeros(length)
        self.next_state = np.zeros((length, *observation_space_d))

    def collect(
        self,
        experience: tuple[  # type: ignore[type-arg]
            Float[np.ndarray, "*state"],
            Int[np.ndarray, "*action"],
            float,
            Float[np.ndarray, "*state"],
        ],
    ) -> None:
        state, action, reward, next_state = experience
        self.state[self.index] = state
        self.action[self.index] = action
        self.reward[self.index] = reward
        self.next_state[self.index] = next_state
        # index wraps around such that old experience auto expire
        self.index = (self.index + 1) % self.length
        if self.index == 0:
            self.is_full = True

    # NOTE: example of type annotation for jaxtyped function
    @jaxtyped  # type: ignore[misc]
    @typechecked
    def sample_from_experience(
        self, sample_size: int
    ) -> tuple[
        Float[torch.Tensor, "batch *observation_space_d"],
        Int[torch.Tensor, "batch *action_space_d"],
        Float[torch.Tensor, "batch"],
        Float[torch.Tensor, "batch *observation_space_d"],
    ]:
        if not self.is_full:
            sample_size = min(self.index, sample_size)
        sample_indices = np.random.choice(
            self.index if not self.is_full else self.length,
            size=sample_size,
            replace=False,
        )
        state = torch.tensor(self.state[sample_indices])
        action = torch.tensor(self.action[sample_indices])
        reward = torch.tensor(self.reward[sample_indices])
        next_state = torch.tensor(self.next_state[sample_indices])
        return state, action, reward, next_state
