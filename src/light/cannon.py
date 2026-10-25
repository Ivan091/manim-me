import math
from dataclasses import dataclass
from typing import Final, Sequence

import numpy as np
from manim import (
    BLUE,
    GREEN,
    ORANGE,
    PINK,
    PURPLE,
    RED,
    TAU,
    TEAL,
    YELLOW,
    ManimColor,
)

PALETTE: Final[tuple[ManimColor, ...]] = (
    BLUE,
    ORANGE,
    GREEN,
    PINK,
    YELLOW,
    PURPLE,
    RED,
    TEAL,
)

INSTANT: Final[float] = math.inf


@dataclass(frozen=True)
class Cannon:
    origin: Sequence[float] = (0.0, 0.0)
    amount: int = 5760
    velocity: float = 1.3
    color_fractions: Sequence[float] = ()
    color_start_angle: float = 0.0
    spawn_rate: float = INSTANT

    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError(f"amount must be positive, got {self.amount}")
        if self.spawn_rate <= 0:
            raise ValueError(
                f"spawn_rate must be positive, got {self.spawn_rate}"
            )
        if len(self.color_fractions) > len(PALETTE):
            raise ValueError(
                f"at most {len(PALETTE)} fractions, "
                f"got {len(self.color_fractions)}"
            )

    def positions(self) -> np.ndarray:
        origin = np.asarray(self.origin, dtype=float)[:2]
        return np.tile(origin, (self.amount, 1))

    def velocities(self) -> np.ndarray:
        angles = np.linspace(0, TAU, self.amount, endpoint=False)
        directions = np.stack([np.cos(angles), np.sin(angles)], axis=1)
        return self.velocity * directions

    def colors(self) -> list[ManimColor]:
        if not self.color_fractions:
            return [PALETTE[0]] * self.amount

        weights = np.asarray(self.color_fractions, dtype=float)
        edges = np.round(
            np.cumsum(weights) / weights.sum() * self.amount
        ).astype(int)
        point_ids = np.arange(self.amount)
        idx = np.searchsorted(edges, point_ids, side="right")

        # rotate the whole color layout:
        # point i has angle i * TAU / amount
        shift = int(round(self.color_start_angle / TAU * self.amount))
        idx = np.roll(idx, shift)
        return [PALETTE[i] for i in idx]

    def fired(self, elapsed: float) -> int:
        if math.isinf(self.spawn_rate):
            return self.amount
        return min(self.amount, int(elapsed * self.spawn_rate))
