import sys

sys.path.append("../")

from manim import *
from _utils.WaitingScene import WaitingScene


class Thumbnail(WaitingScene):
    def construct(self):
        t = Text("null").set_color(RED).scale(2)
        demon = SVGMobject("svg/demon3.svg").set_color(RED).next_to(t, buff=MED_SMALL_BUFF).scale(1.5)
        obj = VGroup(t, demon).move_to(ORIGIN).scale(2)
        self.add(obj)
