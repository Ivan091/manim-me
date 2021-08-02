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
        self.kwargs = kwargs
        super().__init__(begin_fun(begin), finish_fun(finish), **kwargs)
        self.add_updater(lambda x: update_arrow(x, begin, finish, begin_fun, finish_fun, **kwargs))


class FollowingLine(Line):
    def __init__(
            self,
            begin: Mobject,
            finish: Mobject,
            begin_fun=lambda t: t,
            finish_fun=lambda t: t,
            **kwargs
    ):
        self.kwargs = kwargs
        super().__init__(begin_fun(begin), finish_fun(finish), **kwargs)
        self.add_updater(lambda x: update_line(x, begin, finish, begin_fun, finish_fun, **kwargs))


def update_line(line: Line, begin: Mobject, finish: Mobject, begin_fun=lambda t: t, finish_fun=lambda t: t, **kwargs):
    line.match_points(Line(begin_fun(begin), finish_fun(finish), **kwargs))


def update_arrow(arrow: Line, begin: Mobject, finish: Mobject, begin_fun=lambda t: t, finish_fun=lambda t: t, **kwargs):
    arrow.match_points(Arrow(begin_fun(begin), finish_fun(finish), **kwargs))
