import sys

sys.path.append("../../")
from projects.utils.WaitingScene import WaitingScene
from manim import *


class Contract1(WaitingScene):
    def construct(self):
        azari = SVGMobject("assets/azari_colorful_old.svg").scale(3.5).set_color(WHITE)
        azari[1].set_color(BLUE)
        azari[10].set_color(ORANGE)
        azari[13].set_color(BLUE)

        self.play(Write(azari, run_time=2, rate_func=rush_into))
        self.play(azari.animate.move_to(LEFT * 3))
        text = Tex("Cyber", "D", "as", "ei", "n").move_to(UP * 0.5 + RIGHT * 3)
        self.play(Write(text))

        def modify_text(tex: Tex):
            tex.scale(2)
            tex[1].set_color(BLUE)
            tex[4].set_color(ORANGE)
            return tex

        self.play_wait(ApplyFunction(modify_text, text))
        self.play_wait(Write(text, rate_func=lambda t: smooth(1 - t), run_time=2),
                       Write(azari, rate_func=lambda t: smooth(1 - t), run_time=2))
