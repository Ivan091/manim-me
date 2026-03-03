from typing import Any

from manim import *
from manim.mobject.mobject import _AnimationBuilder
from manim.typing import Vector3D


class WaitingScene(Scene):
    wait_time = 0.2
    scene_number = Integer(0).set_color(LIGHT_GRAY).move_to(UP * 3.5 + LEFT * 7)

    def setup(self) -> None:
        Tex.set_default(font_size=60)
        Text.set_default(font_size=60)
        self.add(self.scene_number)

    def play(
            self,
            *args: Animation | Mobject | _AnimationBuilder,
            wait_time: float | None = wait_time,
            **kwargs: Any,
    ) -> None:
        super().play(*args, **kwargs)
        self.update_scene_number()
        if wait_time is not None:
            if wait_time > 0:
                super().play(Wait(wait_time))
                self.update_scene_number()
        else:
            super().play(Wait(self.wait_time))
            self.update_scene_number()

    def update_scene_number(self):
        self.scene_number.set_value(self.scene_number.get_value() + 1)

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
