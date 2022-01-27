from abc import ABC
from typing import TypeVar, Callable

from manim import *

from _utils.WaitingScene import WaitingScene

T = TypeVar('T')


class BitNums(VGroup, ABC):
    def __init__(self,
                 *bits: int,
                 mapper: Callable[[Integer], Integer] = lambda x: x,
                 ):
        def bit_mapper(x: int) -> Integer:
            return mapper(Integer(x))

        super().__init__(*map(bit_mapper, bits))
        for m1, m2 in zip(self.submobjects, self.submobjects[1:]):
            m2.move_to(m1.get_center() + RIGHT * m1.height)
        self.center()
        self.mapper = mapper

    def shift_right(self, f: Callable[[Integer], Integer] = lambda x: x) -> AnimationGroup:
        z = zip(self[0:-1], self[1:])
        r = map(lambda x: x[0].animate.move_to(x[1]), z)
        n = f(self.mapper(BitNums(0).move_to(self[0])))
        acc = AnimationGroup(*r,
                             FadeIn(n, shift=RIGHT),
                             FadeOut(self[-1], shift=RIGHT),
                             )
        self.submobjects = [n, *self.submobjects[:-1]]
        return acc

    def map(self, f: Callable[[Integer], Integer]) -> 'BitNums':
        return BitNums(*map(f, self.submobjects), mapper=f)


class BitAnd(WaitingScene):
    @staticmethod
    def default(x: Integer) -> Integer:
        return x.scale(1)

    @staticmethod
    def right(x: Integer) -> Integer:
        return x.set_color(RED)

    def construct(self):
        num0 = BitNums(1, 0, 1, 1, 0, mapper=self.default)
        num1 = BitNums(0, 0, 0, 0, mapper=self.default)
        num2 = BitNums(1, 0, 0, 0, mapper=self.default)
        VGroup(*num0, *num1, *num2).arrange_in_grid(rows=3, cols=len(num0), buff=MED_LARGE_BUFF).move_to(ORIGIN)
        self.add(num0, num1, num2, Underline(num1))
        self.wait()
