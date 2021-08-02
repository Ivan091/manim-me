from manim import *

from _utils.WaitingScene import WaitingScene


class GlowLine(WaitingScene):
    def construct(self):
        a = Polygon(UP, DOWN, LEFT)
        b = a.copy().set_stroke(width=50, opacity=0.1)
        self.add(a)
        self.play(Create(b))
