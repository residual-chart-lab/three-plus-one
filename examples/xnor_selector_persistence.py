import math

from threeplusone import (
    ThreePlusOneMLP,
    centered_singleton_seed,
    scan_selector_persistence,
    xnor,
)


def centered_net() -> ThreePlusOneMLP:
    return ThreePlusOneMLP(
        epsilon=1.0,
        seed_pattern=centered_singleton_seed(4),
    )


if __name__ == "__main__":
    records = scan_selector_persistence(
        centered_net(),
        xnor(),
        checkpoints=(728, 1000, 2000, 5000, 10000, 20000, 50000, 100000),
        amplitude=0.1,
        phase_delta=1e-4,
        probe_phase=math.pi / 6.0,
    )

    print(
        "epoch,mse,linear_gain,phase_contraction,"
        "selector_action,probe_phase,probe_lock_error,projected_amplitude"
    )
    for row in records:
        print(
            f"{row.epoch},"
            f"{row.mse:.12g},"
            f"{row.linear_gain:.12g},"
            f"{row.phase_contraction:.12g},"
            f"{row.cumulative_selector_action:.12g},"
            f"{row.probe_output_phase:.12g},"
            f"{row.probe_lock_error:.12g},"
            f"{row.projected_residual_amplitude:.12g}"
        )
