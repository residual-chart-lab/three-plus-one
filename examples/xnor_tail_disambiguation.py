import math

from threeplusone import (
    ThreePlusOneMLP,
    add_transverse_vector_seed,
    branch_ray_phase_derivative,
    centered_singleton_seed,
    xnor,
)


def net0():
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
    return net


def train_epoch(net, data):
    for x, target in data:
        net.train_one(x, target)


def coarse_trio_hidden_row(net):
    return [
        sum(net.hidden_w[i][j] for i in range(3)) / 3.0
        for j in range(3)
    ]


def logits_from_row(row):
    w0, w1, w2 = row
    return (
        w0,
        w0 + w2,
        w0 + w1,
        w0 + w1 + w2,
    )


if __name__ == "__main__":
    data = xnor()
    net = net0()
    checkpoints = (
        100_000,
        200_000,
        500_000,
        1_000_000,
        2_000_000,
        5_000_000,
        10_000_000,
    )

    print(
        "N,action,NlogN_action,"
        "u00,u01,u10,u11,"
        "abs_u11_over_logN,abs_u11_over_loglogN"
    )

    idx = 0
    for epoch in range(1, checkpoints[-1] + 1):
        train_epoch(net, data)
        if epoch != checkpoints[idx]:
            continue

        rho = branch_ray_phase_derivative(net, data)
        action = -math.log(abs(rho)) / 3.0
        u00, u01, u10, u11 = logits_from_row(coarse_trio_hidden_row(net))
        logn = math.log(epoch)
        loglogn = math.log(logn)

        print(
            f"{epoch},"
            f"{action:.15g},"
            f"{epoch * logn * action:.15g},"
            f"{u00:.15g},"
            f"{u01:.15g},"
            f"{u10:.15g},"
            f"{u11:.15g},"
            f"{abs(u11)/logn:.15g},"
            f"{abs(u11)/loglogn:.15g}"
        )

        idx += 1
        if idx == len(checkpoints):
            break
