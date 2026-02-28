from manim import *

from _utils.WaitingScene import WaitingScene


class Intro(WaitingScene):
    def construct(self):
        label = Text("Semigroup", font_size=100)

        self.play(Write(label))
        self.play(Transform(label, Text("?", font_size=100)))
        self.play(Transform(label, Text("Pattern", font_size=100)))
        self.play(Unwrite(label))


class Definition(WaitingScene):
    def construct(self):
        label = Paragraph("A type A is a semigroup if it provides an associative function",
                          "that lets you combine any two values of type A into one.", alignment="center", line_spacing=1, font_size=30)
        label[0][5].set_color(GREEN)
        label[1][36].set_color(GREEN)

        self.play(Write(label))
        self.play(label.animate.shift(2 * UP))
        self.play(
            label[0][43:].animate.set_color(ORANGE),
            (label[1][:36] + label[1][37:]).animate.set_color(ORANGE),
        )

        if True:
            code = Code(
                code_string="""
                    def combine(left: A, right: A) -> A:
                        pass # your implementation here :)""",
                language="python",
                background="rectangle",
                formatter_style="monokai",
                background_config={"fill_opacity": 0},
            )
            self.play(Write(code))
            combine_alternative = (
                MathTex("combine(left, right) \\iff left \\oplus right").next_to(code, DOWN, buff=LARGE_BUFF)
            )
            self.play(Write(combine_alternative))
            self.play(Unwrite(code), Unwrite(combine_alternative))

        self.play(
            label[0][43:].animate.set_color(BLUE),
            (label[1][:36] + label[1][37:]).animate.set_color(BLUE),
        )

        self.play(
            label[0][32:43].animate.set_color(ORANGE),
        )

        if True:
            expression = (
                VGroup(
                    MathTex("x").set_opacity(0),
                    MathTex("a"),
                    MathTex("x").set_opacity(0),
                    MathTex("\\oplus"),
                    MathTex("x").set_opacity(0),
                    MathTex("b"),  # 5
                    MathTex("x").set_opacity(0),
                    MathTex("\\oplus"),
                    MathTex("x").set_opacity(0),
                    MathTex("c"),
                    MathTex("x").set_opacity(0),
                    MathTex("\\oplus"),
                    MathTex("x").set_opacity(0),
                    MathTex("d"),
                    MathTex("x").set_opacity(0),
                    MathTex("\\oplus"),  # 15
                    MathTex("x").set_opacity(0),
                    MathTex("e"),
                    MathTex("x").set_opacity(0),
                ).arrange(RIGHT, buff=SMALL_BUFF)
            )

            lb1 = MathTex("\\left(").set_color(BLUE).move_to(expression[0])
            rb1 = MathTex("\\right)").set_color(BLUE).move_to(expression[-1])

            self.play(Write(expression))
            self.play(Write(lb1), Write(rb1))

            self.play(lb1.animate.move_to(expression[0]), rb1.animate.move_to(expression[6]))
            lb2 = lb1.copy().set_color(ORANGE)
            rb2 = rb1.copy().set_color(ORANGE)
            self.play(TransformFromCopy(lb1, lb2.move_to(expression[8])), TransformFromCopy(rb1, rb2.move_to(expression[14])))

            self.play(rb1.animate.move_to(expression[8]), lb2.animate.move_to(expression[12]), rb2.animate.move_to(expression[18]))
            self.play(lb1.animate.scale(1.1).move_to(expression[8]), rb1.animate.scale(1.1).next_to(rb2, RIGHT))

            lb3 = lb2.copy().set_color(GREEN)
            rb3 = rb2.copy().set_color(GREEN)

            self.play(TransformFromCopy(lb1, lb3.scale(1.2).move_to(expression[4])),
                      TransformFromCopy(rb1, rb3.scale(1.2).next_to(rb1, RIGHT)))
            self.play(Unwrite(lb1), Unwrite(lb2), Unwrite(lb3), Unwrite(rb1), Unwrite(rb2), Unwrite(rb3))
            self.play(Unwrite(expression))

        self.play(
            (label[0][:5] + label[0][6:] + label[1][:36] + label[1][37:]).animate.set_color(BLUE),
        )
        self.play(label.animate.move_to(ORIGIN))

        if True:
            final_label = Paragraph("If you have an associative operation over type A,",
                                    "you have a semigroup", alignment="center", line_spacing=1, font_size=30)

            final_label[0][39].set_color(GREEN)
            self.play(Transform(label, final_label))

        self.play(Unwrite(label))
