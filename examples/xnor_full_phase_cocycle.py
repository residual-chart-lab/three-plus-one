"""Scan the actual four-channel phase cocycle after branch formation.

This diagnostic keeps the full antisymmetric equal-pair tangent vector rather
than projecting it back to the instantaneous phase line after every epoch.

For a starting epoch n,

    Gamma_{N,n} = ell_N J_{N-1} ... J_n v_n

is compared with the product of local phase derivatives

    Prod rho_j.

Their difference is exactly the accumulated effect of hidden tangent
components that were discarded by the scalar projection.
"""
import math
from copy import deepcopy

from threeplusone import (
    ThreePlusOneMLP,
    add_transverse_vector_seed,
    centered_singleton_seed,
    transverse_residual,
    xnor,
)
from threeplusone.transverse import epoch_transverse_matrix


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
    r = [float(z.real) for z in residual]
    n2 = dot(r, r)
    if n2 == 0.0:
        raise RuntimeError("branch residual vanished")
    ell = [x / n2 for x in r]
    return r, ell, math.sqrt(n2)


def train_epoch(net, data):
    for x, target in data:
        net.train_one(x, target)


def snapshot_checkpoints(checkpoints):
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
    data = xnor()
    result = {}
    wanted = set(checkpoints)
    for epoch in range(1, max(checkpoints) + 1):
        train_epoch(net, data)
        if epoch in wanted:
            result[epoch] = deepcopy(net)
    return result


def scan_from(start_epoch, net, horizons):
    data = xnor()
    work = deepcopy(net)
    r0, _, _ = phase_data(work)

    tangent = r0[:]
    local_product = 1.0
    output = []
    requested = sorted(set(int(h) for h in horizons))
    target_index = 0
    max_horizon = requested[-1]

    for step in range(1, max_horizon + 1):
        r_before, _, _ = phase_data(work)
        matrix = epoch_transverse_matrix(
            work,
            data,
            representative_unit=1,
        )
        tangent = matvec(matrix, tangent)
        local_phase_image = matvec(matrix, r_before)

        train_epoch(work, data)
        r_after, ell_after, radius = phase_data(work)

        rho = dot(ell_after, local_phase_image)
        local_product *= rho
        gamma = dot(ell_after, tangent)

        phase_part = [gamma * x for x in r_after]
        hidden = [
            tangent[i] - phase_part[i]
            for i in range(4)
        ]
        hidden_norm = math.sqrt(dot(hidden, hidden))
        tangent_norm = math.sqrt(dot(tangent, tangent))
        relative_gap = (
            (gamma - local_product) / gamma
            if gamma != 0.0
            else math.nan
        )

        if step == requested[target_index]:
            end_epoch = start_epoch + step
            output.append({
                "start_epoch": start_epoch,
                "horizon": step,
                "end_epoch": end_epoch,
                "gamma": gamma,
                "local_product": local_product,
                "difference": gamma - local_product,
                "relative_gap": relative_gap,
                "minus_log_abs_gamma": -math.log(abs(gamma)),
                "minus_log_abs_local_product": -math.log(abs(local_product)),
                "hidden_norm": hidden_norm,
                "tangent_norm": tangent_norm,
                "hidden_fraction": hidden_norm / tangent_norm,
                "branch_radius": radius,
            })
            target_index += 1
            if target_index == len(requested):
                break

    return output


if __name__ == "__main__":
    starts = (728, 10_000, 100_000)
    horizons = (
        1, 2, 3, 10, 100, 1_000, 10_000, 100_000, 1_000_000,
    )
    snapshots = snapshot_checkpoints(starts)

    print(
        "start,horizon,end,gamma,local_product,difference,relative_gap,"
        "minus_log_gamma,minus_log_local,hidden_fraction,branch_radius"
    )
    for start in starts:
        rows = scan_from(start, snapshots[start], horizons)
        for row in rows:
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
