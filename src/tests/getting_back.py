from manim import *

from utils.MeineLiebeScene import MeineLiebeScene


class RotationTest(MeineLiebeScene):
    def construct(self):
        text = Tex("This is some text").scale(3)
        self.play1(FadeIn(text))


