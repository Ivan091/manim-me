from manim import *

from _utils.MeineLiebeScene import MeineLiebeScene


class Day1(MeineLiebeScene):
    def construct(self):
        self.add(
            Text("Day 1", font_size=120).set_color(ORANGE)
        )

class Day2(MeineLiebeScene):
    def construct(self):
        self.add(
            Text("Day 2", font_size=120).set_color(ORANGE)
        )


class Day3(MeineLiebeScene):
    def construct(self):
        self.add(
            Text("Day 3", font_size=120).set_color(ORANGE)
        )

class Day4(MeineLiebeScene):
    def construct(self):
        self.add(
            Text("Day 4", font_size=120).set_color(ORANGE)
        )

class Day5(MeineLiebeScene):
    def construct(self):
        books_label = Text("Books done: 0 (for now)").move_to(DOWN * 3)
        books_label[10].set_color(RED)
        main_label = Text("Day 5", font_size=120).set_color(BLUE)
        self.add(
            main_label,
            books_label
        )

class Day6(MeineLiebeScene):
    def construct(self):
        books_label = Text("Books done: 0 (for now)").move_to(DOWN * 3)
        books_label[10].set_color(RED)
        main_label = Text("Day 6", font_size=120).set_color(BLUE)
        self.add(
            main_label,
            books_label
        )

class Day8(MeineLiebeScene):
    def construct(self):
        books_label = Text("Books done: 0 (for now)").move_to(DOWN * 3)
        books_label[10].set_color(RED)
        main_label = Text("Day 8", font_size=120).set_color(BLUE)
        self.add(
            main_label,
            books_label
        )

class Day11(MeineLiebeScene):
    def construct(self):
        books_label = Text("Books done: 0 (for now)").move_to(DOWN * 3)
        books_label[10].set_color(RED)
        main_label = Text("Day 11", font_size=120).set_color(BLUE)
        self.add(
            main_label,
            books_label
        )

class Day13(MeineLiebeScene):
    def construct(self):
        books_label = Text("Books done: 0 (for now)").move_to(DOWN * 3)
        books_label[10].set_color(RED)
        main_label = Text("Day 13", font_size=120).set_color(BLUE)
        self.add(
            main_label,
            books_label
        )

class Day16(MeineLiebeScene):
    def construct(self):
        books_label = Text("Books done: 0 (for now)").move_to(DOWN * 3)
        books_label[10].set_color(RED)
        main_label = Text("Day 16", font_size=120).set_color(BLUE)
        self.add(
            main_label,
            books_label
        )
