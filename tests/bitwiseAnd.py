from manim import *

from _utils.WaitingScene import WaitingScene


def generate_bit_num(*bits):
    bitNum = VGroup()
    for bit in bits:
        bitNum.add(Integer(bit))
    return bitNum


class BitAnd(WaitingScene):
    def construct(self):
        length = 4
        num0 = generate_bit_num(0, 1, 1, 0)
        num1 = generate_bit_num(1, 0, 1, 0)
        num2 = generate_bit_num(1, 0, 0, 0)
        VGroup(*num0, *num1, *num2).arrange_in_grid(3, length).scale(4)
        self.add(num0, num1, Underline(num1))
        self.play(num0[0].copy().animate.move_to(num0[1]),
                  num0[1].copy().animate.move_to(num0[2]),
                  num0[2].copy().animate.move_to(num0[3]),
                  FadeIn(Integer(0).move_to(num0[0]).scale(4), shift=RIGHT),
                  FadeOut(num0[3], shift=RIGHT))
        self.wait()
