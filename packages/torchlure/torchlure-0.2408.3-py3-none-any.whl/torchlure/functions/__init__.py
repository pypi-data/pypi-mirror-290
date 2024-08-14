from collections.abc import Callable
from typing import Literal

import einops as ein
import jaxtyping as jt
import torch as th
from torchtyping import TensorType

Reduction = Literal["none", "mean", "sum"]


def tanh_exp(x, threshold=3.0):
    """
    TanhExp(x) = x * tanh(exp(x))

    - Clamp is necessary to prevent overflow. Using th.where alone is insufficient;
        there might be issues when x is small.

    - TanhExp converges to 1 when x is large;  x*tanh(exp(x)) - x < 0f64 if x > 3
    """
    return th.where(
        x > threshold,
        x,
        x * th.tanh(th.exp(th.clamp(x, max=threshold))),
    )


def return_to_go(rewards: TensorType[..., "T"], gamma: float) -> TensorType[..., "T"]:
    if gamma == 1.0:
        return rewards.flip(-1).cumsum(-1).flip(-1)

    seq_len = rewards.shape[-1]
    rtgs = th.zeros_like(rewards)
    rtg = th.zeros_like(rewards[..., 0])

    for i in range(seq_len - 1, -1, -1):
        rtg = rewards[..., i] + gamma * rtg
        rtgs[..., i] = rtg

    return rtgs


def quantile_loss(y_pred, y_true, tau, reduction: Reduction = "mean"):
    errors = y_true - y_pred
    loss = th.max(tau * errors, (tau - 1) * errors)

    match reduction:
        case "none":
            return loss
        case "mean":
            return th.mean(loss)
        case "sum":
            return th.sum(loss)
        case _:
            raise ValueError(f"Invalid reduction mode: {reduction}")


def expectile_loss(y_pred, y_true, tau, reduction: Reduction = "mean"):
    errors = y_true - y_pred
    weight = th.where(errors > 0, tau, 1 - tau)
    loss = weight * errors**2

    match reduction:
        case "none":
            return loss
        case "mean":
            return th.mean(loss)
        case "sum":
            return th.sum(loss)
        case _:
            raise ValueError(f"Invalid reduction mode: {reduction}")


def unfold_window(
    tensor: jt.Float[th.Tensor, "... T C"],
    window_size: int,
    stride: int = 1,
) -> jt.Float[th.Tensor, "... T-W W C"]:
    *batch_dims, T, C = tensor.shape
    windows = tensor.unfold(-2, window_size, stride)
    windows = ein.rearrange(windows, "... c w -> ... w c")
    return windows


def rolling_apply(
    func: Callable[[jt.Float[th.Tensor, "B T in"]], jt.Float[th.Tensor, "B T out"]],
    tensor: jt.Float[th.Tensor, "B T C"],
    window_size: int,
    stride: int = 1,
) -> jt.Float[th.Tensor, "B T out"]:
    windows = unfold_window(tensor=tensor, window_size=window_size, stride=stride)
    batch_size = windows.size(0)
    path = ein.rearrange(windows, "b t w c -> (b t) w c")
    path = func(path)
    path = ein.rearrange(path, "(b t) c -> b t c", b=batch_size)
    return path
