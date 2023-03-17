import copy
from typing import Union
import torch
from torch import nn
from jaxtyping import Float
from woodoku.env import observation_space_d, action_space_d  # do not delete


class DQN_Network:
    def __init__(self, layer_size_list: list[int], lr: float, seed: int = 1423):
        torch.manual_seed(seed)

        # policy net is the Q function
        self._policy_net = self.create_network(layer_size_list)
        # target net is the same, but as a shadow of policy net,
        # where it is not gradient update, but rather inherit the parameter of policy ner every 5 step (see training loop)
        self._target_net = copy.deepcopy(self._policy_net)
        """
        ChatGPT:
        In Q-learning, the target Q-values used to update the Q-network
        depend on the Q-values predicted by the same network. This means that as the
        Q-network learns to predict better Q-values, the targets used to update the
        network also change, leading to a feedback loop that can cause instability in
        the learning process.
        
        By using a target network, the Q-values used for the target do not depend on the
        Q-values predicted by the policy network, but rather on a separate network with
        fixed parameters. This helps to stabilize the learning process by reducing the
        correlation between the target and predicted Q-values, and can result in faster
        convergence and improved performance.
        
        Without a target network, the Q-learning algorithm may still learn and converge,
        but it may be slower and less stable. Overestimation of Q-values can lead to
        suboptimal policies, and instability can result in slower convergence and
        difficulty in training deep Q-networks.
        """

        self.loss_fn = torch.nn.MSELoss()  # the loss function
        # NOTE: only policy_net is passed in for optimizer to do back propagation and not target_net
        self.optimizer = torch.optim.Adam(self._policy_net.parameters(), lr=lr)

        self.step = 0
        self.gamma = torch.tensor(0.95).float()

    # TODO: require shape testing for success and failure case
    def policy_net(self, state: Float[torch.Tensor, "*observation_space_d"]) -> Float[torch.Tensor, "*action_space_d"]:
        return self._policy_net(state)  # type: ignore[no-any-return]

    def target_net(self, state: Float[torch.Tensor, "*observation_space_d"]) -> Float[torch.Tensor, "*action_space_d"]:
        return self._target_net(state)  # type: ignore[no-any-return]

    def update_target_net(self) -> None:
        self._target_net.load_state_dict(self._policy_net.state_dict())

    def create_network(self, layer_size_list: list[int]) -> nn.Sequential:
        """
        Build a MLP with tanh activation in between layers,
        layer dimension specified by layer_size_list

        Args:
            layer_size_list: list of input to a linear layer
        """
        assert len(layer_size_list) > 1

        layers = []
        for i in range(len(layer_size_list) - 1):
            linear = nn.Linear(layer_size_list[i], layer_size_list[i + 1])

            if i < len(layer_size_list) - 2:
                activation: Union[nn.Tanh, nn.Identity] = nn.Tanh()
            else:
                activation = nn.Identity()

            layers += [linear, activation]
        return nn.Sequential(*layers)

    def load_pretrained_model(self, model_path: str) -> None:
        self._policy_net.load_state_dict(torch.load(model_path))

    def save_trained_model(self, model_path: str = "woodokulearn-dqn.pth") -> None:
        torch.save(self._policy_net.state_dict(), model_path)
