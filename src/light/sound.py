from abc import ABC, abstractmethod
from dataclasses import dataclass
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

    def __post_init__(self):
        if self.every < 1:
            raise ValueError(f"every must be at least 1, got {self.every}")
        if self.every_jitter < 0 or self.gain_jitter < 0:
            raise ValueError(f"jitters must not be negative, got {self.every_jitter} and {self.gain_jitter}")

    def play(self, scene: Scene, start: int, count: int, within: float) -> None:
        for i in range(start, start + count):
            block, slot = divmod(i, self.every)
            rng = np.random.default_rng([self.seed, block])
            chosen = round((self.every - 1) / 2 + rng.normal(0.0, self.every_jitter))
            if slot == min(max(chosen, 0), self.every - 1):
                gain = self.gain + rng.normal(0.0, self.gain_jitter)
                scene.add_sound(str(self.path), time_offset=within * (i - start) / count, gain=gain)
