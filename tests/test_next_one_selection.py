import math
import unittest

from threeplusone.selection import (
    NextOneParams,
    NextOneState,
    branch_lock_error,
    branch_rhs,
    c3_rotate,
    rotor_energy,
    selected_branch,
    simulate_next_one,
)


class NextOneSelectionTests(unittest.TestCase):
    def test_c3_branch_field_is_equivariant(self):
        z = complex(0.37, -0.22)
        mu = 0.41
        nu = 0.33
        beta = 0.87

        rhs = branch_rhs(
            z,
            mu=mu,
            anisotropy=nu,
            saturation=beta,
        )

        for turns in (1, 2):
            rotated = c3_rotate(z, turns)
            rotated_rhs = branch_rhs(
                rotated,
                mu=mu,
                anisotropy=nu,
                saturation=beta,
            )
            expected = c3_rotate(rhs, turns)
            self.assertAlmostEqual(rotated_rhs.real, expected.real, places=13)
            self.assertAlmostEqual(rotated_rhs.imag, expected.imag, places=13)

    def test_exact_symmetric_branch_state_cannot_self_select(self):
        params = NextOneParams()
        initial = NextOneState(
            phi=0.0,
            ell=1.8,
            z_re=0.0,
            z_im=0.0,
        )

        states = simulate_next_one(
            initial,
            params,
            dt=0.01,
            steps=6000,
            record_every=500,
        )

        for state in states:
            self.assertEqual(state.z_re, 0.0)
            self.assertEqual(state.z_im, 0.0)
            self.assertIsNone(selected_branch(state))

    def test_damping_drives_rotor_energy_down_through_barrier(self):
        params = NextOneParams()
        initial = NextOneState(
            phi=0.0,
            ell=1.8,
            z_re=1e-4,
            z_im=0.0,
        )

        states = simulate_next_one(
            initial,
            params,
            dt=0.01,
            steps=6000,
            record_every=10,
        )
        energies = [rotor_energy(state, params) for state in states]

        self.assertGreater(energies[0], params.barrier_energy)
        self.assertLess(energies[-1], params.barrier_energy)

        # RK4 is not an exact discrete gradient method, but at this step size
        # the analytic monotone dissipation law is respected numerically.
        for before, after in zip(energies, energies[1:]):
            self.assertLessEqual(after, before + 1e-8)

    def test_same_coarse_rotor_with_three_hidden_histories_selects_three_branches(self):
        params = NextOneParams()

        seed_angles = (
            -2.0 * math.pi / 3.0,
            0.0,
            2.0 * math.pi / 3.0,
        )
        selected = []

        for angle in seed_angles:
            initial = NextOneState(
                phi=0.0,
                ell=1.8,
                z_re=1e-4 * math.cos(angle),
                z_im=1e-4 * math.sin(angle),
            )
            states = simulate_next_one(
                initial,
                params,
                dt=0.01,
                steps=5000,
                record_every=500,
            )
            final = states[-1]
            selected.append(selected_branch(final))

            self.assertGreater(abs(final.z), 1.0)
            error = branch_lock_error(final)
            self.assertIsNotNone(error)
            self.assertLess(error, 0.05)

        self.assertEqual(selected, [0, 1, 2])

    def test_c3_rotated_history_rotates_selected_branch(self):
        params = NextOneParams()
        base = complex(1e-4, 0.0)

        selected = []
        for turns in (0, 1, 2):
            z = c3_rotate(base, turns)
            initial = NextOneState(
                phi=0.0,
                ell=1.8,
                z_re=z.real,
                z_im=z.imag,
            )
            final = simulate_next_one(
                initial,
                params,
                dt=0.01,
                steps=5000,
                record_every=500,
            )[-1]
            selected.append(selected_branch(final))

        # The absolute offset comes from the transported rotor history.
        # C3 rotation of the hidden residual must still cycle the outcome.
        self.assertEqual(
            [(selected[(i + 1) % 3] - selected[i]) % 3 for i in range(3)],
            [1, 1, 1],
        )


if __name__ == "__main__":
    unittest.main()
