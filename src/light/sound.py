from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

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
    gain: float | None = None
    every: int = 1

    def __post_init__(self):
        if self.every < 1:
            raise ValueError(f"every must be at least 1, got {self.every}")

    def play(self, scene: Scene, start: int, count: int, within: float) -> None:
        for i in range(start, start + count):
            if i % self.every == 0:
                scene.add_sound(str(self.path), time_offset=within * (i - start) / count, gain=self.gain)
