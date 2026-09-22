import math

from threeplusone import (
    ThreePlusOneMLP,
    centered_singleton_seed,
    cumulative_transverse_matrix,
    projected_course_phase,
    projected_training_harmonic,
    xnor,
)


def centered_net() -> ThreePlusOneMLP:
    return ThreePlusOneMLP(
        epsilon=1.0,
        seed_pattern=centered_singleton_seed(4),
    )


if __name__ == "__main__":
    net = centered_net()
    matrix = cumulative_transverse_matrix(net, xnor(), epochs=728)

    input_direction = (1.0, 0.0, 0.0, 0.0)
    response = [
        sum(matrix[i][j] * input_direction[j] for j in range(4))
        for i in range(4)
    ]
    gain = math.sqrt(sum(value * value for value in response))
    output_direction = tuple(value / gain for value in response)

    amplitude = 1e-4

    linear = projected_training_harmonic(
        net,
        xnor(),
        epochs=728,
        input_direction=input_direction,
        output_direction=output_direction,
        amplitude=amplitude,
        harmonic=1,
        phase_samples=12,
    ) / amplitude

    quadratic = projected_training_harmonic(
        net,
        xnor(),
        epochs=728,
        input_direction=input_direction,
        output_direction=output_direction,
        amplitude=amplitude,
        harmonic=-2,
        phase_samples=12,
    ) / (amplitude * amplitude)

    print("linear coefficient:", linear)
    print("quadratic C3 coefficient:", quadratic)

    probe_amplitude = 0.01
    probe_phase = math.pi / 6.0

    predicted = (
        probe_phase
        - (quadratic.real / linear.real)
        * probe_amplitude
        * math.sin(3.0 * probe_phase)
    )

    measured = projected_course_phase(
        net,
        xnor(),
        epochs=728,
        input_direction=input_direction,
        output_direction=output_direction,
        amplitude=probe_amplitude,
        phase=probe_phase,
    )

    print("phase input:", probe_phase)
    print("quadratic prediction:", predicted)
    print("full-network phase:", measured)
