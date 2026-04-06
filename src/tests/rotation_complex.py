from manim import *

from _utils.MeineLiebeScene import MeineLiebeScene


class RotationTest(MeineLiebeScene):
    def construct(self):
        sq = Square(color=ORANGE, side_length=2, stroke_width=2)
        self.add(sq)
        self.play1(sq.copy().set_color(BLUE).animate.apply_complex_function(lambda z: z ** 3))
