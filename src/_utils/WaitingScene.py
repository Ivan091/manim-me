from typing import Any

from manim import *
from manim.mobject.mobject import _AnimationBuilder
from manim.typing import Vector3D


class WaitingScene(Scene):
    wait_time = 0.2

    def play(
            self,
            *args: Animation | Mobject | _AnimationBuilder,
            **kwargs: Any,
    ) -> None:
        super().play(*args, **kwargs)
        super().play(Wait(self.wait_time))

    def tag_vgroup(self, group: VGroup, color: ManimColor = GREEN, direction: Vector3D = UP):
        tags = VGroup()
        for i, vm in enumerate(group):
            tags.add(
                Text(str(i), font_size=10).next_to(vm, direction).set_color(color)
            )

        self.add(tags)


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
