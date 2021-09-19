from typing import Iterable

from manim import *

line_config = {
    "stroke_width": 1
}


def is_square(n: int):
    square_root = n ** 0.5
    return square_root == int(square_root)


def build_matrix(rows: int, columns: int) -> Iterable[Iterable[VMobject]]:
    return [[Dot(fill_opacity=0) for _ in range(columns)] for _ in range(rows)]


def build_table_of_matrix(matrix: Iterable[Iterable[VMobject]]) -> MobjectTable:
    return MobjectTable(matrix, h_buff=0.2, v_buff=0.2, include_outer_lines=True, line_config=line_config)


def build_table(rows: int, columns: int) -> MobjectTable:
    return MobjectTable(build_matrix(rows, columns), h_buff=0.05, v_buff=0.05, include_outer_lines=True, line_config=line_config).to_corner(UL)


def add_all_squares(table: MobjectTable):
    n = 1
    for a in range(1, len(table.get_rows()) + 1):
        for b in range(1, len(table.get_columns()) + 1):
            if is_square(n):
                cell = table.get_cell([a, b], fill_color=BLUE, fill_opacity=0.5, stroke_opacity=0)
                table.add(cell)
            n += 1


class Squares(Scene):
    table = build_table(10, 10)

    def construct(self):
        add_all_squares(self.table)
        self.add(self.table)
        self.wait(0.5)
        for _ in range(20):
            self.expand(1, 0)
        for _ in range(50):
            self.expand(0, 1)

    def expand(self, d_height: int, d_width: int):
        new_table = build_table(len(self.table.get_rows()) + d_height, len(self.table.get_columns()) + d_width)
        add_all_squares(new_table)
        self.remove(self.table)
        self.add(new_table)
        self.table = new_table
        self.wait(0.1)
