from typing import Sequence

from manim import *


class Turtle:
    def __init__(self, init_pos: np.ndarray, angle: float):
        self.angle = angle
        self.path = [init_pos]

    def rotate(self, dr: float):
        self.angle += dr

    def go(self, speed: float):
        new_pos = np.array(self.get_pos(), copy=True)
        new_pos[0] += speed * np.cos(self.angle)
        new_pos[1] += speed * np.sin(self.angle)
        self.path.append(new_pos)

    def get_pos(self) -> np.ndarray:
        return self.path[-1]

    def get_path(self) -> Sequence[np.ndarray]:
        return self.path


class TurtleTest(Scene):
    def construct(self):
        axiom = "F+F+F+F"
        axiom = axiom.replace("F", "F+F-F-F+F")
        axiom = axiom.replace("F", "F+F-F-F+F")
        axiom = axiom.replace("F", "F+F-F-F+F")
        axiom = axiom.replace("F", "F+F-F-F+F")
        t = Turtle(ORIGIN, 0)
        for ch in axiom:
            if ch == "+":
                t.rotate(PI / 2)
            elif ch == "-":
                t.rotate(-PI / 2)
            else:
                t.go(1)
        curve = VMobject().set_points_as_corners(t.get_path()).move_to(ORIGIN).scale_to_fit_height(6)
        self.play(Create(curve, run_time=20))
