import sys

sys.path.append("../")
from manim import *
from utils import WaitingScene


class SourceCode(VGroup):
    """
    [i] -> CodeLine i
    """

    def __init__(
            self,
            file: str,
            language: str,
            start: int = 0,
            end: int = None,
    ):
        VGroup.__init__(self)
        listing = Code(
            file,
            language=language,
            tab_width=4,
            font="Consolas",
            style="monokai",
            insert_line_nums=False,
        )
        if end is None:
            end = listing.code.__len__()
        start = max(start, 0)
        end = min(end, listing.code.__len__())

        for q in range(start, end):
            self.add(listing[2][q])

    def line(self, number: int) -> VGroup:
        """
        Gets line as VGroup by number. Numeration begins from 1.
        :param number: line number
        :return: line
        """
        return self[number - 1]

    def letter(self, line: int, row: int) -> VMobject:
        """
        Gets letter as VMobject. Numeration begins from 1.
        :param line: number of line of the letter
        :param row: number of row of the letter
        :return: letter
        """
        return self[line - 1][row - 1]


def make_code_scene(scene: WaitingScene, listing: SourceCode, label: Text):
    scene.play_wait(Write(label))
    scene.play_wait(label.animate.next_to(listing, UP))
    scene.play_wait(Write(listing))
    scene.play_wait(FadeOut(listing), FadeOut(label))
