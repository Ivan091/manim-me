from abc import ABC

from manim import *
from manim.mobject.geometry import ArrowTriangleFilledTip


class ArrowMobject(Arrow, ABC):
    def __init__(
            self,
            begin: Mobject,
            finish: Mobject,
            stroke_width=6,
            buff=MED_SMALL_BUFF,
            max_tip_length_to_length_ratio=0.25,
            max_stroke_width_to_length_ratio=5,
            preserve_tip_size_when_scaling=False,
            **kwargs
    ):
        self.max_tip_length_to_length_ratio = (
            max_tip_length_to_length_ratio
        )
        self.max_stroke_width_to_length_ratio = (
            max_stroke_width_to_length_ratio
        )
        self.preserve_tip_size_when_scaling = (
            preserve_tip_size_when_scaling
        )
        tip_shape = kwargs.pop("tip_shape", ArrowTriangleFilledTip)
        Line.__init__(self, begin, finish, buff=buff, stroke_width=stroke_width, **kwargs)

        self.begin = begin
        self.finish = finish

        self.initial_stroke_width = self.stroke_width
        self.add_tip(tip_shape=tip_shape)
        update_arrow_mobject(self)
        self.set_stroke_width_from_length()

    def add_default_updater(self):
        self.add_updater(update_arrow_mobject)
        return self


def update_arrow_mobject(arrow: ArrowMobject):
    arrow.set_start_and_end_attrs(arrow.begin, arrow.finish)
    arrow.put_start_and_end_on(arrow.start, arrow.end)
    arrow.account_for_buff()
    arrow.reset_endpoints_based_on_tip(arrow.tip, False)
    arrow.position_tip(arrow.tip)
    arrow.tip.width = arrow.get_default_tip_length()


def update_arrow_mobject_transform(arrow: ArrowMobject, source: Mobject, destination: Mobject):
    arrow.begin = source
    arrow.finish = destination
    update_arrow_mobject(arrow)


def update_arrow(arrow: Arrow, source: Mobject, destination: Mobject):
    arrow.set_start_and_end_attrs(source, destination)
    arrow.put_start_and_end_on(arrow.start, arrow.end)
    arrow.account_for_buff()
    arrow.reset_endpoints_based_on_tip(arrow.tip, at_start=False)
