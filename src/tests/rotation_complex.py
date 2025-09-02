from manim import *

from _utils.WaitingScene import WaitingScene


class RotationTest(WaitingScene):
    def construct(self):
        sq = Square(color=ORANGE, side_length=2, stroke_width=2)
        self.add(sq)
        self.play1(sq.copy().set_color(BLUE).animate.apply_complex_function(lambda z: z ** 3))
