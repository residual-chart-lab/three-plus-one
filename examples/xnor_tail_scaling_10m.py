import math

from threeplusone import (
    ThreePlusOneMLP,
    add_transverse_vector_seed,
    centered_singleton_seed,
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


if __name__ == "__main__":
    data = xnor()
    net = net0()
    checkpoints = (1_000_000, 2_000_000, 5_000_000, 10_000_000)
    k = 0

    print(
        "N,action,NlogN_action,NlogNloglogN_action,"
        "da,da_over_loglogN,"
        "dbias,dwx,dwy,"
        "gA_mix_logN,gB_mix_logN,"
        "dh_mix_logN,dag_mix_logN"
    )

    for epoch in range(1, checkpoints[-1] + 1):
        for x, t in data:
            net.train_one(x, t)

        if epoch != checkpoints[k]:
            continue

        _, action = one_epoch_phase_contraction(net, data)
        logn = math.log(epoch)
        loglogn = math.log(logn)

        aA = net.output_w[1]
        aB = net.output_w[2]
        da = aA - aB

        dbias = net.hidden_w[0][0] - net.hidden_w[1][0]
        dwx = net.hidden_w[0][1] - net.hidden_w[1][1]
        dwy = net.hidden_w[0][2] - net.hidden_w[1][2]

        hA = net._forward([0.0, 1.0])[0][0]
        hB = net._forward([0.0, 1.0])[0][1]
        gA = hA * (1.0 - hA)
        gB = hB * (1.0 - hB)

        print(
            f"{epoch},"
            f"{action:.15g},"
            f"{epoch * logn * action:.15g},"
            f"{epoch * logn * loglogn * action:.15g},"
            f"{da:.15g},"
            f"{da / loglogn:.15g},"
            f"{dbias:.15g},"
            f"{dwx:.15g},"
            f"{dwy:.15g},"
            f"{gA * logn:.15g},"
            f"{gB * logn:.15g},"
            f"{(hA - hB) * logn:.15g},"
            f"{(aA * gA - aB * gB) * logn:.15g}"
        )

        k += 1
        if k == len(checkpoints):
            break
