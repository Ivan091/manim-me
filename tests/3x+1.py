from typing import Sequence

from manim import *


def scale_to_fit(dims: Sequence[float], inner: Mobject, buff: float = MED_SMALL_BUFF):
    scale_0 = (dims[0] - 2 * buff) / inner.length_over_dim(0)
    scale_1 = (dims[1] - 2 * buff) / inner.length_over_dim(1)
    scale = min(scale_0, scale_1)
    print(scale_0, scale_1)
    inner.scale(scale)
