import unittest

from threeplusone import (
    ThreePlusOneMLP,
    centered_singleton_seed,
    epsilon_sweep,
    xnor,
)


class ThreePlusOneTests(unittest.TestCase):
    def test_zero_epsilon_preserves_exact_hidden_symmetry(self):
        net = ThreePlusOneMLP(epsilon=0.0, max_epochs=640)
        result = net.fit(xnor())

        self.assertFalse(result.converged)
        self.assertEqual(net.hidden_groups(), [[1, 2, 3, 4]])
        self.assertEqual(net.hidden_spread(), 0.0)

    def test_three_plus_one_breaks_symmetry_and_converges(self):
        net = ThreePlusOneMLP(epsilon=1.0)
        result = net.fit(xnor())

        self.assertTrue(result.converged)
        self.assertEqual(result.epochs, 715)
        self.assertAlmostEqual(result.mse, 0.009981583676939314, places=14)
        self.assertEqual(net.hidden_groups(), [[1, 2, 3], [4]])
        self.assertGreater(net.hidden_spread(), 0.0)

    def test_centered_seed_preserves_initial_function_and_still_learns(self):
        seed = centered_singleton_seed(4)
        self.assertEqual(seed, (-0.25, -0.25, -0.25, 0.75))
        self.assertEqual(sum(seed), 0.0)

        control = ThreePlusOneMLP(epsilon=0.0)
        centered = ThreePlusOneMLP(epsilon=1.0, seed_pattern=seed)

        for x, _ in xnor():
            self.assertAlmostEqual(
                control.predict(x),
                centered.predict(x),
                places=15,
            )

        result = centered.fit(xnor())
        self.assertTrue(result.converged)
        self.assertLessEqual(result.mse, centered.target_mse)
        self.assertEqual(centered.hidden_groups(), [[1, 2, 3], [4]])
        self.assertGreater(centered.hidden_spread(), 0.0)

    def test_seed_pattern_is_explicit(self):
        net = ThreePlusOneMLP(
            hidden=4,
            epsilon=0.5,
            seed_pattern=[0, 0, 1, 1],
        )
        self.assertEqual(
            net.output_weights(),
            (-1.0, -1.0, -1.0, -0.5, -0.5),
        )

    def test_sweep_returns_controls(self):
        rows = epsilon_sweep(
            xnor(),
            [0.0, 1.0],
            max_epochs=1000,
        )
        self.assertEqual(len(rows), 2)
        self.assertFalse(rows[0].converged)
        self.assertTrue(rows[1].converged)


if __name__ == "__main__":
    unittest.main()
