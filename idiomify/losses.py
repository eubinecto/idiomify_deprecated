"""
1. simple cosine similarity.
2. the.. what?
"""
import torch

cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)  # for now, use simple cosine sim.


def cosine_sim(Y: torch.Tensor, Y_hat: torch.Tensor) -> torch.Tensor:
    global cos
    loss = torch.sum(1 - cos(Y, Y_hat))  # sum up all the loss for this batch
    return loss

