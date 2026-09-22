import math

from threeplusone import (
    ThreePlusOneMLP,
    add_transverse_seed,
    centered_singleton_seed,
    scan_transverse_growth,
    transverse_residual_norm,
    xnor,
)


def centered_net() -> ThreePlusOneMLP:
    return ThreePlusOneMLP(
        epsilon=1.0,
        seed_pattern=centered_singleton_seed(4),
    )


def print_instability_intervals(records) -> None:
    start = records[0].epoch
    current = records[0].unstable_dimension

    for record in records[1:]:
        if record.unstable_dimension != current:
            print(
                f"epochs {start}-{record.epoch - 1}: "
                f"{current} expanding channel directions"
            )
            start = record.epoch
            current = record.unstable_dimension

    print(
        f"epochs {start}-{records[-1].epoch}: "
        f"{current} expanding channel directions"
    )


if __name__ == "__main__":
    records = scan_transverse_growth(
        centered_net(),
        xnor(),
        epochs=728,
    )

    print_instability_intervals(records)

    peak = max(
        records,
        key=lambda record: record.cumulative_top_gain,
    )
    final = records[-1]

    print(
        "peak cumulative top gain:",
        f"{peak.cumulative_top_gain:.6f}",
        "at epoch",
        peak.epoch,
    )
    print(
        "epoch 728 cumulative singular values:",
        tuple(round(value, 6) for value in final.cumulative_singular_values),
    )

    net = centered_net()
    add_transverse_seed(
        net,
        amplitude=1e-6,
        phase=0.0,
        channel=0,
    )
    initial = transverse_residual_norm(net)

    for _ in range(728):
        for x, target in xnor():
            net.train_one(x, target)

    final_residual = transverse_residual_norm(net)

    print(
        "tiny-history amplification:",
        f"{final_residual / initial:.6f}x",
    )
