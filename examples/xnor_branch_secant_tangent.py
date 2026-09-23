import math
from copy import deepcopy

from threeplusone import (
    ThreePlusOneMLP,
    add_transverse_vector_seed,
    centered_singleton_seed,
    epoch_transverse_matrix,
    xnor,
)

from xnor_sgd_tail_scaling import one_epoch_phase_contraction


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


def q(net, unit):
    return [
        net.output_w[unit + 1],
        net.hidden_w[unit][0],
        net.hidden_w[unit][1],
        net.hidden_w[unit][2],
    ]


def norm(v):
    return math.sqrt(sum(x * x for x in v))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def matvec(m, v):
    return [sum(m[i][j] * v[j] for j in range(4)) for i in range(4)]


if __name__ == "__main__":
    data = xnor()
    net = net0()
    checkpoints = (10_000, 100_000, 1_000_000)
    k = 0

    print(
        "N,R,secant_gain,tangent_gain,rho_ratio,rho_fd,"
        "action_ratio,action_fd,NlogN_defect"
    )

    for epoch in range(1, checkpoints[-1] + 1):
        for x, t in data:
            net.train_one(x, t)

        if epoch != checkpoints[k]:
            continue

        qA = q(net, 0)
        qB = q(net, 1)
        D = [a - b for a, b in zip(qA, qB)]
        R = norm(D)
        v = [x / R for x in D]

        # Tangential split of the equal B pair uses the representative B unit.
        tangent_map = epoch_transverse_matrix(
            net,
            data,
            representative_unit=1,
        )

        after = deepcopy(net)
        for x, t in data:
            after.train_one(x, t)

        qA2 = q(after, 0)
        qB2 = q(after, 1)
        D2 = [a - b for a, b in zip(qA2, qB2)]
        R2 = norm(D2)
        v2 = [x / R2 for x in D2]

        secant_gain = R2 / R
        tangent_vector = matvec(tangent_map, v)
        tangent_gain = dot(v2, tangent_vector)
        rho_ratio = tangent_gain / secant_gain
        action_ratio = -math.log(abs(rho_ratio)) / 3.0

        rho_fd, action_fd = one_epoch_phase_contraction(net, data)

        print(
            f"{epoch},"
            f"{R:.15g},"
            f"{secant_gain:.15g},"
            f"{tangent_gain:.15g},"
            f"{rho_ratio:.15g},"
            f"{rho_fd:.15g},"
            f"{action_ratio:.15g},"
            f"{action_fd:.15g},"
            f"{epoch * math.log(epoch) * (secant_gain - tangent_gain):.15g}"
        )

        k += 1
        if k == len(checkpoints):
            break
