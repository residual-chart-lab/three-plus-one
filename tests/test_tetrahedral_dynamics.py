import math
import unittest

from threeplusone.dynamics import (
    DualRotorParams,
    DualRotorState,
    relative_energy,
    relative_phase,
    relative_regime,
    relative_winding,
    simulate_dual_rotor,
    total_momentum,
)
from threeplusone.geometry import (
    TETRAHEDRAL_BRANCH_ANGLE,
    centered_contrast_vertices,
    child_axes,
    dot,
    dual_tetrahedra,
    oriented_area,
    tetrahedral_relative_order,
    tetrahedron_vertices,
)


class TetrahedralGeometryTests(unittest.TestCase):
    def test_centered_contrast_vertices_form_regular_tetrahedron(self):
        vertices = centered_contrast_vertices()

        for i, vi in enumerate(vertices):
            self.assertAlmostEqual(sum(vi), 0.0, places=15)
            self.assertAlmostEqual(sum(x * x for x in vi), 1.0, places=15)

            for j, vj in enumerate(vertices):
                inner = sum(a * b for a, b in zip(vi, vj))
                expected = 1.0 if i == j else -1.0 / 3.0
                self.assertAlmostEqual(inner, expected, places=15)

    def test_axis_construction_is_regular_tetrahedron(self):
        vertices = tetrahedron_vertices((0.0, 0.0, 1.0), phase=0.37)

        for i, vi in enumerate(vertices):
            self.assertAlmostEqual(dot(vi, vi), 1.0, places=14)
            for j, vj in enumerate(vertices):
                expected = 1.0 if i == j else -1.0 / 3.0
                self.assertAlmostEqual(dot(vi, vj), expected, places=14)

    def test_dual_frames_are_central_inversions_when_phases_match(self):
        upper, lower = dual_tetrahedra(
            (0.2, -0.4, 1.0),
            theta_plus=0.71,
            theta_minus=0.71,
        )
        for u, l in zip(upper, lower):
            for a, b in zip(u, l):
                self.assertAlmostEqual(a, -b, places=14)

    def test_unlabeled_relative_order_has_c3_gauge_invariance(self):
        plus = 0.37
        minus = -0.21
        alignment, parity = tetrahedral_relative_order(plus, minus)

        for shift_plus, shift_minus in (
            (2.0 * math.pi / 3.0, 0.0),
            (0.0, 2.0 * math.pi / 3.0),
            (4.0 * math.pi / 3.0, -2.0 * math.pi / 3.0),
        ):
            a2, p2 = tetrahedral_relative_order(
                plus + shift_plus,
                minus + shift_minus,
            )
            self.assertAlmostEqual(a2, alignment, places=14)
            self.assertAlmostEqual(p2, parity, places=14)

        swapped_alignment, swapped_parity = tetrahedral_relative_order(
            minus,
            plus,
        )
        self.assertAlmostEqual(swapped_alignment, alignment, places=14)
        self.assertAlmostEqual(swapped_parity, -parity, places=14)

    def test_oriented_area_is_antisymmetric(self):
        axis = (0.0, 0.0, 1.0)
        u = (1.0, 0.0, 0.0)
        v = (0.0, 1.0, 0.0)

        self.assertAlmostEqual(oriented_area(axis, u, v), 1.0)
        self.assertAlmostEqual(oriented_area(axis, v, u), -1.0)

    def test_child_axes_have_tetrahedral_branch_angle(self):
        parent = (0.0, 0.0, 1.0)
        for child in child_axes(parent):
            angle = math.acos(max(-1.0, min(1.0, dot(parent, child))))
            self.assertAlmostEqual(angle, TETRAHEDRAL_BRANCH_ANGLE, places=14)


class DualRotorTests(unittest.TestCase):
    def test_relative_energy_separates_libration_and_rotation(self):
        params = DualRotorParams(kappa=1.0)

        low = DualRotorState(0.0, 0.0, 1.0, -1.0)
        high = DualRotorState(0.0, 0.0, 1.5, -1.5)

        self.assertEqual(relative_regime(low, params), "libration")
        self.assertEqual(relative_regime(high, params), "rotation")
        self.assertLess(relative_energy(low, params), 2.0)
        self.assertGreater(relative_energy(high, params), 2.0)

    def test_symplectic_integrator_preserves_momentum_and_energy(self):
        params = DualRotorParams(kappa=1.0)
        initial = DualRotorState(0.0, 0.0, 1.5, -1.5)
        energy0 = relative_energy(initial, params)
        momentum0 = total_momentum(initial)

        states = simulate_dual_rotor(
            initial,
            params,
            dt=0.002,
            steps=10000,
            record_every=50,
        )

        max_energy_error = max(
            abs(relative_energy(state, params) - energy0)
            for state in states
        )
        max_momentum_error = max(
            abs(total_momentum(state) - momentum0)
            for state in states
        )

        self.assertLess(max_energy_error, 5e-5)
        self.assertLess(max_momentum_error, 1e-12)
        self.assertGreater(abs(relative_winding(states)), 5.0)

    def test_libration_does_not_accumulate_winding(self):
        params = DualRotorParams(kappa=1.0)
        initial = DualRotorState(0.0, 0.0, 1.0, -1.0)

        states = simulate_dual_rotor(
            initial,
            params,
            dt=0.002,
            steps=10000,
            record_every=50,
        )

        max_abs_phase = max(abs(relative_phase(state)) for state in states)
        self.assertLess(max_abs_phase, 0.6)
        self.assertLess(abs(relative_winding(states)), 0.2)


if __name__ == "__main__":
    unittest.main()
