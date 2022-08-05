from typing import Tuple

import torch


class ExperienceReplay:
    def __init__(self, length: int) -> None:
        pass
        # self.experience_replay = deque(maxlen=length)

    def collect(
        self, experience: Tuple[torch.Tensor, int, float, torch.Tensor]
    ) -> None:
        """
        Args:
            experience: list of state, action, reward, next_state
        """
        pass
        # self.experience_replay.append(experience)

    def sample_from_experience(
        self, sample_size: int
    ) -> Tuple[torch.Tensor, int, float, torch.Tensor]:
        pass
        # if len(self.experience_replay) < sample_size:
        #     sample_size = len(self.experience_replay)
        # sample = random.sample(self.experience_replay, sample_size)

        # state = torch.tensor([exp[0] for exp in sample]).float()
        # action = torch.tensor([exp[1] for exp in sample]).float()
        # reward = torch.tensor([exp[2] for exp in sample]).float()
        # next_state = torch.tensor([exp[3] for exp in sample]).float()
        # return state, action, reward, next_state
