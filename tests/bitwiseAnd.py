from abc import ABC
from typing import TypeVar, Callable

from colour import Color
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

    def shift_right(self, scene: Scene, f: Callable[[Integer], Integer] = lambda x: x):
        z = zip(self[0:-1], self[1:])
        r = map(lambda x: x[0].animate.move_to(x[1]), z)
        n = f(self.mapper(BitNums(0).move_to(self[0])))
        scene.play(
            AnimationGroup(*r,
                           FadeIn(n, shift=RIGHT),
                           FadeOut(self[-1], shift=RIGHT),
                           )
        )
        self.submobjects = [n, *self.submobjects[:-1]]

    def shift_left(self, scene: Scene, f: Callable[[Integer], Integer] = lambda x: x):
        z = zip(self[1:], self[0:-1])
        r = map(lambda x: x[0].animate.move_to(x[1]), z)
        n = f(self.mapper(BitNums(0).move_to(self[-1])))
        scene.play(
            AnimationGroup(*r,
                           FadeIn(n, shift=LEFT),
                           FadeOut(self[0], shift=LEFT),
                           )
        )
        self.submobjects = [*self.submobjects[1:], n]

    def flip_bit(self, scene: Scene, n: int, f: Callable[[Integer], Integer] = lambda x: x, val_f: Callable[[int], int] = lambda x: 1 - x):
        old_mobj = self[n]
        new_val = val_f(old_mobj.get_value())
        new_mobj = f(self.mapper(Integer(new_val)))
        scene.play(old_mobj.animate.become(new_mobj, match_center=True))
        self[n] = new_mobj

    def flip_bit_math(self, scene: Scene, n: int, f: Callable[[Integer], Integer] = lambda x: x, val_f: Callable[[int], int] = lambda x: 1 - x):
        return self.flip_bit(scene, -n - 1, f, val_f)

    def map(self, f: Callable[[Integer], Integer]) -> 'BitNums':
        return BitNums(*map(f, self.submobjects), mapper=f)


class BitAnd(WaitingScene):
    @staticmethod
    def default(x: Integer) -> Integer:
        return x.scale(4)

    @staticmethod
    def to_blue(x: Integer) -> Integer:
        return x.set_color(Color(BLUE))

    @staticmethod
    def to_yellow(x: Integer) -> Integer:
        return x.set_color(Color(YELLOW))

    def construct(self):
        num0 = BitNums(1, 0, 1, 1, mapper=self.default)
        # num1 = BitNums(0, 0, 0, 0, mapper=self.default)
        # num2 = BitNums(1, 0, 0, 0, mapper=self.default)
        # VGroup(*num0, *num1, *num2).arrange_in_grid(rows=3, cols=len(num0), buff=MED_LARGE_BUFF).move_to(ORIGIN)
        # self.add(num0, num1, num2, Underline(num1))
        self.add(num0)
        # self.play(num0.shift_left(self.to_yellow))
        # self.play(num0.flip_bit(0))
        #
        self.wait()

        num0.flip_bit(self, 2, f=self.to_yellow)
        num0.flip_bit(self, 2, f=self.to_blue)

        num0.shift_right(self, self.to_yellow)
        num0.shift_right(self, self.to_yellow)
        num0.shift_right(self, self.to_yellow)
        num0.shift_right(self, self.to_yellow)
        #
        # self.play(num0.flip_bit(0))
        # self.play(num0.flip_bit(0))

        self.wait()
