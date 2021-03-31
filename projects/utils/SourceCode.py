import sys

sys.path.append("../../")
from manim import *
from abc import ABC
from projects.utils import WaitingScene


class SourceCode(VGroup, ABC):
    """
    Indexes of line and of char in code begin from 1

    [i] -> CodeLine i

    [i][0] -> Row number Paragraph

    [i][1] -> Line of code Paragraph
    """

    def __init__(
            self,
            file: str,
            language: str,
            start: int = 1,
            end: int = None,
    ):
        VGroup.__init__(self)
        listing = SourceCodeGenerator(
            file,
            language=language,
            tab_width=4,
            font="Consolas",
            style="monokai",
            insert_line_nums=True,
        )
        if end is None:
            end = listing.code.__len__()
        else:
            end -= 1
        start -= 1
        start = max(start, 0)
        end = min(end, listing.code.__len__())

        self.add(VMobject())
        for i in range(start, end):
            self.add(VGroup(listing[1][i], listing[2][i]))


class SourceCodeGenerator(Code, ABC):
    def __init__(
            self,
            file_name: str = None,
            language: str = None,
            line_num_from: int = 1,
            tab_width: int = 5,
            font: str = "Consolas",
            insert_line_nums: bool = True,
            style: str = "monokai",
            line_spacing: float = 0.5,
            **kwargs,
    ):
        Code.__init__(
            self,
            file_name=file_name,
            tab_width=tab_width,
            font=font,
            insert_line_no=insert_line_nums,
            line_no_from=line_num_from,
            style=style,
            language=language,
            line_spacing=line_spacing,
            **kwargs,
        )

    def gen_colored_lines(self):
        lines_text = []
        for line_no in range(0, self.code_json.__len__()):
            line_str = ""
            for word_index in range(self.code_json[line_no].__len__()):
                line_str = line_str + self.code_json[line_no][word_index][0]
            lines_text.append(" " + self.tab_spaces[line_no] * " " * self.tab_width + line_str)
        code = Paragraph(
            *[i for i in lines_text],
            line_spacing=self.line_spacing,
            font=self.font,
            disable_ligatures=True,
            stroke_width=self.stroke_width,
        ).scale(self.scale_factor)
        for line_no in range(code.__len__()):
            line = code.chars[line_no]
            line_char_index = self.tab_spaces[line_no] * self.tab_width + 1
            for word_index in range(self.code_json[line_no].__len__()):
                line[
                line_char_index: line_char_index
                                 + self.code_json[line_no][word_index][0].__len__()
                ].set_color(self.code_json[line_no][word_index][1])
                line_char_index += self.code_json[line_no][word_index][0].__len__()
        return code


def make_code_scene(scene: WaitingScene, listing: SourceCode, label: Text):
    scene.play_wait(Write(label))
    scene.play_wait(label.animate.next_to(listing, UP))
    scene.play_wait(Write(listing))
    scene.play_wait(FadeOut(listing), FadeOut(label))
