"""Scan the actual four-channel phase cocycle after branch formation.

This diagnostic keeps the full antisymmetric equal-pair tangent vector rather
than projecting it back to the instantaneous phase line after every epoch.

For a starting epoch n,

    Gamma_{N,n} = ell_N J_{N-1} ... J_n v_n

is compared with the product of local phase derivatives

    Prod rho_j.

All requested starting epochs are propagated through one shared SGD trajectory,
so the long scan computes each epoch Jacobian only once.
"""
import math

from threeplusone import (
    ThreePlusOneMLP,
    add_transverse_vector_seed,
    centered_singleton_seed,
    transverse_residual,
    xnor,
)
from threeplusone.transverse import sample_transverse_matrix


def matvec(matrix, vector):
    return [
        sum(matrix[i][j] * vector[j] for j in range(4))
        for i in range(4)
    ]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def phase_data(net):
    residual = transverse_residual(net)
    if max(abs(z.imag) for z in residual) > 1e-10:
        raise RuntimeError("expected phase-zero real branch residual")
    radial = [float(z.real) for z in residual]
    norm2 = dot(radial, radial)
    if norm2 == 0.0:
        raise RuntimeError("branch residual vanished")
    ell = [x / norm2 for x in radial]
    return radial, ell, math.sqrt(norm2)


def train_epoch(net, data):
    for x, target in data:
        net.train_one(x, target)


def matmul(a, b):
    return [
        [
            sum(a[i][k] * b[k][j] for k in range(4))
            for j in range(4)
        ]
        for i in range(4)
    ]


def advance_epoch_with_tangent(net, data):
    """Advance the actual network one epoch and return that epoch's tangent."""
    matrix = [
        [1.0 if i == j else 0.0 for j in range(4)]
        for i in range(4)
    ]
    for x, target in data:
        step = sample_transverse_matrix(
            net,
            x,
            target,
            representative_unit=1,
        )
        matrix = matmul(step, matrix)
        net.train_one(x, target)
    return matrix


def make_net():
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


def scan(starts, horizons):
    starts = tuple(sorted(set(int(x) for x in starts)))
    horizons = tuple(sorted(set(int(x) for x in horizons)))
    requested = set(horizons)
    data = xnor()
    net = make_net()

    first_start = starts[0]
    max_end = max(start + horizons[-1] for start in starts)

    for _ in range(first_start):
        train_epoch(net, data)

    active = {}
    rows = []

    for epoch in range(first_start, max_end):
        if epoch in starts:
            radial, _, _ = phase_data(net)
            active[epoch] = {
                "tangent": radial[:],
                "local_product": 1.0,
            }

        radial_before, _, _ = phase_data(net)
        # Propagate copies only after the exact epoch tangent has been built.
        # advance_epoch_with_tangent mutates net to the next SGD epoch.
        tangent_inputs = {
            start: state["tangent"][:]
            for start, state in active.items()
        }
        matrix = advance_epoch_with_tangent(net, data)
        local_phase_image = matvec(matrix, radial_before)

        for start, state in active.items():
            state["tangent"] = matvec(matrix, tangent_inputs[start])

        radial_after, ell_after, radius = phase_data(net)
        rho = dot(ell_after, local_phase_image)

        finished = []
        for start, state in active.items():
            state["local_product"] *= rho
            horizon = epoch + 1 - start
            if horizon not in requested:
                continue

            tangent = state["tangent"]
            gamma = dot(ell_after, tangent)
            local_product = state["local_product"]
            phase_part = [gamma * x for x in radial_after]
            hidden = [
                tangent[i] - phase_part[i]
                for i in range(4)
            ]
            hidden_norm = math.sqrt(dot(hidden, hidden))
            tangent_norm = math.sqrt(dot(tangent, tangent))

            rows.append({
                "start_epoch": start,
                "horizon": horizon,
                "end_epoch": epoch + 1,
                "gamma": gamma,
                "local_product": local_product,
                "difference": gamma - local_product,
                "relative_gap": (
                    (gamma - local_product) / gamma
                    if gamma != 0.0
                    else math.nan
                ),
                "minus_log_abs_gamma": -math.log(abs(gamma)),
                "minus_log_abs_local_product": -math.log(abs(local_product)),
                "hidden_norm": hidden_norm,
                "tangent_norm": tangent_norm,
                "hidden_fraction": hidden_norm / tangent_norm,
                "branch_radius": radius,
            })

            if horizon == horizons[-1]:
                finished.append(start)

        for start in finished:
            del active[start]

    return rows


if __name__ == "__main__":
    starts = (728, 10_000, 100_000)
    horizons = (
        1, 2, 3, 10, 100, 1_000, 10_000, 100_000, 1_000_000,
    )

    print(
        "start,horizon,end,gamma,local_product,difference,relative_gap,"
        "minus_log_gamma,minus_log_local,hidden_fraction,branch_radius"
    )
    for row in scan(starts, horizons):
        print(
            f"{row['start_epoch']},"
            f"{row['horizon']},"
            f"{row['end_epoch']},"
            f"{row['gamma']:.17g},"
            f"{row['local_product']:.17g},"
            f"{row['difference']:.17g},"
            f"{row['relative_gap']:.17g},"
            f"{row['minus_log_abs_gamma']:.17g},"
            f"{row['minus_log_abs_local_product']:.17g},"
            f"{row['hidden_fraction']:.17g},"
            f"{row['branch_radius']:.17g}"
        )
