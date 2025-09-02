from manim import *

from _utils.WaitingScene import WaitingScene


class RotationTest(WaitingScene):
    def construct(self):
        text = Tex("This is some text").scale(3)
        self.play1(FadeIn(text))


