# pylint: disable=unused-argument
from __future__ import annotations
from typing import Tuple


class Action:
    """
    The class representing the action.

    The first dimension is integer between 0 and 2, inclusive, representing which shape to choose. The second and the
    third dimensions are both integer between 0 and 8, inclusive, representing the x, y coordinates to place.
    """

    dimension: Tuple[int] = (3,)
    range: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]] = (
        (0, 3),
        (0, 9),
        (0, 9),
    )
    data: Tuple[int, int, int]

    @staticmethod
    def random_action() -> Action:
        """
        Generate a random action within the range.

        Returns:

        """
        pass

    def get_action(
        self, model: int, state: int, action_space_len: int, epsilon: int
    ) -> None:
        pass
        # # We do not require gradient at this point, because this function will be
        # used either # during experience collection or during inference

        # with torch.no_grad():
        #     Qp = model.policy_net(torch.from_numpy(state).float())

        # ## TODO: select and return action based on epsilon-greedy
        # # From the 4 states predict the a list of Expected cumulative rewards
        # given all state and action pair # (seems like the naive brute force way)

        # # Pick the action with the maximum expected cumulative reward Q*(s,a)

        # # with probability epsilon:
        # # do random exploration (sample a random action)
        # if torch.rand(1).item() <= epsilon:
        #     action = torch.randint(0, action_space_len, (1,))
        # else:  # stick with exploitation
        #     q, action = Qp.max(axis=0)

        # return action


def train(model: int, batch_size: int) -> None:
    pass
    # state, action, reward, next_state = memory.sample_from_experience(
    #     sample_size=batch_size
    # )

    # # TODO: predict expected return of current state using main network

    # # Q(s,a)
    # # version 1
    # # chooses the optimal action in this batch to get Q reward
    # # (unrelistic for model with large to infinity number of action)
    # Q_pred, _ = model.policy_net(state).max(axis=1)

    # # version 2
    # # Q(s,a) chooses the reward of the actions sampled
    # # Q_pred = model.policy_net(state)[torch.arange(batch_size), action.long()]

    # # TODO: get target return using target network
    # Q_next, _ = model.target_net(next_state).max(axis=1)
    # # (r + gamma * Q*(next_state, a)
    # target = reward + model.gamma * Q_next

    # # TODO: Optimize the model
    # loss = model.loss_fn(Q_pred, target)
    # model.optimizer.zero_grad()
    # loss.backward(retain_graph=True)
    # model.optimizer.step()

    # # this updates the target net to the parameter of the policy net every 5 step
    # # the gradient of the two network is not simutaneously update to avoid
    # overshoot when both are updated # therefore only policy net is backproped
    # and updated, and we let target net lag behind.
    # model.step += 1
    # if model.step % 5 == 0:
    #     model.target_net.load_state_dict(model.policy_net.state_dict())

    # return loss.item()
