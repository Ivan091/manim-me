from manim import *
from tests.gravity_simulation import Trace


class Following(Scene):
    def construct(self):
        d = Dot()
        t = Trace(d.get_center, 800).add_updater(lambda m, dt: m.shift(LEFT * 0.05)).start_trace().set_color_by_gradient([WHITE, BLUE, PURE_BLUE])
        self.add(t)
        self.play(d.animate.shift(UP))
        self.play(d.animate.shift(RIGHT * 4))
        c = Circle(stroke_width=20, color=RED, stroke_opacity=0.4).rotate(-PI / 2)
        c.shift(d.get_center() - c.get_start())
        self.play(
            Succession(
                FadeIn(c),
                MoveAlongPath(d, c, run_time=2),
                MoveAlongPath(d, c, run_time=1.5),
                MoveAlongPath(d, c, run_time=1),
                MoveAlongPath(d, c, run_time=0.5),
                FadeOut(c),
            ),
        )
        p = VMobject(stroke_width=20, color=YELLOW, stroke_opacity=0.4).set_points_smoothly([UP * 2, UR, ORIGIN, DL, DOWN * 2, DR, ORIGIN, UL, UP * 2])
        p.shift(d.get_center() - p.get_start())
        self.play(
            Succession(
                FadeIn(p),
                MoveAlongPath(d, p, run_time=2),
                MoveAlongPath(d, p, run_time=1.5),
                MoveAlongPath(d, p, run_time=1),
                MoveAlongPath(d, p, run_time=0.5),
                FadeOut(p),
            ),
        )
        self.wait()
