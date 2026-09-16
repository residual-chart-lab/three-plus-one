from .core import ThreePlusOneMLP, FitResult, EpochRecord
from .datasets import xnor
from .experiments import epsilon_sweep

__all__ = [
    "ThreePlusOneMLP",
    "FitResult",
    "EpochRecord",
    "xnor",
    "epsilon_sweep",
]
__version__ = "0.1.1"
