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


@dataclass(frozen=True)
class Bimodal(Distribution):
    peak: Normal = Normal()

    def offsets(self, count: int, rng: np.random.Generator) -> np.ndarray:
        sides = rng.choice((-0.5, 0.5), count)
        return sides + self.peak.offsets(count, rng) / 2


@dataclass(frozen=True)
class Arcsine(Distribution):
    edge: float = 0.5

    def __post_init__(self):
        if self.edge <= 0:
            raise ValueError(f"edge must be positive, got {self.edge}")

    def offsets(self, count: int, rng: np.random.Generator) -> np.ndarray:
        return rng.beta(self.edge, self.edge, count) * 2 - 1
