from .core import ThreePlusOneMLP, FitResult, EpochRecord, centered_singleton_seed
from .datasets import xnor
from .experiments import epsilon_sweep
from .geometry import (
    TETRAHEDRAL_BRANCH_ANGLE,
    centered_contrast_vertices,
    child_axes,
    dual_tetrahedra,
    oriented_area,
    tetrahedral_relative_order,
    tetrahedron_vertices,
)
from .dynamics import (
    DualRotorParams,
    DualRotorState,
    relative_energy,
    relative_regime,
    relative_winding,
    simulate_dual_rotor,
    total_momentum,
)

__all__ = [
    "ThreePlusOneMLP",
    "FitResult",
    "EpochRecord",
    "centered_singleton_seed",
    "xnor",
    "epsilon_sweep",
    "TETRAHEDRAL_BRANCH_ANGLE",
    "centered_contrast_vertices",
    "child_axes",
    "dual_tetrahedra",
    "oriented_area",
    "tetrahedral_relative_order",
    "tetrahedron_vertices",
    "DualRotorParams",
    "DualRotorState",
    "relative_energy",
    "relative_regime",
    "relative_winding",
    "simulate_dual_rotor",
    "total_momentum",
]
__version__ = "0.2.0"
