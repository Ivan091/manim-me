from manim import *


class Cardioid(Scene):
    def construct(self):
        main = Circle(radius=1)
        main_path = Circle(radius=1.33)
        second = Circle(radius=0.33).move_to(main_path.get_start())
        dot = Dot(second.get_start())
        self.add(main, second, dot, TracedPath(dot.get_center))
        move_circle = MoveAlongPath(
            second,
            main_path,
            run_time=4,
            rate_func=linear
        )
        move_dot = MoveAlongPath(
            dot,
            second,
            run_time=1,
            rate_func=linear,
        )
        self.play(
            move_circle,
            Succession(
                move_dot,
                move_dot,
                move_dot,
                move_dot,
            )
        )
        self.play(
            move_circle,
            Succession(
                move_dot,
                move_dot,
                move_dot,
                move_dot,
            )
        )
