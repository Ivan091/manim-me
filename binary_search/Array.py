from manim import *

sys.path.append("../")
from utils.WaitingScene import WaitingScene


def init_array() -> VGroup:
    array = VGroup()
    for i in range(10):
        square = Square(1)
        square.add(Text(f"{i}"))
        array.add(square)
    array.arrange(RIGHT, 0.03)
    return array


def init_pointers(array: VGroup, size: int) -> VDict:
    pointers = VDict()

    left = Vector(UP * size).next_to(array[0], DOWN)
    left.add(Text("l").next_to(left, buff=SMALL_BUFF))
    pointers["l"] = left

    right = Vector(UP * size).next_to(array[-1], DOWN)
    right.add(Text("r").next_to(right, buff=SMALL_BUFF))
    pointers["r"] = right

    middle = Vector(DOWN * size).next_to(array[5], UP)
    middle.add(Text("m").next_to(middle, buff=SMALL_BUFF))
    pointers["m"] = middle

    return pointers


def shift_x(source: VMobject, destination: VMobject) -> list:
    return destination.get_center() - source.get_center()


class Array(WaitingScene):
    def __init__(self):
        super().__init__()
        self.array = init_array()
        self.pointers = init_pointers(self.array, 2)

    def construct(self):
        self.play_wait(Write(self.array))
        self.play_wait(Write(self.pointers))
        self.play_wait(self.pointers["l"].animate.shift(shift_x(self.array[0], self.array[1])))
