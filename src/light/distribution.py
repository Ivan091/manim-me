from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np


class Distribution(ABC):
    @abstractmethod
    def offsets(self, count: int, rng: np.random.Generator) -> np.ndarray: ...


@dataclass(frozen=True)
class Uniform(Distribution):
    def offsets(self, count: int, rng: np.random.Generator) -> np.ndarray:
        return rng.uniform(-1.0, 1.0, count)


@dataclass(frozen=True)
class Normal(Distribution):
    sigmas: float = 3.0

    def __post_init__(self):
        if self.sigmas <= 0:
            raise ValueError(f"sigmas must be positive, got {self.sigmas}")

    def offsets(self, count: int, rng: np.random.Generator) -> np.ndarray:
        scale = 1.0 / self.sigmas
        offsets = rng.normal(0.0, scale, count)
        outside = np.abs(offsets) > 1.0
        while outside.any():
            offsets[outside] = rng.normal(0.0, scale, int(outside.sum()))
            outside = np.abs(offsets) > 1.0
        return offsets
