from manim import *

from _utils.WaitingScene import WaitingScene

axis_config = {
    'tip_length': 0.2,
    'color': BLUE,
    'exclude_origin_tick': True,
}


class Function(WaitingScene):
    def construct(self):
        axes = Axes(y_range=[-10, 10, 1], x_range=[-3, 4, 1], axis_config=axis_config)
        points = [[0, 0, 0], [1, 2, 0], [2, 1, 0]]
        points = list(map(lambda x: axes.coords_to_point(*x), points))
        self.add(axes, VMobject().set_points_as_corners(points))
