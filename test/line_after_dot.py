from manim import *


class LineAfterDot(Scene):
    def construct(self):
        circ = Circle(color=RED).shift(4 * LEFT)
        dot = Dot(color=RED).move_to(circ.get_start())
        rolling_circle = VGroup(circ, dot)
        trace = TracedPath(circ.get_start)
        self.add(trace, rolling_circle)
        self.play(rolling_circle.animate.shift(8 * RIGHT), run_time=4, rate_func=linear)
        self.wait(1)
        trace.clear_updaters()
        self.play(trace.animate.shift(DOWN))
        self.play(trace.animate.shift(LEFT * 2))
        self.wait(1)


class Circles(Scene):
    def construct(self):
        vt_y = ValueTracker(0)
        c_y = Circle().to_edge(UP).rotate(PI)
        d_y = Dot().add_updater(lambda m: m.move_to(c_y.point_from_proportion(vt_y.get_value() % 1)))
        l_y = Line(ORIGIN, DOWN * 20).add_updater(lambda m: m.shift(d_y.get_center() - m.get_start())).update()
        y = VGroup(c_y, d_y, l_y)

        vt_x = ValueTracker(0)
        c_x = Circle().next_to(c_y, DOWN + LEFT).rotate(PI)
        d_x = Dot().add_updater(lambda m: m.move_to(c_x.point_from_proportion(vt_x.get_value() % 1)))
        l_x = Line(ORIGIN, RIGHT * 20).add_updater(lambda m: m.shift(d_x.get_center() - m.get_start())).update()
        x = VGroup(c_x, d_x, l_x)

        d = Dot().add_updater(lambda m: m.move_to(line_intersection(l_x.get_start_and_end(), l_y.get_start_and_end()))).update()
        trace = TracedPath(d.get_center, min_distance_to_new_point=0.0001).set_stroke(width=4)

        self.add(x, y, d, trace)
        self.play(
            ApplyMethod(
                vt_x.set_value, 1,
                rate_func=linear
            ),
            ApplyMethod(
                vt_y.set_value, 1,
                rate_func=linear
            ),
            run_time=10,
        )

        self.wait(1)

        trace.clear_updaters()
        self.play(trace.animate.shift(RIGHT * 2))
        self.wait(1)
