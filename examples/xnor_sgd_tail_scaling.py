import math
from copy import deepcopy

from threeplusone import (
    ThreePlusOneMLP,
    add_transverse_vector_seed,
    centered_singleton_seed,
    transverse_residual,
    xnor,
)


C_R = (
    2.0 / math.sqrt(6.0),
    -1.0 / math.sqrt(6.0),
    -1.0 / math.sqrt(6.0),
)
C_I = (
    0.0,
    1.0 / math.sqrt(2.0),
    -1.0 / math.sqrt(2.0),
)


def centered_net() -> ThreePlusOneMLP:
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


def local_state(net, unit):
    return [
        net.output_w[unit + 1],
        net.hidden_w[unit][0],
        net.hidden_w[unit][1],
        net.hidden_w[unit][2],
    ]


def set_local_state(net, unit, q):
    net.output_w[unit + 1] = q[0]
    net.hidden_w[unit][0] = q[1]
    net.hidden_w[unit][1] = q[2]
    net.hidden_w[unit][2] = q[3]


def rotate_copy_residual(net, angle):
    states = [local_state(net, i) for i in range(3)]
    means = [
        sum(states[i][j] for i in range(3)) / 3.0
        for j in range(4)
    ]
    c = math.cos(angle)
    s = math.sin(angle)

    rotated = [[0.0] * 4 for _ in range(3)]
    for j in range(4):
        re = sum(C_R[i] * states[i][j] for i in range(3))
        im = sum(C_I[i] * states[i][j] for i in range(3))
        re2 = c * re - s * im
        im2 = s * re + c * im
        for i in range(3):
            rotated[i][j] = means[j] + C_R[i] * re2 + C_I[i] * im2

    for i in range(3):
        set_local_state(net, i, rotated[i])


def train_epoch(net, data):
    for x, target in data:
        net.train_one(x, target)


def projected_phase(net, direction):
    z = transverse_residual(net)
    value = sum(direction[j] * z[j] for j in range(4))
    return math.atan2(value.imag, value.real)


def one_epoch_phase_contraction(ray_net, data, delta=1e-2):
    center = deepcopy(ray_net)
    plus = deepcopy(ray_net)
    minus = deepcopy(ray_net)

    rotate_copy_residual(plus, +delta)
    rotate_copy_residual(minus, -delta)

    train_epoch(center, data)
    train_epoch(plus, data)
    train_epoch(minus, data)

    z0 = transverse_residual(center)
    radial = [z.real for z in z0]
    norm = math.sqrt(sum(v * v for v in radial))
    direction = [v / norm for v in radial]

    phase_plus = projected_phase(plus, direction)
    phase_minus = projected_phase(minus, direction)
    phase_diff = math.atan2(
        math.sin(phase_plus - phase_minus),
        math.cos(phase_plus - phase_minus),
    )
    rho = phase_diff / (2.0 * delta)
    action = -math.log(abs(rho)) / 3.0
    return rho, action


def tail_observables(net, data):
    mse = net.mse(data)

    deltas = []
    errors2 = []
    hidden_g = []
    margins = []

    for x, target in data:
        h, y = net._forward(x)
        error = float(target) - y
        d = error * y * (1.0 - y)
        deltas.append(abs(d))
        errors2.append(error * error)

        # Signed output margin: positive when classification is correct.
        logit = math.log(y / (1.0 - y))
        margins.append(logit if target > 0.5 else -logit)

        for hv in h:
            hidden_g.append(hv * (1.0 - hv))

    output_nonbias = net.output_w[1:]
    output_norm = math.sqrt(sum(a * a for a in output_nonbias))
    hidden_norm = math.sqrt(
        sum(w * w for row in net.hidden_w for w in row)
    )

    return {
        "mse": mse,
        "mean_abs_delta": sum(deltas) / len(deltas),
        "mean_hidden_g": sum(hidden_g) / len(hidden_g),
        "min_margin": min(margins),
        "mean_margin": sum(margins) / len(margins),
        "output_norm": output_norm,
        "hidden_norm": hidden_norm,
        "max_output_abs": max(abs(a) for a in output_nonbias),
    }


if __name__ == "__main__":
    data = xnor()
    net = centered_net()
    checkpoints = (
        10_000,
        20_000,
        50_000,
        100_000,
        200_000,
        500_000,
        1_000_000,
    )

    print(
        "N,mse,N_mse,mean_abs_delta,N_delta,"
        "mean_hidden_g,min_margin,mean_margin,"
        "output_norm,output_norm_over_logN,"
        "hidden_norm,hidden_norm_over_loglogN,"
        "rho1,action1,NlogN_action1"
    )

    checkpoint_index = 0
    for epoch in range(1, checkpoints[-1] + 1):
        train_epoch(net, data)
        if epoch != checkpoints[checkpoint_index]:
            continue

        obs = tail_observables(net, data)
        rho, action = one_epoch_phase_contraction(net, data)
        logn = math.log(epoch)
        loglogn = math.log(logn)

        print(
            f"{epoch},"
            f"{obs['mse']:.15g},"
            f"{epoch * obs['mse']:.15g},"
            f"{obs['mean_abs_delta']:.15g},"
            f"{epoch * obs['mean_abs_delta']:.15g},"
            f"{obs['mean_hidden_g']:.15g},"
            f"{obs['min_margin']:.15g},"
            f"{obs['mean_margin']:.15g},"
            f"{obs['output_norm']:.15g},"
            f"{obs['output_norm'] / logn:.15g},"
            f"{obs['hidden_norm']:.15g},"
            f"{obs['hidden_norm'] / loglogn:.15g},"
            f"{rho:.15g},"
            f"{action:.15g},"
            f"{epoch * logn * action:.15g}"
        )

        checkpoint_index += 1
        if checkpoint_index == len(checkpoints):
            break
