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


def linear_fit(xs, ys):
    n = len(xs)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    sxx = sum((x - mean_x) ** 2 for x in xs)
    sxy = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    slope = sxy / sxx
    intercept = mean_y - slope * mean_x
    residuals = [y - (intercept + slope * x) for x, y in zip(xs, ys)]
    rmse = math.sqrt(sum(r * r for r in residuals) / n)
    return intercept, slope, rmse


if __name__ == "__main__":
    checkpoints = (
        10_000,
        20_000,
        50_000,
        100_000,
        200_000,
        500_000,
        1_000_000,
    )

    records = scan_selector_persistence(
        centered_net(),
        xnor(),
        checkpoints=checkpoints,
        amplitude=0.1,
        phase_delta=1e-4,
        probe_phase=math.pi / 6.0,
    )

    print(
        "epoch,mse,rho,selector_action,probe_phase,"
        "probe_lock_error,projected_amplitude"
    )
    for row in records:
        print(
            f"{row.epoch},"
            f"{row.mse:.15g},"
            f"{row.phase_contraction:.15g},"
            f"{row.cumulative_selector_action:.15g},"
            f"{row.probe_output_phase:.15g},"
            f"{row.probe_lock_error:.15g},"
            f"{row.projected_residual_amplitude:.15g}"
        )

    print("\nlocal effective slope c_eff = dA / d(log log N)")
    for left, right in zip(records, records[1:]):
        dx = math.log(math.log(right.epoch)) - math.log(math.log(left.epoch))
        c_eff = (
            right.cumulative_selector_action
            - left.cumulative_selector_action
        ) / dx
        print(f"{left.epoch}->{right.epoch}: {c_eff:.12g}")

    late = records[1:]
    ys = [row.cumulative_selector_action for row in late]
    candidates = {
        "log_N": [math.log(row.epoch) for row in late],
        "log_log_N": [math.log(math.log(row.epoch)) for row in late],
        "inv_log_N": [1.0 / math.log(row.epoch) for row in late],
    }

    print("\nsimple late-window linear fits")
    for name, xs in candidates.items():
        intercept, slope, rmse = linear_fit(xs, ys)
        print(
            f"{name}: intercept={intercept:.12g}, "
            f"slope={slope:.12g}, rmse={rmse:.12g}"
        )

    # If A_N ~ c log log N + b, then rho_N ~ C (log N)^(-3c).
    _, c, _ = linear_fit(candidates["log_log_N"], ys)
    print(f"\nimplied rho exponent p=3c: {3.0 * c:.12g}")
