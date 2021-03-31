from manim import *


class WaitingScene(Scene):
    def __init__(self):
        Scene.__init__(self)

    def play_wait(self, *args, wait_time: float = 0.5, **kwargs):
        super().play(*args, **kwargs)
        self.wait(wait_time)
