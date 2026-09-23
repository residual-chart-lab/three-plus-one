import math
from copy import deepcopy

from threeplusone import (
    ThreePlusOneMLP,
    add_transverse_vector_seed,
    centered_singleton_seed,
    epoch_transverse_matrix,
    projected_training_harmonic,
    transverse_residual,
    xnor,
)

from xnor_sgd_tail_scaling import (
    centered_net,
    local_state,
    one_epoch_phase_contraction,
    set_local_state,
    train_epoch,
)


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


if __name__ == "__main__":
    data = xnor()
    ray = centered_net()
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
        "N,r,lambda,nu,nu_over_lambda,"
        "q_eps005,q_eps01,q_eps02,q_rel_spread,"
        "predicted_action,measured_action,pred_over_measured,"
        "NlogN_nu_over_lambda,NlogN_predicted_action"
    )

    checkpoint_index = 0
    for epoch in range(1, checkpoints[-1] + 1):
        train_epoch(ray, data)
        if epoch != checkpoints[checkpoint_index]:
            continue

        z = transverse_residual(ray)
        # Reflection symmetry keeps the phase-0 ray real.
        radial = [value.real for value in z]
        r = math.sqrt(sum(value * value for value in radial))
        direction = tuple(value / r for value in radial)

        coarse = symmetrize_trio(ray)
        linear_map = epoch_transverse_matrix(coarse, data)
        response = matvec(linear_map, direction)
        gain = math.sqrt(sum(value * value for value in response))
        output_direction = tuple(value / gain for value in response)

        ratios = []
        linears = []
        quadratics = []
        for eps in (5e-3, 1e-2, 2e-2):
            linear_eps = projected_training_harmonic(
                coarse,
                data,
                epochs=1,
                input_direction=direction,
                output_direction=output_direction,
                amplitude=eps,
                harmonic=1,
                phase_samples=12,
            ) / eps
            quadratic_eps = projected_training_harmonic(
                coarse,
                data,
                epochs=1,
                input_direction=direction,
                output_direction=output_direction,
                amplitude=eps,
                harmonic=-2,
                phase_samples=12,
            ) / (eps * eps)
            linears.append(linear_eps)
            quadratics.append(quadratic_eps)
            ratios.append(quadratic_eps.real / linear_eps.real)

        linear = linears[1]
        quadratic = quadratics[1]
        ratio = ratios[1]
        ratio_spread = (max(ratios) - min(ratios)) / abs(ratio)
        predicted_action = ratio * r
        _, measured_action = one_epoch_phase_contraction(ray, data)

        logn = math.log(epoch)
        print(
            f"{epoch},"
            f"{r:.15g},"
            f"{linear.real:.15g},"
            f"{quadratic.real:.15g},"
            f"{ratio:.15g},"
            f"{ratios[0]:.15g},"
            f"{ratios[1]:.15g},"
            f"{ratios[2]:.15g},"
            f"{ratio_spread:.15g},"
            f"{predicted_action:.15g},"
            f"{measured_action:.15g},"
            f"{predicted_action / measured_action:.15g},"
            f"{epoch * logn * ratio:.15g},"
            f"{epoch * logn * predicted_action:.15g}"
        )

        checkpoint_index += 1
        if checkpoint_index == len(checkpoints):
            break
