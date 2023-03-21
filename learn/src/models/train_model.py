# pylint: disable=unused-argument
from __future__ import annotations
from jaxtyping import Int
import numpy as np

from learn.src.models.model import DQN_Network
from woodoku.env import Action


def get_action(model: DQN_Network, state: Int[np.ndarray, "*state"], action_space_len: int, epsilon: float) -> Action:  # type: ignore[type-arg]
    raise NotImplementedError


def train(model: DQN_Network, batch_size: int) -> None:
    raise NotImplementedError


# def train_loop(model, optimizer, loss_fn, train_loader, num_epochs):
# for epoch in range(num_epochs):
#     for inputs, targets in train_loader:
#         # Zero the gradients
#         optimizer.zero_grad()

#         # Forward pass
#         outputs = model(inputs)
#         loss = loss_fn(outputs, targets)

#         # Backward pass
#         loss.backward()

#         # Update model parameters
#         optimizer.step()

#     # Print training progress
#     print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {loss.item():.4f}")
