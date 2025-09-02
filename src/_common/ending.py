from manim import *
from _utils.WaitingScene import WaitingScene


class Ending(WaitingScene):
    def construct(self):
        azari = SVGMobject("assets/azari_colorful_old.svg").scale(3.5).set_color(WHITE)
        azari[1].set_color(BLUE)
        azari[10].set_color(ORANGE)
        azari[13].set_color(BLUE)

        self.play(Write(azari, run_time=10, rate_func=smooth))
        self.play(azari.animate.move_to(LEFT * 3))
        text = Tex("Cyber", "D", "as", "ei", "n").move_to(UP * 0.5 + RIGHT * 3)
        self.play(Write(text))

        def modify_text(tex: Tex):
            tex.scale(2)
            tex[1].set_color(BLUE)
            tex[4].set_color(ORANGE)
            return tex

        self.play1(ApplyFunction(modify_text, text))
        self.play1(
            Unwrite(text, run_time=4),
            Unwrite(azari, run_time=4)
        )
