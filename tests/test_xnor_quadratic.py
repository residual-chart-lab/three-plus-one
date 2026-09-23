import math
import unittest

from threeplusone import ThreePlusOneMLP, centered_singleton_seed, xnor
from threeplusone.transverse import (
    cumulative_transverse_matrix,
    dominant_course_anisotropy,
    dominant_singular_pair,
    projected_course_phase,
    projected_training_harmonic,
    epoch_transverse_quadratic_direction,
)


def centered_net() -> ThreePlusOneMLP:
    return ThreePlusOneMLP(
        epsilon=1.0,
        seed_pattern=centered_singleton_seed(4),
    )


def angle_distance(a: float, b: float) -> float:
    return abs(math.atan2(math.sin(a - b), math.cos(a - b)))


class XNORQuadraticAnisotropyTests(unittest.TestCase):
    def test_exact_epoch_quadratic_direction_matches_fourier_extraction(self):
        net = centered_net()
        direction = (0.8, -0.3, 0.4, 0.2)
        norm = math.sqrt(sum(v * v for v in direction))
        direction = tuple(v / norm for v in direction)

        linear_response, quadratic_response = epoch_transverse_quadratic_direction(
            net,
            xnor(),
            direction,
        )
        linear_norm = math.sqrt(sum(v * v for v in linear_response))
        output_direction = tuple(v / linear_norm for v in linear_response)

        exact_linear = sum(
            output_direction[i] * linear_response[i]
            for i in range(4)
        )
        exact_quadratic = sum(
            output_direction[i] * quadratic_response[i]
            for i in range(4)
        )

        eps = 1e-4
        measured_linear = projected_training_harmonic(
            net,
            xnor(),
            epochs=1,
            input_direction=direction,
            output_direction=output_direction,
            amplitude=eps,
            harmonic=1,
            phase_samples=12,
        ) / eps
        measured_quadratic = projected_training_harmonic(
            net,
            xnor(),
            epochs=1,
            input_direction=direction,
            output_direction=output_direction,
            amplitude=eps,
            harmonic=-2,
            phase_samples=12,
        ) / (eps * eps)

        self.assertAlmostEqual(measured_linear.real, exact_linear, places=8)
        self.assertAlmostEqual(measured_linear.imag, 0.0, places=9)
        self.assertAlmostEqual(measured_quadratic.real, exact_quadratic, places=6)
        self.assertAlmostEqual(measured_quadratic.imag, 0.0, places=7)

    def test_dominant_course_extracts_clean_linear_and_quadratic_harmonics(self):
        result = dominant_course_anisotropy(
            centered_net(),
            xnor(),
            epochs=728,
            amplitude=1e-4,
            phase_samples=12,
        )

        self.assertAlmostEqual(result.linear_gain.real, 34.7030625, places=5)
        self.assertAlmostEqual(result.linear_gain.imag, 0.0, places=8)

        self.assertAlmostEqual(
            result.quadratic_coefficient.real,
            -87.21614,
            places=3,
        )
        self.assertAlmostEqual(
            result.quadratic_coefficient.imag,
            0.0,
            places=5,
        )

    def test_forbidden_low_order_harmonics_are_numerically_absent(self):
        net = centered_net()
        matrix = cumulative_transverse_matrix(net, xnor(), epochs=728)
        _, output_direction, input_direction = dominant_singular_pair(matrix)

        amplitude = 1e-4
        allowed_linear = projected_training_harmonic(
            net,
            xnor(),
            epochs=728,
            input_direction=input_direction,
            output_direction=output_direction,
            amplitude=amplitude,
            harmonic=1,
            phase_samples=12,
        )
        allowed_quadratic = projected_training_harmonic(
            net,
            xnor(),
            epochs=728,
            input_direction=input_direction,
            output_direction=output_direction,
            amplitude=amplitude,
            harmonic=-2,
            phase_samples=12,
        )

        forbidden = []
        for harmonic in (-1, 0, 2, 3):
            forbidden.append(
                projected_training_harmonic(
                    net,
                    xnor(),
                    epochs=728,
                    input_direction=input_direction,
                    output_direction=output_direction,
                    amplitude=amplitude,
                    harmonic=harmonic,
                    phase_samples=12,
                )
            )

        self.assertGreater(abs(allowed_linear), 1e-3)
        self.assertGreater(abs(allowed_quadratic), 1e-8)
        self.assertTrue(all(abs(value) < 1e-10 for value in forbidden))

    def test_actual_training_bends_finite_history_toward_singleton_rays(self):
        net = centered_net()
        matrix = cumulative_transverse_matrix(net, xnor(), epochs=728)
        _, output_direction, input_direction = dominant_singular_pair(matrix)

        amplitude = 0.2

        # Inside the basin around the phase-0 singleton ray.
        initial_a = math.pi / 6.0
        final_a = projected_course_phase(
            net,
            xnor(),
            epochs=728,
            input_direction=input_direction,
            output_direction=output_direction,
            amplitude=amplitude,
            phase=initial_a,
        )
        self.assertLess(
            angle_distance(final_a, 0.0),
            angle_distance(initial_a, 0.0),
        )

        # Inside the neighboring basin around the +2*pi/3 singleton ray.
        initial_b = math.pi / 2.0
        target_b = 2.0 * math.pi / 3.0
        final_b = projected_course_phase(
            net,
            xnor(),
            epochs=728,
            input_direction=input_direction,
            output_direction=output_direction,
            amplitude=amplitude,
            phase=initial_b,
        )
        self.assertLess(
            angle_distance(final_b, target_b),
            angle_distance(initial_b, target_b),
        )


    def test_original_output_weight_channel_has_positive_threefold_anisotropy(self):
        net = centered_net()
        matrix = cumulative_transverse_matrix(net, xnor(), epochs=728)

        input_direction = (1.0, 0.0, 0.0, 0.0)
        linear_response = [
            sum(matrix[i][j] * input_direction[j] for j in range(4))
            for i in range(4)
        ]
        linear_gain = math.sqrt(sum(value * value for value in linear_response))
        output_direction = tuple(value / linear_gain for value in linear_response)

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

        self.assertAlmostEqual(linear.real, 15.1556910, places=5)
        self.assertAlmostEqual(quadratic.real, 6.65860, places=4)
        self.assertAlmostEqual(linear.imag, 0.0, places=8)
        self.assertAlmostEqual(quadratic.imag, 0.0, places=5)

        probe_amplitude = 0.01
        theta = math.pi / 6.0
        predicted = (
            theta
            - (quadratic.real / linear.real)
            * probe_amplitude
            * math.sin(3.0 * theta)
        )
        measured = projected_course_phase(
            net,
            xnor(),
            epochs=728,
            input_direction=input_direction,
            output_direction=output_direction,
            amplitude=probe_amplitude,
            phase=theta,
        )

        self.assertAlmostEqual(measured, predicted, places=4)

    def test_full_nonlinear_course_respects_c3_rotation(self):
        net = centered_net()
        matrix = cumulative_transverse_matrix(net, xnor(), epochs=728)
        _, output_direction, input_direction = dominant_singular_pair(matrix)

        amplitude = 0.2
        phase = 0.37

        out0 = projected_course_phase(
            net,
            xnor(),
            epochs=728,
            input_direction=input_direction,
            output_direction=output_direction,
            amplitude=amplitude,
            phase=phase,
        )
        out1 = projected_course_phase(
            net,
            xnor(),
            epochs=728,
            input_direction=input_direction,
            output_direction=output_direction,
            amplitude=amplitude,
            phase=phase + 2.0 * math.pi / 3.0,
        )

        shifted = math.atan2(
            math.sin(out1 - out0),
            math.cos(out1 - out0),
        )
        self.assertAlmostEqual(shifted, 2.0 * math.pi / 3.0, places=9)


if __name__ == "__main__":
    unittest.main()
