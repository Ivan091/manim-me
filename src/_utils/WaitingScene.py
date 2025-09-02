from manim import *
from manim.mobject.mobject import _AnimationBuilder


class WaitingScene(Scene):
    wait_time = 0.2

    def play1(self, *args: Animation | Mobject | _AnimationBuilder, **kwargs):
        self.play(*args, **kwargs)
        self.wait(duration=self.wait_time)

    def play3(self, *args: Animation | Mobject | _AnimationBuilder, **kwargs):
        self.play(AnimationGroup(*args, run_time=3), **kwargs)

    def play5(self, *args: Animation | Mobject | _AnimationBuilder, **kwargs):
        self.play(AnimationGroup(*args, run_time=5), **kwargs)

    def get_all_vmobjects(self) -> list[VMobject]:
        vmobjects = []
        for item in self.mobjects:
            if isinstance(item, VMobject):
                vmobjects.append(item)
        return vmobjects
