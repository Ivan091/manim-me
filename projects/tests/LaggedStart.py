import sys

sys.path.append("../../")
from projects.utils.ArrowMobjectUpdating import *
from manim import *


class LaggedStartTest(Scene):
    def construct(self):
        items = VGroup(*[Dot() for _ in range(2)])
        items.arrange(RIGHT, 2)
        arrow = ArrowMobjectUpdating(items[0], items[1]).add_default_updater().set_color(BLUE)
        self.add(items, arrow)
        azari = SVGMobject("../common/assets/azari_colorful.svg").set_color(WHITE).move_to(items[0].get_center())
        # arrow.clear_updaters()
        # arrow.add_updater(lambda a: update_arrow_mobject_transform(a, items[0], items[1]))
        self.play(
            AnimationGroup(
                ReplacementTransform(
                    items[0],
                    azari,
                    run_time=0.5
                ),
                arrow.animate.set_color(RED)
            )
        )
        self.wait(1)


def dot_func(mob: VMobject) -> VMobject:
    mob.shift(UP * 3)
    return mob
