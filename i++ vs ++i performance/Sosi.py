import sys

sys.path.append("../")

from manim.mobject.geometry import ArrowCircleTip
from utils.ArrowMobjectUpdating import ArrowMobjectUpdating
from utils.WaitingScene import *


class Test(WaitingScene):
    def construct(self):
        dot1 = [Dot().move_to(LEFT + UP), Dot().move_to(UP)]
        dot2 = [Dot().move_to(LEFT + DOWN), Dot().move_to(RIGHT * 2 + DOWN)]
        self.add(*dot1, *dot2)
        self.add(ArrowMobjectUpdating(dot1[0], dot1[1], tip_shape=ArrowCircleTip))
        self.add(ArrowMobjectUpdating(dot2[0], dot2[1], tip_shape=ArrowCircleTip))
        self.play_wait(dot1[1].animate().move_to(RIGHT * 2 + UP))
        # arr = VGroup(*[Dot() for _ in range(2)])
        # arr.arrange(RIGHT, 1)
        # self.add(arr)
        # arrow = VGroup(ArrowMobjectUpdating(arr[0], arr[1]))
        # self.add(arrow)
        # self.play_wait(arr[1].animate().move_to(arr[0].get_boundary_point(RIGHT) + RIGHT))
        # self.play_wait(arr[1].animate().move_to(UP * 3))
        # self.play_wait(arr[1].animate().move_to(arr[0].get_center() + RIGHT))
