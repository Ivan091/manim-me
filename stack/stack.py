import sys

sys.path.append("../")
from utils.WaitingScene import *
from utils.SourceCode import SourceCode
from manim import *


class Stack(WaitingScene):
    def construct(self):
        listing = SourceCode("code/stack.txt", "java").scale(1.4)
        finger = SVGMobject("../common/assets/finger.svg").scale(0.2).set_color(WHITE).next_to(listing.line(1), LEFT)
        VGroup(listing, finger).to_edge(LEFT)
        VGroup(listing, finger).to_edge(LEFT)
        stack = StackAnimated(Dot().move_to(RIGHT * 4 + DOWN * 2))
        self.play_wait(Write(listing))
        self.play_wait(Write(finger))
        self.play_wait(stack.push(VGroup(Square(1.3), Text("1"))), finger.animate.next_to(listing.line(2), LEFT))
        self.play_wait(stack.push(VGroup(Square(1.3), Text("2"))), finger.animate.next_to(listing.line(3), LEFT))
        self.play_wait(stack.push(VGroup(Square(1.3), Text("3"))), finger.animate.next_to(listing.line(4), LEFT))
        self.play_wait(stack.pull(), FadeOut(finger))


class StackAnimated:
    def __init__(self, start: np.ndarray):
        self.base_pos = start
        self.items = []

    def push(self, item: VMobject) -> Animation:
        if not self.items:
            item.move_to(self.base_pos)
        else:
            item.next_to(self.items[-1], UP, SMALL_BUFF)
        self.items.append(item)
        return FadeIn(item, shift=DOWN)

    def pull(self) -> Animation:
        last_item = self.items[-1]
        self.items.pop()
        return FadeOut(last_item, shift=UP)

