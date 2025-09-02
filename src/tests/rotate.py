from manim import *


class Rotating1(Scene):
    def construct(self):
        a = Square()
        self.add(a)
        self.wait()
        self.play(
            AnimationGroup(
                a.animate.shift(LEFT * 2).set_color(RED),
                Rotating(
                    a,
                    run_time=1,
                    rate_func=smooth,
                    radians=PI,
                ),
            )
        )
        self.wait()
