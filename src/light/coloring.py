from abc import ABC, abstractmethod
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
    color_gradient,
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


class Coloring(ABC):
    @abstractmethod
    def colors(self, count: int) -> list[ManimColor]: ...


@dataclass(frozen=True)
class StaticColor(Coloring):
    color: ManimColor = PALETTE[0]

    def colors(self, count: int) -> list[ManimColor]:
        return [self.color] * count


@dataclass(frozen=True)
class Palette(Coloring):
    fractions: Sequence[float] = (1,)
    start_angle: float = 0.0

    def __post_init__(self):
        if not 0 < len(self.fractions) <= len(PALETTE):
            raise ValueError(
                f"expected 1 to {len(PALETTE)} fractions, "
                f"got {len(self.fractions)}"
            )
        if min(self.fractions) <= 0:
            raise ValueError(f"fractions must be positive: {self.fractions}")

    def colors(self, count: int) -> list[ManimColor]:
        weights = np.asarray(self.fractions, dtype=float)
        edges = np.round(
            np.cumsum(weights) / weights.sum() * count
        ).astype(int)
        point_ids = np.arange(count)
        idx = np.searchsorted(edges, point_ids, side="right")

        # rotate the whole color layout:
        # point i has angle i * TAU / count
        shift = int(round(self.start_angle / TAU * count))
        idx = np.roll(idx, shift)
        return [PALETTE[i] for i in idx]


@dataclass(frozen=True)
class Gradient(Coloring):
    stops: Sequence[ManimColor] = (BLUE, PURPLE)

    def __post_init__(self):
        if len(self.stops) < 2:
            raise ValueError(
                f"a gradient needs at least 2 stops, got {len(self.stops)}"
            )

    def colors(self, count: int) -> list[ManimColor]:
        return color_gradient(self.stops, count)
