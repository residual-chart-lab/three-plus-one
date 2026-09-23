import math
from copy import deepcopy

from threeplusone import (
    add_transverse_vector_seed,
    centered_singleton_seed,
    sample_transverse_matrix,
    transverse_residual,
    branch_ray_phase_derivative,
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




def hidden_epoch_vector(net, data, unit=0):
    work = deepcopy(net)
    before = work.hidden_w[unit][:]
    train_epoch(work, data)
    return [
        work.hidden_w[unit][j] - before[j]
        for j in range(3)
    ]


def hidden_epoch_cancellation(net, data, unit=0):
    work = deepcopy(net)
    contributions = []
    total = [0.0, 0.0, 0.0]

    for x, target in data:
        before = work.hidden_w[unit][:]
        work.train_one(x, target)
        delta = [
            work.hidden_w[unit][j] - before[j]
            for j in range(3)
        ]
        contributions.append(delta)
        for j in range(3):
            total[j] += delta[j]

    total_norm = math.sqrt(sum(v * v for v in total))
    l1_vector_norm = sum(
        math.sqrt(sum(v * v for v in delta))
        for delta in contributions
    )
    ratio = total_norm / l1_vector_norm if l1_vector_norm else 0.0
    return total_norm, l1_vector_norm, ratio



def hidden_logit_tail(net, data, unit=0):
    values = []
    for x, target in data:
        xhat = (1.0, float(x[0]), float(x[1]))
        u = sum(net.hidden_w[unit][j] * xhat[j] for j in range(3))
        h = 1.0 / (1.0 + math.exp(-u))
        g = h * (1.0 - h)
        values.append((u, g))
    return values


def hidden_displacement_from_initial(net, unit=0):
    base = [-1.0, -1.0, -1.0]
    delta = [net.hidden_w[unit][j] - base[j] for j in range(3)]
    norm = math.sqrt(sum(v * v for v in delta))
    return delta, norm


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
        "hidden_epoch_update,NlogN_hidden_epoch_update,"
        "hidden_cancel_ratio,logN_hidden_cancel_ratio,"
        "hidden_disp_norm,hidden_disp_over_loglogN,"
        "hidden_radial_update,NlogN_hidden_radial_update,hidden_update_cosine,"
        "u00,u01,u10,u11,min_abs_u,mean_abs_u,"
        "min_abs_u_over_loglogN,mean_abs_u_over_loglogN,"
        "lambda,nu_out,nu_cross,nu_curvature,nu_total,"
        "action_out,action_cross,action_curvature,action_total,"
        "exact_action,finite_action,NlogN_exact_action,NlogN_action_total"
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
        exact_rho = branch_ray_phase_derivative(ray, data)
        exact_action = -math.log(abs(exact_rho)) / 3.0
        _, finite_action = one_epoch_phase_contraction(ray, data)

        logn = math.log(epoch)
        hidden_update, hidden_abs_sum, cancel_ratio = hidden_epoch_cancellation(
            ray, data
        )
        logits = hidden_logit_tail(coarse, data)
        abs_logits = [abs(u) for u, _ in logits]
        hidden_disp, hidden_disp_norm = hidden_displacement_from_initial(coarse)
        hidden_epoch_vec = hidden_epoch_vector(coarse, data)
        hidden_epoch_vec_norm = math.sqrt(sum(v * v for v in hidden_epoch_vec))
        if hidden_disp_norm > 0.0:
            hidden_radial_update = sum(
                hidden_disp[j] * hidden_epoch_vec[j]
                for j in range(3)
            ) / hidden_disp_norm
        else:
            hidden_radial_update = 0.0
        if hidden_disp_norm > 0.0 and hidden_epoch_vec_norm > 0.0:
            hidden_update_cosine = hidden_radial_update / hidden_epoch_vec_norm
        else:
            hidden_update_cosine = 0.0
        loglogn = math.log(logn)
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
            f"{hidden_update:.15g},"
            f"{epoch * logn * hidden_update:.15g},"
            f"{cancel_ratio:.15g},"
            f"{logn * cancel_ratio:.15g},"
            f"{hidden_disp_norm:.15g},"
            f"{hidden_disp_norm / loglogn:.15g},"
            f"{hidden_radial_update:.15g},"
            f"{epoch * logn * hidden_radial_update:.15g},"
            f"{hidden_update_cosine:.15g},"
            f"{logits[0][0]:.15g},"
            f"{logits[1][0]:.15g},"
            f"{logits[2][0]:.15g},"
            f"{logits[3][0]:.15g},"
            f"{min(abs_logits):.15g},"
            f"{sum(abs_logits)/len(abs_logits):.15g},"
            f"{min(abs_logits)/loglogn:.15g},"
            f"{(sum(abs_logits)/len(abs_logits))/loglogn:.15g},"
            f"{lam:.15g},"
            f"{projected['out']:.15g},"
            f"{projected['cross']:.15g},"
            f"{projected['curvature']:.15g},"
            f"{nu_total:.15g},"
            f"{action['out']:.15g},"
            f"{action['cross']:.15g},"
            f"{action['curvature']:.15g},"
            f"{action_total:.15g},"
            f"{exact_action:.15g},"
            f"{finite_action:.15g},"
            f"{epoch * logn * exact_action:.15g},"
            f"{epoch * logn * action_total:.15g}"
        )

        checkpoint_index += 1
        if checkpoint_index == len(checkpoints):
            break
