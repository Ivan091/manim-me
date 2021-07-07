from abc import ABC

from colour import Color
from manim import *

colors = [
    RED_A,
    RED_B,
    RED_D,
    RED_E,
    BLUE_A,
    BLUE_E,
    PURPLE,
]

fractalDepth = 7

smallFractalDepth = 5


def create_line(color_of_base: Color, color_of_center: Color) -> VGroup:
    return VGroup(
        Line(LEFT * 3, LEFT, stroke_width=2).set_color(color_of_base),
        Line(LEFT, UP * 2, stroke_width=2).set_color(color_of_center),
        Line(UP * 2, RIGHT, stroke_width=2).set_color(color_of_center),
        Line(RIGHT, RIGHT * 3, stroke_width=2).set_color(color_of_base)
    )


class Triangle(VGroup):
    def __init__(self, a: np.ndarray, b: np.ndarray, c: np.ndarray, **kwargs):
        VGroup.__init__(
            self,
            Line(a, b, **kwargs),
            Line(b, c, **kwargs),
            Line(c, a, **kwargs),
        )

    def get_vertex(self, vertex_number: int) -> np.ndarray:
        return self[vertex_number].get_start()


class TriangleDots(VGroup):
    def __init__(self, a: np.ndarray, b: np.ndarray, c: np.ndarray, stroke_width=DEFAULT_STROKE_WIDTH, radius=DEFAULT_SMALL_DOT_RADIUS, **kwargs):
        VGroup.__init__(
            self,
            Line(a, b, stroke_width=stroke_width),
            Line(b, c, stroke_width=stroke_width),
            Line(c, a, stroke_width=stroke_width),
            Dot(a, radius=radius),
            Dot(b, radius=radius),
            Dot(c, radius=radius),
            **kwargs
        )

    def get_vertex(self, vertex_number: int) -> np.ndarray:
        return self[vertex_number + 3].get_center()

    def get_vertexes(self) -> np.ndarray:
        return np.array([self.get_vertex(0), self.get_vertex(1), self.get_vertex(2)])


class TriangleOuter(Scene):
    def construct(self):
        fractal = create_line(WHITE, WHITE).scale(2)
        self.play(Write(fractal))
        for j in range(smallFractalDepth):
            newFractal = VGroup()
            for line in fractal:
                b = create_line(line.get_color(), colors[j])
                b.rotate(line.get_angle()) \
                    .scale(np.linalg.norm(line.get_end() - line.get_start()) / np.linalg.norm(b[0].get_start() - b[3].get_end())) \
                    .shift(line.get_start() - b[0].get_start())
                newFractal.add(*b)
            self.play(Transform(fractal, newFractal))
        self.play(Unwrite(fractal))
        self.wait(1)


class TriangleInner(Scene):
    def construct(self):
        firstTriangle = Triangle(LEFT * 7 + DOWN * 3, LEFT * 4 + UP * 3.8, RIGHT * 7 + DOWN * 3)
        self.play(Write(firstTriangle))
        fractal = VGroup(firstTriangle)
        deepestLevel = VGroup(firstTriangle)
        for j in range(fractalDepth):
            visualTriangles = VGroup()
            utilTriangles = VGroup()
            for triangle in deepestLevel:
                centers = [line.get_center() for line in triangle]
                visualTriangles.add(Triangle(*centers).set_color(colors[j])).set_stroke(width=2)
                utilTriangles.add(
                    Triangle(triangle.get_vertex(0), centers[0], centers[2]),
                    Triangle(triangle.get_vertex(1), centers[1], centers[0]),
                    Triangle(triangle.get_vertex(2), centers[2], centers[1]),
                )
            self.play(Write(visualTriangles))
            fractal.add(visualTriangles)
            deepestLevel = utilTriangles
        self.play(Unwrite(fractal))
        self.wait(1)


class TriangleOut(MovingCameraScene):
    def construct(self):
        initTr = TriangleDots(LEFT + DOWN, UP * 0.5, RIGHT + DOWN, radius=0.02)
        fr = [initTr, *initTr.get_vertexes()]
        self.play(Write(initTr))
        for j in range(fractalDepth):
            tr = fr[0]
            tr1 = tr.copy().set_color(colors[j])
            tr1.shift(fr[2] - fr[1])
            tr2 = tr.copy().set_color(colors[j])
            tr2.shift(fr[3] - fr[1])

            newGr = VGroup(*tr, *tr1, *tr2)
            fr[0] = newGr
            fr[2] += fr[2] - fr[1]
            fr[3] += fr[3] - fr[1]

            animBolder = []
            for obj in newGr:
                if type(obj) is not Dot:
                    animBolder.append(obj.animate.set_stroke(width=(1 + j) * 4))
                else:
                    animBolder.append(obj.animate.scale(1.4))

            self.play(
                TransformFromCopy(tr.copy(), tr1),
                TransformFromCopy(tr.copy(), tr2),
                self.camera.frame.animate(run_time=2).set_width(newGr.width * 2).move_to(newGr),
                *animBolder
            )
        self.play(Unwrite(fr[0]))
        self.wait(1)
