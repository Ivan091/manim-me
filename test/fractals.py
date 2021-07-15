from typing import Optional, Callable

from colour import Color
from manim import *

colors = [
    BLUE_A,
    BLUE_B,
    BLUE_C,
    BLUE_D,
    PURPLE_C,
    PURPLE_D,
    PURPLE_E,
]

fractalDepth = 7

smallFractalDepth = 5


def combine_points(new_m: Mobject, base_point: np.ndarray, new_point: np.ndarray) -> Mobject:
    return new_m.shift(base_point - new_point)


class TriangleOuter(Scene):
    @staticmethod
    def create_line(color_of_base: Color, color_of_center: Color) -> VGroup:
        return VGroup(
            Line(LEFT * 3, LEFT, stroke_width=2).set_color(color_of_base),
            Line(LEFT, UP * 2, stroke_width=2).set_color(color_of_center),
            Line(UP * 2, RIGHT, stroke_width=2).set_color(color_of_center),
            Line(RIGHT, RIGHT * 3, stroke_width=2).set_color(color_of_base)
        )

    def construct(self):
        fractal = self.create_line(WHITE, WHITE).scale(2)
        self.play(Write(fractal))
        for j in range(smallFractalDepth):
            newFractal = VGroup()
            for line in fractal:
                b = self.create_line(line.get_color(), colors[j])
                b.rotate(line.get_angle()) \
                    .scale(np.linalg.norm(line.get_end() - line.get_start()) / np.linalg.norm(b[0].get_start() - b[3].get_end())) \
                    .shift(line.get_start() - b[0].get_start())
                newFractal.add(*b)
            self.play(Transform(fractal, newFractal))
        self.play(Unwrite(fractal))
        self.wait(1)


class TriangleInner(Scene):
    @staticmethod
    def find_centers_of_sides(poly: Polygon) -> []:
        ps = poly.get_points()[::4]
        return [
            (ps[0] + ps[1]) * 0.5,
            (ps[1] + ps[2]) * 0.5,
            (ps[2] + ps[0]) * 0.5,
        ]

    def construct(self):
        initTr = Polygon(LEFT * 7 + DOWN * 3, LEFT * 4 + UP * 3.8, RIGHT * 7 + DOWN * 3, color=WHITE)
        fr = VGroup(initTr)
        deepestLevel = VGroup(initTr)
        self.play(Write(initTr))
        for j in range(fractalDepth):
            visualTr = VGroup()
            utilTr = VGroup()
            for tr in deepestLevel:
                centers = self.find_centers_of_sides(tr)
                visualTr.add(Polygon(*centers, color=colors[j], stroke_width=2))
                vertexes = tr.get_points()[::4]
                utilTr.add(
                    Polygon(vertexes[0], centers[0], centers[2]),
                    Polygon(vertexes[1], centers[1], centers[0]),
                    Polygon(vertexes[2], centers[2], centers[1]),
                )
            self.play(Write(visualTr))
            fr.add(visualTr)
            deepestLevel = utilTr
        self.play(Unwrite(fr))
        self.wait(1)


class TriangleOut(MovingCameraScene):
    def construct(self):
        initTr = Polygon(LEFT + DOWN, UP * 0.5, RIGHT + DOWN, color=WHITE)
        fr = VGroup(initTr)
        self.play(Write(initTr))
        for j in range(fractalDepth):
            copyTop = fr.copy().set_color(colors[j])
            copyRight = fr.copy().set_color(colors[j])
            combine_points(copyTop, fr.get_boundary_point(UP), copyTop.get_boundary_point(LEFT))
            combine_points(copyRight, fr.get_boundary_point(RIGHT), copyRight.get_boundary_point(LEFT))
            oldFr = fr.copy()
            fr.add(copyRight, copyTop)
            self.play(
                TransformFromCopy(oldFr.copy(), copyTop),
                TransformFromCopy(oldFr.copy(), copyRight),
                self.camera.frame.animate(run_time=2).set_width(fr.width * 2).move_to(fr),
                fr.animate.set_stroke(width=(j + 1) * 4)
            )
        self.play(Unwrite(fr))
        self.wait(1)


class Tree(Scene):
    left_vt = ValueTracker(0.01)
    right_vt = ValueTracker(-0.01)

    @staticmethod
    def _root_updater(m: Line, vt: ValueTracker, root: Line):
        m.put_start_and_end_on(root.get_end(), m.get_end())
        m.set_angle(root.get_angle() + vt.get_value())

    def _create_subtree(self, root: Line, depth: int, length: float):
        if depth >= fractalDepth:
            return
        end = root.get_end()
        left = Line(end, end + UP * length, stroke_width=3).add_updater(lambda m: self._root_updater(m, self.left_vt, root)).set_color(colors[depth])
        right = Line(end, end + UP * length, stroke_width=3).add_updater(lambda m: self._root_updater(m, self.right_vt, root)).set_color(colors[depth])
        root.add(left)
        root.add(right)
        depth += 1
        length *= 0.66
        self._create_subtree(left, depth, length)
        self._create_subtree(right, depth, length)

    def create_tree(self):
        length = 1.9
        root = Line(DOWN * 5, DOWN * 1.3, stroke_width=3)
        self._create_subtree(root, 0, length)
        return root

    def construct(self):
        self.add(self.create_tree())
        self.play(
            self.left_vt.animate(run_time=15, rate_func=linear).set_value(PI * 3 / 4),
            self.right_vt.animate(run_time=15, rate_func=linear).set_value(-PI * 3 / 4)
        )
        self.wait()


class Fibonacci(Scene):
    directions = [UR, DR, DL, UL]

    def get_dir(self, j: int):
        return self.directions[j % 4]

    def add_sub(self, parent: Rectangle, dir_idx: int) -> Rectangle:
        if dir_idx % 2 == 0:
            rect = Rectangle(width=parent.width * 0.38, height=parent.height)
        else:
            rect = Rectangle(width=parent.width, height=parent.height * 0.38)
        return rect.align_to(parent, self.directions[dir_idx])

    def create_spiral(self, gr: VGroup) -> VGroup:
        line = VGroup()
        for j in range(len(gr) - 1):
            line.add(
                CubicBezier(
                    gr[j].get_boundary_point(self.get_dir(j + 2)),
                    gr[j].get_boundary_point(self.get_dir(j + 2)) * 0.45 + gr[j].get_boundary_point(self.get_dir(j + 3)) * 0.55,
                    gr[j + 1].get_boundary_point(self.get_dir(j + 3)) * 0.45 + gr[j].get_boundary_point(self.get_dir(j + 3)) * 0.55,
                    gr[j + 1].get_boundary_point(self.get_dir(j + 3)),
                    z_index=1,
                    stroke_width=2
                )
            )
        return line

    def construct(self):
        baseRect = Rectangle(width=12, height=7)
        gr = VGroup(baseRect)
        for j in range(fractalDepth):
            rect = self.add_sub(gr[j], j % 4).set_fill(colors[j], opacity=1)
            gr.add(rect)
        gr.set_stroke(width=2)
        spiral = self.create_spiral(gr).set_color_by_gradient(RED, BLACK)
        self.play(Write(gr[0]))
        for j in range(len(gr) - 1):
            self.play(
                TransformFromCopy(gr[j], gr[j + 1], run_time=0.5),
                Create(spiral[j]),
            )
        self.wait(1)
