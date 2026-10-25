import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Final, Sequence

import numpy as np
from manim import TAU, ManimColor

from light.coloring import Coloring, StaticColor

INSTANT: Final[float] = math.inf
_TIME_EPS: Final[float] = 1e-9


class Cannon(ABC):
    @abstractmethod
    def amount_for(self, duration: float) -> int: ...

    @abstractmethod
    def positions(self, count: int) -> np.ndarray: ...

    @abstractmethod
    def velocities(self, count: int) -> np.ndarray: ...

    @abstractmethod
    def colors(self, count: int) -> list[ManimColor]: ...

    @abstractmethod
    def fired(self, elapsed: float) -> int: ...


@dataclass(frozen=True)
class RadialCannon(Cannon):
    origin: Sequence[float] = (0.0, 0.0)
    amount: int = 5760
    velocity: float = 1.3
    coloring: Coloring = StaticColor()
    spawn_rate: float = INSTANT

    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError(f"amount must be positive, got {self.amount}")
        if self.spawn_rate <= 0:
            raise ValueError(
                f"spawn_rate must be positive, got {self.spawn_rate}"
            )

    def amount_for(self, duration: float) -> int:
        return self.amount

    def positions(self, count: int) -> np.ndarray:
        origin = np.asarray(self.origin, dtype=float)[:2]
        return np.tile(origin, (count, 1))

    def velocities(self, count: int) -> np.ndarray:
        angles = np.linspace(0, TAU, count, endpoint=False)
        directions = np.stack([np.cos(angles), np.sin(angles)], axis=1)
        return self.velocity * directions

    def colors(self, count: int) -> list[ManimColor]:
        return self.coloring.colors(count)

    def fired(self, elapsed: float) -> int:
        if math.isinf(self.spawn_rate):
            return self.amount
        fired = int(elapsed * self.spawn_rate + _TIME_EPS)
        return min(self.amount, fired)


@dataclass(frozen=True)
class StreamCannon(Cannon):
    origin: Sequence[float] = (0.0, 0.0)
    direction: float = 0.0
    velocity: float = 1.3
    coloring: Coloring = StaticColor()
    spawn_rate: float = 60.0

    def __post_init__(self):
        if not 0 < self.spawn_rate < math.inf:
            raise ValueError(
                f"spawn_rate must be positive and finite, "
                f"got {self.spawn_rate}"
            )

    def amount_for(self, duration: float) -> int:
        return int(duration * self.spawn_rate) + 1

    def positions(self, count: int) -> np.ndarray:
        origin = np.asarray(self.origin, dtype=float)[:2]
        return np.tile(origin, (count, 1))

    def velocities(self, count: int) -> np.ndarray:
        heading = np.array([np.cos(self.direction), np.sin(self.direction)])
        return np.tile(self.velocity * heading, (count, 1))

    def colors(self, count: int) -> list[ManimColor]:
        return self.coloring.colors(count)

    def fired(self, elapsed: float) -> int:
        return int(elapsed * self.spawn_rate + _TIME_EPS)
