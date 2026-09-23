import math

from threeplusone import (
    ThreePlusOneMLP,
    add_transverse_vector_seed,
    centered_singleton_seed,
    xnor,
)


def centered_ray_net():
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


def sigmoid_preact(row, x):
    return row[0] + row[1] * x[0] + row[2] * x[1]


if __name__ == "__main__":
    data = xnor()
    net = centered_ray_net()
    checkpoints = (10_000, 100_000, 1_000_000)
    k = 0

    for epoch in range(1, checkpoints[-1] + 1):
        for x, t in data:
            net.train_one(x, t)

        if epoch != checkpoints[k]:
            continue

        print(f"=== epoch {epoch} ===")
        print("output_w", ",".join(f"{v:.15g}" for v in net.output_w))

        for si, (x, target) in enumerate(data):
            h, y = net._forward(x)
            err = target - y
            d = err * y * (1.0 - y)
            logit = math.log(y / (1.0 - y))
            margin = logit if target > 0.5 else -logit
            print(
                "sample",
                si,
                x,
                target,
                f"y={y:.15g}",
                f"err={err:.15g}",
                f"d={d:.15g}",
                f"margin={margin:.15g}",
            )
            print(
                "  h",
                ",".join(f"{v:.15g}" for v in h),
            )
            u = [sigmoid_preact(row, x) for row in net.hidden_w]
            g = [hv * (1.0 - hv) for hv in h]
            print("  u", ",".join(f"{v:.15g}" for v in u))
            print("  g", ",".join(f"{v:.15g}" for v in g))
            print(
                "  hidden_delta",
                ",".join(
                    f"{(g[i] * d * net.output_w[i+1]):.15g}"
                    for i in range(4)
                ),
            )

        for i, row in enumerate(net.hidden_w):
            print(
                f"hidden_w[{i}]",
                ",".join(f"{v:.15g}" for v in row),
            )

        k += 1
        if k == len(checkpoints):
            break
