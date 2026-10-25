from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from manim import Scene


class Sound(ABC):
    @abstractmethod
    def play(self, scene: Scene, count: int, within: float) -> None: ...


@dataclass(frozen=True)
class Silence(Sound):
    def play(self, scene: Scene, count: int, within: float) -> None:
        return


@dataclass(frozen=True)
class Sample(Sound):
    path: Path | str
    gain: float | None = None

    def play(self, scene: Scene, count: int, within: float) -> None:
        for i in range(count):
            scene.add_sound(str(self.path), time_offset=within * i / count, gain=self.gain)
