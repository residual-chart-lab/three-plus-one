"""Measure coupling between the instantaneous phase line and hidden tangent space.

The four-channel tangent is decomposed at each epoch into the normalized branch
axis e_n and its Euclidean orthogonal complement.  For the one-epoch tangent J_n,

    alpha_n = <e_{n+1}, J_n e_n>

is the normalized phase-line gain,

    c_n = P_{n+1} J_n e_n

is phase -> hidden leakage, and

    b_n = P_n J_n^T e_{n+1}

is the hidden -> phase coupling row represented as a vector.

The two-step return from the leaked component is also measured in the original
phase-readout normalization.  This is the memory correction omitted by a
product of local scalar phase derivatives.
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


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def matvec(matrix, vector):
    return [
        sum(matrix[i][j] * vector[j] for j in range(4))
        for i in range(4)
    ]


def transpose_matvec(matrix, vector):
    return [
        sum(matrix[i][j] * vector[i] for i in range(4))
        for j in range(4)
    ]


def norm(vector):
    return math.sqrt(dot(vector, vector))


def phase_axis(net):
    residual = transverse_residual(net)
    if max(abs(z.imag) for z in residual) > 1e-10:
        raise RuntimeError("expected phase-zero branch")
    radial = [float(z.real) for z in residual]
    radius = norm(radial)
    return radial, [x / radius for x in radial], radius


def train_epoch(net, data):
    for x, target in data:
        net.train_one(x, target)


def checkpoint_metrics(net):
    data = xnor()
    radial0, e0, r0 = phase_axis(net)
    J0 = epoch_transverse_matrix(net, data, representative_unit=1)

    one = deepcopy(net)
    train_epoch(one, data)
    radial1, e1, r1 = phase_axis(one)

    Je = matvec(J0, e0)
    alpha = dot(e1, Je)
    leakage = [Je[i] - alpha * e1[i] for i in range(4)]
    leak_norm = norm(leakage)

    Jte = transpose_matvec(J0, e1)
    back = [Jte[i] - alpha * e0[i] for i in range(4)]
    back_norm = norm(back)

    rho0 = (r0 / r1) * alpha

    J1 = epoch_transverse_matrix(one, data, representative_unit=1)
    two = deepcopy(one)
    train_epoch(two, data)
    _, e2, r2 = phase_axis(two)

    return_normalized = dot(e2, matvec(J1, leakage))
    return_phase = (r0 / r2) * return_normalized

    radial1_image = matvec(J1, radial1)
    rho1 = dot(e2, radial1_image) / r2
    full_two = dot(
        e2,
        matvec(J1, matvec(J0, radial0)),
    ) / r2

    return {
        "rho": rho0,
        "one_minus_rho": 1.0 - rho0,
        "alpha": alpha,
        "phase_to_hidden": leak_norm,
        "hidden_to_phase": back_norm,
        "coupling_product": leak_norm * back_norm,
        "two_step_return": return_phase,
        "two_step_full": full_two,
        "two_step_local_product": rho0 * rho1,
        "radius": r0,
    }


if __name__ == "__main__":
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
    checkpoints = (728, 10_000, 100_000, 1_000_000)

    print(
        "epoch,rho,one_minus_rho,alpha,phase_to_hidden,hidden_to_phase,"
        "coupling_product,two_step_return,return_over_local_defect,radius"
    )
    for epoch in range(1, checkpoints[-1] + 1):
        train_epoch(net, data)
        if epoch not in checkpoints:
            continue
        row = checkpoint_metrics(net)
        ratio = (
            row["two_step_return"] / row["one_minus_rho"]
            if row["one_minus_rho"] != 0.0
            else math.nan
        )
        print(
            f"{epoch},"
            f"{row['rho']:.17g},"
            f"{row['one_minus_rho']:.17g},"
            f"{row['alpha']:.17g},"
            f"{row['phase_to_hidden']:.17g},"
            f"{row['hidden_to_phase']:.17g},"
            f"{row['coupling_product']:.17g},"
            f"{row['two_step_return']:.17g},"
            f"{ratio:.17g},"
            f"{row['radius']:.17g}"
        )

        if epoch == 728:
            assert abs(
                row["two_step_return"] - 2.869405956915665e-6
            ) < 5e-12
            assert abs(
                row["two_step_full"] - row["two_step_local_product"]
                - row["two_step_return"]
            ) < 5e-12
