class DqnNetwork:
    def __init__(self) -> None:
        pass

    def dummy(self) -> None:
        pass

    def dummy2(self) -> None:
        pass

    def dummy3(self) -> None:
        pass

    def dummy4(self) -> None:
        pass

    pass
    # def __init__(self, layer_size_list, lr, seed=1423):
    #     torch.manual_seed(seed)

    #     # policy net is the Q function
    #     self.policy_net = self.create_network(layer_size_list)
    #     # target net is the same, but as a shadow of policy net,
    #     # where it is not gradient update, but rather inherit the paramter of
    #     policy ner every 5 step (see training loop) self.target_net =
    #     copy.deepcopy(self.policy_net)

    #     self.loss_fn = torch.nn.MSELoss() # the loss function
    #     self.optimizer = torch.optim.Adam(self.policy_net.parameters(), lr=lr)

    #     self.step = 0
    #     self.gamma = torch.tensor(0.95).float()

    # def create_network(self, layer_size_list:List[int]):
    #     """
    #         Build a MLP with tanh activation in between layers,
    #         layer dimention specified by layer_size_list

    #         Args:
    #             layer_size_list: list of input to a linear layer
    #     """
    #     assert len(layer_size_list) > 1

    #     layers = []
    #     for i in range(len(layer_size_list) - 1):
    #         linear = nn.Linear(layer_size_list[i], layer_size_list[i + 1])

    #         if i < len(layer_size_list) - 2:
    #           activation = nn.Tanh()
    #         else:
    #           activation = nn.Identity()

    #         layers += (linear, activation)
    #     return nn.Sequential(*layers)

    # def load_pretrained_model(self, model_path):
    #     self.policy_net.load_state_dict(torch.load(model_path))

    # def save_trained_model(self, model_path="cartpole-dqn.pth"):
    #     torch.save(self.policy_net.state_dict(), model_path)
