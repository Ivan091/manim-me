from manim import *

from _utils.MeineLiebeScene import MeineLiebeScene


class GlowLine(MeineLiebeScene):
    def construct(self):
        tex = Tex("WaveWaveWaveWaveWave").scale(2)
        self.play(ApplyWave(
            tex,
            direction=RIGHT,
            time_width=0.5,
            amplitude=0.3
        ))
        self.play(ApplyWave(
            tex,
            rate_func=linear,
            ripples=4
        ))
