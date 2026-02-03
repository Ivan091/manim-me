from itertools import cycle

from manim import Rectangle, Mobject, PI, RED, YELLOW, ORANGE, GREEN, BLUE, PURPLE
from numpy import cos, sin

from _utils.WaitingScene import WaitingScene


class DVDScene(WaitingScene):
    def construct(self):
        direction = PI / 4
        speed = 3
        colors = cycle([RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE])
        main_frame = Rectangle(height=8, width=14.2222)
        r = Rectangle(height=1, width=2, fill_opacity=1)

        def updater(m: Mobject, dt: float):
            nonlocal direction

            if m.get_right()[0] > main_frame.get_right()[0]:
                direction = PI - direction
                m.set_color(next(colors))
            elif m.get_left()[0] < main_frame.get_left()[0]:
                direction = PI - direction
                m.set_color(next(colors))
            elif m.get_top()[1] > main_frame.get_top()[1]:
                direction = -direction
                m.set_color(next(colors))
            elif m.get_bottom()[1] < main_frame.get_bottom()[1]:
                direction = -direction
                m.set_color(next(colors))

            m.shift((dt * speed * cos(direction), dt * speed * sin(direction), 0))

        self.add(r, main_frame)
        r.add_updater(updater)

        for _ in range(600):
            self.wait(1)
