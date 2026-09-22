import math
import unittest

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


class SelectorPersistenceTests(unittest.TestCase):
    def test_selector_action_continues_after_task_target_is_reached(self):
        records = scan_selector_persistence(
            centered_net(),
            xnor(),
            checkpoints=(728, 5000, 10000, 100000),
            amplitude=0.1,
            phase_delta=1e-4,
            probe_phase=math.pi / 6.0,
        )

        at_728, at_5000, at_10000, at_100000 = records

        # The ordinary task target is already reached at epoch 728.
        self.assertLessEqual(at_728.mse, 0.01001)
        self.assertLess(at_5000.mse, at_728.mse)
        self.assertLess(at_10000.mse, at_5000.mse)
        self.assertLess(at_100000.mse, at_10000.mse)

        # Nevertheless the branch-ray phase derivative keeps contracting.
        self.assertGreater(at_728.phase_contraction, at_5000.phase_contraction)
        self.assertGreater(at_5000.phase_contraction, at_10000.phase_contraction)
        self.assertGreater(at_10000.phase_contraction, at_100000.phase_contraction)

        # Therefore cumulative selector action is still increasing after the
        # task is already conventionally converged.
        self.assertLess(
            at_728.cumulative_selector_action,
            at_5000.cumulative_selector_action,
        )
        self.assertLess(
            at_5000.cumulative_selector_action,
            at_10000.cumulative_selector_action,
        )
        self.assertLess(
            at_10000.cumulative_selector_action,
            at_100000.cumulative_selector_action,
        )

        # A finite off-ray history keeps moving toward the singleton ray.
        initial_error = math.pi / 6.0
        self.assertLess(at_728.probe_lock_error, initial_error)
        self.assertLess(at_5000.probe_lock_error, at_728.probe_lock_error)
        self.assertLess(at_10000.probe_lock_error, at_5000.probe_lock_error)
        self.assertLess(at_100000.probe_lock_error, at_10000.probe_lock_error)

        # The retained residual has not been erased while this sorting occurs.
        self.assertGreater(
            at_5000.projected_residual_amplitude,
            at_728.projected_residual_amplitude,
        )
        self.assertGreater(
            at_10000.projected_residual_amplitude,
            at_5000.projected_residual_amplitude,
        )
        self.assertGreater(
            at_100000.projected_residual_amplitude,
            at_10000.projected_residual_amplitude,
        )

        # Deterministic reference values for the current implementation.
        self.assertAlmostEqual(
            at_728.cumulative_selector_action,
            0.0410643,
            places=5,
        )
        self.assertAlmostEqual(
            at_5000.cumulative_selector_action,
            0.0765029,
            places=5,
        )
        self.assertAlmostEqual(
            at_10000.cumulative_selector_action,
            0.0839642,
            places=5,
        )
        self.assertAlmostEqual(\n            at_100000.cumulative_selector_action,\n            0.1049100,\n            places=5,\n        )\n        self.assertAlmostEqual(at_728.probe_output_phase, 0.4829183, places=5)
        self.assertAlmostEqual(at_5000.probe_output_phase, 0.4498922, places=5)
        self.assertAlmostEqual(at_10000.probe_output_phase, 0.4431109, places=5)
        self.assertAlmostEqual(at_100000.probe_output_phase, 0.4245341, places=5)


if __name__ == "__main__":
    unittest.main()
