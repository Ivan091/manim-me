import sys

sys.path.append("../")
from _utils.WaitingScene import *
from _utils.SourceCode import SourceCode, make_code_scene
from manim import *


class NullAlways(WaitingScene):
    def construct(self):
        listing = SourceCode("src/NullAlways.java", "java").move_to(ORIGIN).scale(2)
        self.play1(Write(listing))
        self.play1(FadeOutAndShift(listing))


class NullHandle(WaitingScene):
    def construct(self):
        l1 = SourceCode("src/NullHandlingSmall.java", "java")
        l2 = SourceCode("src/NullHandlingPolluted.java", "java")
        group = VGroup(l1, l2).scale(1.8)
        group.arrange(RIGHT, 2)
        self.play1(Write(l1))
        self.play1(Write(l2))
        self.play(FadeOut(group))


class LambdaProcessing(WaitingScene):
    def construct(self):
        l1 = SourceCode("src/LambdaSmall.java", "java")
        l2 = SourceCode("src/LambdaPolluted.java", "java")
        gr = VGroup(l1, l2).scale(1.2).arrange(RIGHT, 1)
        self.play1(Write(l1))
        self.play1(Write(l2))
        self.play1(FadeOut(gr))


class NullSometimes(WaitingScene):
    def construct(self):
        listing = SourceCode("src/NullSometimes.java", "java").move_to(ORIGIN).scale(1.5)
        self.play1(Write(listing))
        self.play1(FadeOut(listing))


class NullObject(WaitingScene):
    def construct(self):
        listing = SourceCode("src/NullObject.java", "java").move_to(ORIGIN).scale(1.5)
        label = Text("Null object")
        make_code_scene(self, listing, label)


class Optional(WaitingScene):
    def construct(self):
        listing = SourceCode("src/Optional.java", "java").move_to(ORIGIN).scale(1.5)
        label = Text("Nullable")
        self.play1(Write(label))
        self.play1(label.animate.next_to(listing, UP))
        self.play1(Write(listing))
        self.play1(Write(listing, rate_func=lambda t: smooth(1 - t)),
                       Write(label, rate_func=lambda t: smooth(1 - t)))


class FailFast(WaitingScene):
    def construct(self):
        listing = SourceCode("src/FailFast.java", "java").move_to(ORIGIN).scale(1)
        label = Text("Fail fast")
        make_code_scene(self, listing, label)
