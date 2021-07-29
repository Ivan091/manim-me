import sys
sys.path.append("../")
from _utils.WaitingScene import *


def init_array() -> VGroup:
    array = VGroup()
    for i in range(15):
        square = Square(1)
        square.add(Text(f"{i}"))
        array.add(square)
    array.arrange(RIGHT, 0.03).shift(RIGHT * 3)
    return array


def init_pointers(array: VGroup, size: int) -> VDict:
    pointers = VDict()

    array[0][1].set_color(RED)
    middle = Vector(UP * size).next_to(array[0], DOWN)
    label = Text("null").add_updater(lambda mob: mob.next_to(middle, buff=SMALL_BUFF)).set_color(RED)
    pointers["null"] = VGroup(middle, label)

    return pointers


class NullInMemory(WaitingScene):
    def construct(self):
        array = init_array()
        pointers = init_pointers(array, 2)
        self.play_wait(Write(array, run_time=10), Write(pointers))
        brace = Brace(array[0:12], UP)
        self.play_wait(FadeIn(brace))
        braceLabel = Text("memory").add_updater(lambda mob: mob.next_to(brace, UP))
        self.play_wait(Write(braceLabel))
        self.play_wait(FadeOut(*self.get_all_vmobjects()))
