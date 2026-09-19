from .core import ThreePlusOneMLP, FitResult, EpochRecord, centered_singleton_seed
from .datasets import xnor
from .experiments import epsilon_sweep

__all__ = [
    "ThreePlusOneMLP",
    "FitResult",
    "EpochRecord",
    "centered_singleton_seed",
    "xnor",
    "epsilon_sweep",
]
__version__ = "0.1.2"
