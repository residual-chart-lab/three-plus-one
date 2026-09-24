"""Future-readout coordinates for the full four-channel tangent state.

At checkpoints where the four-row observability matrix O_n is invertible,
the tangent state x_n can be represented by its next four phase readouts

    z_n = O_n x_n
        = (y_n, y_{n+1}, y_{n+2}, y_{n+3}).

In these coordinates the one-epoch tangent update is necessarily a
time-varying companion map: the first three coordinates shift, while the
fourth is a linear combination of the previous four.

This diagnostic constructs that map at high precision from the exact-binary
training checkpoints used by xnor_future_observability.py.
"""
from copy import deepcopy

from mpmath import mp

from threeplusone import (
    ThreePlusOneMLP,
    add_transverse_vector_seed,
    centered_singleton_seed,
    xnor,
)

from xnor_future_observability import observations


def train_epoch(net, data):
    for x, target in data:
        net.train_one(x, target)


def matmul(a, b):
    return a * b


def checkpoint_coordinates(net, epoch):
    mp.dps = 120
    rows, _, _ = observations(mp, net, horizon=4)
    O = mp.matrix(rows[:4])
    shifted = mp.matrix(rows[1:5])

    det_o = mp.det(O)
    if det_o == 0:
        raise RuntimeError("observability matrix is singular")

    companion = shifted * O**-1

    ideal = mp.matrix([
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [0, 0, 0, 0],
    ])
    shift_error = max(
        abs(companion[i, j] - ideal[i, j])
        for i in range(3)
        for j in range(4)
    )

    last = [companion[3, j] for j in range(4)]

    binomial = [mp.mpf(-1), mp.mpf(4), mp.mpf(-6), mp.mpf(4)]
    defect = [last[j] - binomial[j] for j in range(4)]
    cubic_mode = [mp.mpf(1), mp.mpf(-3), mp.mpf(3), mp.mpf(-1)]
    denom = sum(x * x for x in cubic_mode)
    epsilon = sum(defect[j] * cubic_mode[j] for j in range(4)) / denom
    residual = [
        defect[j] - epsilon * cubic_mode[j]
        for j in range(4)
    ]
    residual_norm = mp.sqrt(sum(x * x for x in residual))

    print(
        "epoch",
        epoch,
        "detO",
        mp.nstr(det_o, 30),
        "shift_error",
        mp.nstr(shift_error, 12),
        "recurrence",
        [mp.nstr(x, 30) for x in last],
        "epsilon",
        mp.nstr(epsilon, 30),
        "N_epsilon",
        mp.nstr(epoch * epsilon, 30),
        "defect_residual_norm",
        mp.nstr(residual_norm, 20),
        flush=True,
    )

    return companion


if __name__ == "__main__":
    data = xnor()
    net = ThreePlusOneMLP(
        epsilon=1.0,
        seed_pattern=centered_singleton_seed(4),
    )
    add_transverse_vector_seed(
        net,
        direction=(1.0, 0.0, 0.0, 0.0),
        amplitude=0.1,
        phase=0.0,
    )

    checkpoints = (728, 10_000, 100_000, 1_000_000)
    for epoch in range(1, checkpoints[-1] + 1):
        train_epoch(net, data)
        if epoch in checkpoints:
            checkpoint_coordinates(deepcopy(net), epoch)
