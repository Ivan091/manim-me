from typing import Union

from manim import *


class FollowingArrow(Arrow):
    def __init__(
            self,
            begin_fun=lambda: Union[Mobject, np.ndarray],
            finish_fun=lambda: Union[Mobject, np.ndarray],
            **kwargs
    ):
        self.kwargs = kwargs
        super().__init__(begin_fun(), finish_fun(), **kwargs)
        self.add_updater(lambda x: update_arrow(x, begin_fun, finish_fun, **kwargs))


class FollowingLine(Line):
    def __init__(
            self,
            begin_fun=lambda: Union[Mobject, np.ndarray],
            finish_fun=lambda: Union[Mobject, np.ndarray],
            **kwargs
    ):
        self.kwargs = kwargs
        super().__init__(begin_fun(), finish_fun(), **kwargs)
        self.add_updater(lambda x: update_line(x, begin_fun, finish_fun, **kwargs))


def update_line(line: Line, begin_fun=lambda: Union[Mobject, np.ndarray], finish_fun=lambda: Union[Mobject, np.ndarray], **kwargs):
    line.match_points(Line(begin_fun(), finish_fun(), **kwargs))


def update_arrow(arrow: Line, begin_fun=lambda: Union[Mobject, np.ndarray], finish_fun=lambda: Union[Mobject, np.ndarray], **kwargs):
    arrow.match_points(Arrow(begin_fun(), finish_fun(), **kwargs))
