from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from manim import Scene


class Sound(ABC):
    @abstractmethod
    def play(self, scene: Scene, start: int, count: int, within: float) -> None: ...


@dataclass(frozen=True)
class Silence(Sound):
    def play(self, scene: Scene, start: int, count: int, within: float) -> None:
        return


@dataclass(frozen=True)
class Sample(Sound):
    path: Path | str
    gain: float = 0.0
    every: int = 1
    every_jitter: float = 0.0
    gain_jitter: float = 0.0
    seed: int = 0
    _pops: list[tuple[int, float, float]] = field(default_factory=list, init=False, repr=False, compare=False)

    def __post_init__(self):
        if self.every < 1:
            raise ValueError(f"every must be at least 1, got {self.every}")
        if self.every_jitter < 0 or self.gain_jitter < 0:
            raise ValueError(f"jitters must not be negative, got {self.every_jitter} and {self.gain_jitter}")

    def play(self, scene: Scene, start: int, count: int, within: float) -> None:
        end = start + count
        self._schedule_until(end)
        for index, gain, phase in self._pops:
            if start <= index < end:
                scene.add_sound(str(self.path), time_offset=within * phase, gain=gain)

    def _schedule_until(self, end: int) -> None:
        pops = self._pops
        while not pops or pops[-1][0] < end:
            rng = np.random.default_rng([self.seed, len(pops)])
            gap = max(1, round(rng.normal(self.every, self.every_jitter)))
            last = pops[-1][0] if pops else -1
            pops.append((last + gap, self.gain + rng.normal(0.0, self.gain_jitter), rng.random()))
