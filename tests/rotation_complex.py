from manim import *

from _utils.WaitingScene import WaitingScene


class RotationTest(WaitingScene):
    def construct(self):
        sq = Square(color=ORANGE, side_length=3)
        self.add(sq)
        a = np.sin(PI)
        b = np.cos(PI)
        point = complex(a, b)
        point /= abs(point)
        self.play_wait(sq.copy().set_color(BLUE).animate.apply_complex_function(lambda z: z * point))
