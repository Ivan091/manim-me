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
        num0 = generate_bit_num(1, 1, 0, 0)
        num1 = generate_bit_num(1, 0, 1, 0)
        num2 = generate_bit_num(1, 0, 0, 0)
        VGroup(*num0, *num1, *num2).arrange_in_grid(3, length).scale_to_fit_height(5)
        self.add(num0, num1, Underline(num1))

        pair = VGroup(num0[0], num1[0])
        rect = SurroundingRectangle(pair)
        self.play(Write(rect))
        for j in range(length - 1):
            self.play(TransformFromCopy(pair, num2[j]))
            pair = VGroup(num0[j + 1], num1[j + 1])
            self.play(rect.animate.become(SurroundingRectangle(pair)))
        self.play(TransformFromCopy(pair, num2[length - 1]))
        self.play(Unwrite(rect))
