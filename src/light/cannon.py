import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Final, Sequence

import numpy as np
from manim import TAU, ManimColor

from light.coloring import Coloring, StaticColor
from light.distribution import Distribution, Uniform
from light.sound import Silence, Sound

INSTANT: Final[float] = math.inf
_TIME_EPS: Final[float] = 1e-9


def _heading(direction: float) -> np.ndarray:
    return np.array([np.cos(direction), np.sin(direction)])


def _check_stream(spawn_rate: float, firing_time: float) -> None:
    if not 0 < spawn_rate < math.inf:
        raise ValueError(
            f"spawn_rate must be positive and finite, got {spawn_rate}"
        )
    if firing_time <= 0:
        raise ValueError(f"firing_time must be positive, got {firing_time}")


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

    @property
    @abstractmethod
    def sound(self) -> Sound: ...


@dataclass(frozen=True)
class RadialCannon(Cannon):
    origin: Sequence[float] = (0.0, 0.0)
    amount: int = 5760
    velocity: float = 1.3
    coloring: Coloring = StaticColor()
    spawn_rate: float = INSTANT
    sound: Sound = Silence()

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
    firing_time: float = math.inf
    sound: Sound = Silence()

    def __post_init__(self):
        _check_stream(self.spawn_rate, self.firing_time)

    def amount_for(self, duration: float) -> int:
        return int(min(duration, self.firing_time) * self.spawn_rate) + 1

    def positions(self, count: int) -> np.ndarray:
        origin = np.asarray(self.origin, dtype=float)[:2]
        return np.tile(origin, (count, 1))

    def velocities(self, count: int) -> np.ndarray:
        heading = _heading(self.direction)
        return np.tile(self.velocity * heading, (count, 1))

    def colors(self, count: int) -> list[ManimColor]:
        return self.coloring.colors(count)

    def fired(self, elapsed: float) -> int:
        return int(min(elapsed, self.firing_time) * self.spawn_rate + _TIME_EPS)


@dataclass(frozen=True)
class WideCannon(Cannon):
    origin: Sequence[float] = (0.0, 0.0)
    direction: float = 0.0
    width: float = 1.0
    velocity: float = 1.3
    coloring: Coloring = StaticColor()
    spawn_rate: float = 60.0
    distribution: Distribution = Uniform()
    seed: int = 0
    firing_time: float = math.inf
    sound: Sound = Silence()

    def __post_init__(self):
        if self.width <= 0:
            raise ValueError(f"width must be positive, got {self.width}")
        _check_stream(self.spawn_rate, self.firing_time)

    def amount_for(self, duration: float) -> int:
        return int(min(duration, self.firing_time) * self.spawn_rate) + 1

    def positions(self, count: int) -> np.ndarray:
        origin = np.asarray(self.origin, dtype=float)[:2]
        heading = _heading(self.direction)
        across = np.array([-heading[1], heading[0]])
        rng = np.random.default_rng(self.seed)
        offsets = self.distribution.offsets(count, rng)
        return origin + (self.width / 2) * offsets[:, None] * across

    def velocities(self, count: int) -> np.ndarray:
        heading = _heading(self.direction)
        return np.tile(self.velocity * heading, (count, 1))

    def colors(self, count: int) -> list[ManimColor]:
        return self.coloring.colors(count)

    def fired(self, elapsed: float) -> int:
        return int(min(elapsed, self.firing_time) * self.spawn_rate + _TIME_EPS)
