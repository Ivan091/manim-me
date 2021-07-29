from manim import *

colors = [
    RED,
    ORANGE,
    YELLOW,
    GREEN,
    BLUE,
    BLUE_E,
    PURPLE
]


def create_nested_squares(count: int) -> VGroup:
    squares = VGroup()
    prevSize = 1
    for j in range(count):
        curSize = prevSize / 2 * (2 ** 0.5)
        squares.add(Square(curSize).rotate(PI / 4 * j).move_to(ORIGIN))
        prevSize = curSize
    return squares


class SquareInSquare(Scene):
    def construct(self):
        squares = create_nested_squares(50).add_updater(lambda m, dt: m.rotate(0.02).scale(1.03) if dt != 0 else m)

        self.play(
            Succession(
                FadeIn(squares),
                ApplyMethod(squares.set_color, colors[0]),
                ApplyMethod(squares.set_color, colors[1]),
                ApplyMethod(squares.set_color, colors[2]),
                ApplyMethod(squares.set_color, colors[3]),
                ApplyMethod(squares.set_color, colors[4]),
                ApplyMethod(squares.set_color, colors[5]),
                ApplyMethod(squares.set_color, colors[6]),
                Unwrite(squares)
            )
        )
        self.wait(1)
