from manim import *


class FollowingArrow(Arrow):
    def __init__(
            self,
            begin: Mobject,
            finish: Mobject,
            begin_fun=lambda t: t,
            finish_fun=lambda t: t,
            **kwargs
    ):
        super().__init__(begin_fun(begin), finish_fun(finish), **kwargs)
        self.add_updater(lambda x: update_arrow(x, begin, finish, begin_fun, finish_fun))


class FollowingLine(Line):
    def __init__(
            self,
            begin: Mobject,
            finish: Mobject,
            begin_fun=lambda t: t,
            finish_fun=lambda t: t,
            **kwargs
    ):
        super().__init__(begin_fun(begin), finish_fun(finish), **kwargs)
        self.add_updater(lambda x: update_line(x, begin, finish, begin_fun, finish_fun))


def update_line(arrow: Line, begin: Mobject, finish: Mobject, begin_fun=lambda t: t, finish_fun=lambda t: t):
    arrow.set_start_and_end_attrs(begin_fun(begin), finish_fun(finish))
    arrow.put_start_and_end_on(arrow.start, arrow.end)
    arrow.generate_points()


def update_arrow(arrow: Arrow, begin: Mobject, finish: Mobject, begin_fun=lambda t: t, finish_fun=lambda t: t):
    update_line(arrow, begin_fun(begin), finish_fun(finish))
    arrow.tip.width = arrow.get_default_tip_length()
    arrow.reset_endpoints_based_on_tip(arrow.tip, False)
