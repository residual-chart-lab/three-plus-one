import math
from copy import deepcopy

from threeplusone import (
    ThreePlusOneMLP,
    add_transverse_vector_seed,
    centered_singleton_seed,
    xnor,
)


def ray_net():
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


def trio_coarse(net):
    work = deepcopy(net)
    out_mean = sum(work.output_w[i + 1] for i in range(3)) / 3.0
    hidden_mean = [
        sum(work.hidden_w[i][j] for i in range(3)) / 3.0
        for j in range(3)
    ]
    for i in range(3):
        work.output_w[i + 1] = out_mean
        work.hidden_w[i] = hidden_mean[:]
    return work


def hidden_preactivation(net, unit, x):
    row = net.hidden_w[unit]
    return row[0] + row[1] * float(x[0]) + row[2] * float(x[1])


def frozen_hidden_gradient_terms(net, unit, data):
    a = float(net.output_w[unit + 1])
    terms = []
    for x, target in data:
        h, y = net._forward(x)
        hv = float(h[unit])
        g = hv * (1.0 - hv)
        d = (float(target) - y) * y * (1.0 - y)
        coeff = net.learning_rate * a * d * g
        xhat = (1.0, float(x[0]), float(x[1]))
        terms.append({
            "x": tuple(x),
            "target": float(target),
            "h": hv,
            "u": hidden_preactivation(net, unit, x),
            "g": g,
            "gp": g * (1.0 - 2.0 * hv),
            "d": d,
            "coeff": coeff,
            "vec": tuple(coeff * xx for xx in xhat),
        })
    return terms


def vec_norm(v):
    return math.sqrt(sum(x * x for x in v))


def vec_sum(vectors):
    return tuple(sum(v[j] for v in vectors) for j in range(3))


def exact_hidden_epoch_update(net, unit, data):
    work = deepcopy(net)
    before = work.hidden_w[unit][:]
    train_epoch(work, data)
    return tuple(work.hidden_w[unit][j] - before[j] for j in range(3))


def coeff_walsh(terms):
    # XNOR order: 00(+), 01(-), 10(-), 11(+).
    c00, c01, c10, c11 = [t["coeff"] for t in terms]
    return {
        "bias": c00 + c01 + c10 + c11,
        "x1": c10 + c11,
        "x2": c01 + c11,
        "parity": c00 - c01 - c10 + c11,
    }


if __name__ == "__main__":
    data = xnor()
    net = ray_net()
    checkpoints = (10_000, 20_000, 50_000, 100_000, 200_000, 500_000, 1_000_000)

    header = [
        "N",
        "loglogN",
        "coarse_w0_over_loglog",
        "coarse_w1_over_loglog",
        "coarse_w2_over_loglog",
    ]
    for label in ("00", "01", "10", "11"):
        header += [
            f"u_{label}",
            f"absu_over_loglog_{label}",
            f"logN_g_{label}",
            f"logN_gp_abs_{label}",
            f"N_coeff_abs_{label}",
        ]
    header += [
        "coeff_rel_spread_times_logN",
        "frozen_update_norm",
        "NlogN_frozen_update_norm",
        "exact_update_norm",
        "NlogN_exact_update_norm",
        "exact_over_frozen",
        "cancel_ratio",
        "logN_cancel_ratio",
        "walsh_bias_NlogN",
        "walsh_x1_NlogN",
        "walsh_x2_NlogN",
        "walsh_parity_N",
    ]
    print(",".join(header))

    checkpoint_index = 0
    for epoch in range(1, checkpoints[-1] + 1):
        train_epoch(net, data)
        if epoch != checkpoints[checkpoint_index]:
            continue

        coarse = trio_coarse(net)
        terms = frozen_hidden_gradient_terms(coarse, 0, data)
        frozen = vec_sum([t["vec"] for t in terms])
        exact = exact_hidden_epoch_update(coarse, 0, data)

        logn = math.log(epoch)
        loglogn = math.log(logn)
        coeff_abs = [abs(t["coeff"]) for t in terms]
        coeff_mean = sum(coeff_abs) / len(coeff_abs)
        rel_spread = (max(coeff_abs) - min(coeff_abs)) / coeff_mean

        l1 = sum(vec_norm(t["vec"]) for t in terms)
        cancel_ratio = vec_norm(frozen) / l1

        walsh = coeff_walsh(terms)

        row = [
            epoch,
            loglogn,
            coarse.hidden_w[0][0] / loglogn,
            coarse.hidden_w[0][1] / loglogn,
            coarse.hidden_w[0][2] / loglogn,
        ]
        for t in terms:
            row += [
                t["u"],
                abs(t["u"]) / loglogn,
                logn * t["g"],
                logn * abs(t["gp"]),
                epoch * abs(t["coeff"]),
            ]
        row += [
            rel_spread * logn,
            vec_norm(frozen),
            epoch * logn * vec_norm(frozen),
            vec_norm(exact),
            epoch * logn * vec_norm(exact),
            vec_norm(exact) / vec_norm(frozen),
            cancel_ratio,
            logn * cancel_ratio,
            epoch * logn * walsh["bias"],
            epoch * logn * walsh["x1"],
            epoch * logn * walsh["x2"],
            epoch * walsh["parity"],
        ]
        print(",".join(f"{float(v):.15g}" if not isinstance(v, int) else str(v) for v in row))

        checkpoint_index += 1
        if checkpoint_index == len(checkpoints):
            break
