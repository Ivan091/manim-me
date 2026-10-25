from pathlib import Path

from manim import Scene

from light.boundaries import Boundary
from light.cannon import Cannon, RadialCannon
from light.world import World

ASSETS_DIR = Path(__file__).parent / "assets"


class BoundaryScene(Scene):
    simulation_time: int = 15
    boundary: Boundary
    cannon: Cannon = RadialCannon()
    points_radius: float = 0.017

    def construct(self) -> None:
        world = World(self.boundary, self.cannon, self.simulation_time)
        self.add(world.to_mobject(self.points_radius, self))
        self.wait(self.simulation_time)
