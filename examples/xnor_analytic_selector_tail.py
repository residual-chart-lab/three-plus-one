import math
from copy import deepcopy

from threeplusone import (
    add_transverse_vector_seed,
    centered_singleton_seed,
    sample_transverse_matrix,
    transverse_residual,
    xnor,
)
from threeplusone.core import ThreePlusOneMLP

from xnor_sgd_tail_scaling import (
    local_state,
    one_epoch_phase_contraction,
    set_local_state,
    train_epoch,
)


def centered_ray_net() -> ThreePlusOneMLP:
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


def symmetrize_trio(net):
    work = deepcopy(net)
    states = [local_state(work, i) for i in range(3)]
    mean = [
        sum(states[i][j] for i in range(3)) / 3.0
        for j in range(4)
    ]
    for i in range(3):
        set_local_state(work, i, mean)
    return work


def matvec(matrix, vector):
    return [
        sum(matrix[i][j] * vector[j] for j in range(len(vector)))
        for i in range(len(matrix))
    ]


def addvec(a, b):
    return [a[i] + b[i] for i in range(4)]


def local_quadratic_sources(net, x, target, direction):
    h, y = net._forward(x)
    hv = float(h[0])
    d = (float(target) - y) * y * (1.0 - y)
    a = float(net.output_w[1])
    eta = float(net.learning_rate)

    g = hv * (1.0 - hv)
    gp = g * (1.0 - 2.0 * hv)
    gpp = g * (1.0 - 6.0 * hv + 6.0 * hv * hv)

    xhat = (1.0, float(x[0]), float(x[1]))
    va = float(direction[0])
    vw = tuple(float(direction[j + 1]) for j in range(3))
    s = sum(xhat[j] * vw[j] for j in range(3))
    c = 1.0 / math.sqrt(6.0)

    q_out = [
        eta * d * c * 0.5 * gp * s * s,
        0.0,
        0.0,
        0.0,
    ]

    cross_coeff = eta * d * c * gp * va * s
    q_cross = [0.0] + [cross_coeff * xx for xx in xhat]

    curvature_coeff = eta * d * c * 0.5 * a * gpp * s * s
    q_curvature = [0.0] + [curvature_coeff * xx for xx in xhat]

    return q_out, q_cross, q_curvature, {
        "d": abs(d),
        "g": g,
        "gp": abs(gp),
        "gpp": abs(gpp),
        "a": abs(a),
        "s": abs(s),
    }


def epoch_source_decomposition(net, data, direction):
    work = deepcopy(net)
    linear = [float(v) for v in direction]
    sources = {
        "out": [0.0] * 4,
        "cross": [0.0] * 4,
        "curvature": [0.0] * 4,
    }
    stats = {"d": [], "g": [], "gp": [], "gpp": [], "a": [], "s": []}

    for x, target in data:
        step = sample_transverse_matrix(work, x, target)
        q_out, q_cross, q_curvature, local_stats = local_quadratic_sources(
            work, x, target, linear
        )

        for key in sources:
            sources[key] = matvec(step, sources[key])

        sources["out"] = addvec(sources["out"], q_out)
        sources["cross"] = addvec(sources["cross"], q_cross)
        sources["curvature"] = addvec(sources["curvature"], q_curvature)

        for key, value in local_stats.items():
            stats[key].append(value)

        linear = matvec(step, linear)
        work.train_one(x, target)

    return linear, sources, {
        key: sum(values) / len(values)
        for key, values in stats.items()
    }


if __name__ == "__main__":
    data = xnor()
    ray = centered_ray_net()
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
        "N,r,va,vw_norm,mean_d,N_mean_d,mean_g,logN_mean_g,"
        "mean_gp,logN_mean_gp,mean_gpp,logN_mean_gpp,"
        "mean_a,mean_a_over_logN,mean_s,"
        "lambda,nu_out,nu_cross,nu_curvature,nu_total,"
        "action_out,action_cross,action_curvature,action_total,"
        "measured_action,NlogN_action_total"
    )

    checkpoint_index = 0
    for epoch in range(1, checkpoints[-1] + 1):
        train_epoch(ray, data)
        if epoch != checkpoints[checkpoint_index]:
            continue

        z = transverse_residual(ray)
        radial = [value.real for value in z]
        r = math.sqrt(sum(value * value for value in radial))
        direction = tuple(value / r for value in radial)

        coarse = symmetrize_trio(ray)
        linear, sources, stats = epoch_source_decomposition(
            coarse, data, direction
        )
        lam = math.sqrt(sum(value * value for value in linear))
        output_direction = tuple(value / lam for value in linear)

        projected = {
            key: sum(output_direction[i] * vec[i] for i in range(4))
            for key, vec in sources.items()
        }
        nu_total = sum(projected.values())

        action = {
            key: projected[key] * r / lam
            for key in projected
        }
        action_total = nu_total * r / lam
        _, measured_action = one_epoch_phase_contraction(ray, data)

        logn = math.log(epoch)
        vw_norm = math.sqrt(sum(value * value for value in direction[1:]))

        print(
            f"{epoch},"
            f"{r:.15g},"
            f"{direction[0]:.15g},"
            f"{vw_norm:.15g},"
            f"{stats['d']:.15g},"
            f"{epoch * stats['d']:.15g},"
            f"{stats['g']:.15g},"
            f"{logn * stats['g']:.15g},"
            f"{stats['gp']:.15g},"
            f"{logn * stats['gp']:.15g},"
            f"{stats['gpp']:.15g},"
            f"{logn * stats['gpp']:.15g},"
            f"{stats['a']:.15g},"
            f"{stats['a'] / logn:.15g},"
            f"{stats['s']:.15g},"
            f"{lam:.15g},"
            f"{projected['out']:.15g},"
            f"{projected['cross']:.15g},"
            f"{projected['curvature']:.15g},"
            f"{nu_total:.15g},"
            f"{action['out']:.15g},"
            f"{action['cross']:.15g},"
            f"{action['curvature']:.15g},"
            f"{action_total:.15g},"
            f"{measured_action:.15g},"
            f"{epoch * logn * action_total:.15g}"
        )

        checkpoint_index += 1
        if checkpoint_index == len(checkpoints):
            break
