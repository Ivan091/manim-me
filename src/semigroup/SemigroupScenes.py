from manim import *

from _utils.MeineLiebeScene import MeineLiebeScene


class SquaredVMobject(VGroup):
    def __init__(self, square: Square, vmobject: VMobject):
        self.square = square
        self.vmobject = vmobject
        VGroup.__init__(self, square, vmobject)


class Intro(MeineLiebeScene):
    def construct(self):
        label = Text("Semigroup", font_size=100)

        self.play(Write(label))
        self.play(Transform(label, Text("?", font_size=100)))
        self.play(Transform(label, Text("Pattern", font_size=100)))
        self.play(Unwrite(label))


class Definition(MeineLiebeScene):
    def construct(self):
        label = Paragraph(
            "A type A is a semigroup if it provides an associative function",
            "that lets you combine any two values of type A into one.", alignment="center", line_spacing=1, font_size=30
        )
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

            self.play(
                TransformFromCopy(lb1, lb3.scale(1.2).move_to(expression[4])),
                TransformFromCopy(rb1, rb3.scale(1.2).next_to(rb1, RIGHT))
            )
            self.play(Unwrite(lb1), Unwrite(lb2), Unwrite(lb3), Unwrite(rb1), Unwrite(rb2), Unwrite(rb3))
            self.play(Unwrite(expression))

        self.play(
            (label[0][:5] + label[0][6:] + label[1][:36] + label[1][37:]).animate.set_color(BLUE),
        )
        self.play(label.animate.move_to(ORIGIN))

        if True:
            final_label = Paragraph(
                "If you have an associative operation over type A,",
                "you have a semigroup", alignment="center", line_spacing=1, font_size=30
            )

            final_label[0][39].set_color(GREEN)
            self.play(Transform(label, final_label))

        self.play(Unwrite(label))


class Example(MeineLiebeScene):
    def construct(self):

        semigroup_label = Tex("Semigroup[int, sum] = a + b")
        self.play(Write(semigroup_label))
        self.play(semigroup_label.animate.move_to(UP * 2))

        if True:
            numbers = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
            numbers_label = VGroup([Tex(str(num)) for num in numbers]).arrange(RIGHT, buff=MED_LARGE_BUFF)
            self.play(Write(numbers_label))

            acc = numbers[0]
            for i in range(1, len(numbers)):
                acc = acc + numbers[i]
                result_label_tmp = Tex(str(acc)).move_to(numbers_label[i]).set_color(BLUE)
                self.play(
                    ReplacementTransform(VGroup(numbers_label[i - 1], numbers_label[i]), result_label_tmp)
                )
                numbers_label[i] = result_label_tmp

            self.play(numbers_label[-1].animate.move_to(ORIGIN).set_font_size(100))
            self.play(Unwrite(numbers_label[-1]))

        self.play(Transform(semigroup_label, Tex("Semigroup[list, concat] = concat(a, b)").move_to(semigroup_label)))

        if True:
            lists = [[], [0, 1], [4, 9], [16, 25], [36, 49]]
            lists_labels = VGroup([Tex(f"[{", ".join(map(str, arr))}]") for arr in lists]).arrange(RIGHT, buff=MED_LARGE_BUFF)
            self.play(Write(lists_labels))
            acc = lists[0]
            acc_label = lists_labels[0].copy().move_to(DOWN).set_color(BLUE)
            self.play(TransformFromCopy(lists_labels[0], acc_label))
            for i in range(1, len(lists)):
                acc = acc + lists[i]
                circled_plus = MathTex("\\oplus").next_to(acc_label, DOWN)
                copy_to_add = lists_labels[i].copy().next_to(circled_plus, DOWN)
                acc_label_tmp = Tex(f"[{", ".join(map(str, acc))}]").move_to(DOWN).set_color(BLUE)
                self.play(
                    Write(circled_plus),
                    TransformFromCopy(lists_labels[i], copy_to_add)
                )
                self.play(
                    TransformMatchingShapes(VGroup(circled_plus, copy_to_add, acc_label), acc_label_tmp)
                )
                acc_label = acc_label_tmp

            self.play(Unwrite(lists_labels), Unwrite(acc_label))


class ExampleReduce(MeineLiebeScene):
    def construct(self):
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, LIGHT_GRAY, WHITE]

        squares_group = VGroup(
            [
                VGroup(
                    [Square(0.5) for _ in range(8)]
                ).arrange(RIGHT, buff=SMALL_BUFF).set_color(colors[i]) for i in range(8)
            ]
        ).arrange(DOWN, buff=SMALL_BUFF)

        self.play(Write(squares_group))

        self.play(
            Transform(
                squares_group,
                VGroup(
                    [gr.copy().arrange_in_grid(4, 2, buff=SMALL_BUFF) for gr in squares_group]
                ).arrange(RIGHT, MED_LARGE_BUFF).move_to(UP * 2),
                lag_ratio=0.1, run_time=6
            )
        )

        results = VGroup(
            [VGroup(Square(0.5), Integer(0, font_size=40)).set_color(colors[i]).next_to(squares_group[i], DOWN) for i in range(8)]
        )
        self.play(Write(results))

        for square_i in range(8):
            animations = []
            for group_i in range(8):
                anim = AnimationGroup(
                    ReplacementTransform(squares_group[group_i][square_i], results[group_i][0]),
                    Transform(results[group_i][1], results[group_i][1].copy().set_value(square_i + 1)),
                    run_time=0.5
                )
                animations.append(anim)
            self.play(AnimationGroup(animations, lag_ratio=0.1), wait_time=0)

        self.play(Transform(results, results.copy().arrange_in_grid(4, 2, buff=SMALL_BUFF)))
        self.play(results.animate.set_color(WHITE))

        final_result = VGroup(Square(1), Integer(0, font_size=40, edge_to_fix=ORIGIN)).next_to(results, DOWN)

        self.play(Write(final_result))

        for square_i in range(8):
            target = final_result[1].copy().set_value((square_i + 1) * 8)
            self.play(
                ReplacementTransform(results[square_i][0], final_result[0]),
                ReplacementTransform(VGroup(final_result[1], results[square_i][1]), target),
                run_time=0.5,
                wait_time=0
            )
            final_result[1] = target

        self.play(final_result.animate.move_to(ORIGIN).scale(2))
        self.play(Unwrite(final_result))


class ZipSum(MeineLiebeScene):
    def construct(self):
        label = MathTex("\\oplus(a, b) = a + b")

        lefts = VGroup([SquaredVMobject(Square(0.7), Integer(i, font_size=40)) for i in range(6)])
        pluses = VGroup([MathTex("\\oplus") for _ in range(6)])
        rights = VGroup([SquaredVMobject(Square(0.7), Integer(i * 10, font_size=40)) for i in range(6)])
        equals = VGroup([MathTex("=") for _ in range(6)])
        question_marks = VGroup([SquaredVMobject(Square(0.7), Tex("?")) for _ in range(6)])

        VGroup(
            label, VGroup(*lefts, *pluses, *rights, *equals, *question_marks).arrange_in_grid(
                6, 5, buff=MED_SMALL_BUFF, flow_order="dr"
            )
        ).arrange(DOWN, buff=MED_SMALL_BUFF)

        question_marks_sum = VGroup(
            [
                SquaredVMobject(
                    Square(0.7), Integer(left.vmobject.get_value() + right.vmobject.get_value(), font_size=40)
                ).move_to(qm)
                for left, right, qm in zip(lefts, rights, question_marks)
            ]
        )

        question_marks_product = VGroup(
            [
                SquaredVMobject(
                    Square(0.7), Integer(left.vmobject.get_value() * right.vmobject.get_value(), font_size=40)
                ).move_to(qm)
                for left, right, qm in zip(lefts, rights, question_marks)
            ]
        )

        self.play(Write(VGroup(label, *lefts, *pluses, *rights, *equals, *question_marks)), run_time=4)

        question_marks.save_state()
        self.play(
            AnimationGroup(
                [
                    ReplacementTransform(VGroup(qm, VGroup(left.copy(), right.copy())), qm_sum)
                    for left, right, qm, qm_sum in zip(lefts, rights, question_marks, question_marks_sum)
                ],
                lag_ratio=0.1
            )
        )
        question_marks.restore()

        self.play(
            AnimationGroup(
                label.animate.become(MathTex("\\oplus(a, b) = a * b"), match_center=True),
                *[
                    ReplacementTransform(qm_sum, qm)
                    for qm, qm_sum in zip(question_marks, question_marks_sum)
                ],
                lag_ratio=0.1
            )
        )

        question_marks.save_state()
        self.play(
            AnimationGroup(
                [
                    ReplacementTransform(VGroup(qm, VGroup(left.copy(), right.copy())), qm_product)
                    for left, right, qm, qm_product in zip(lefts, rights, question_marks, question_marks_product)
                ],
                lag_ratio=0.1
            )
        )
        question_marks.restore()

        self.play(
            Unwrite(VGroup(label, *lefts, *pluses, *rights, *equals, *question_marks_product))
        )


class MapRow(VGroup):
    def __init__(self, key: str, value: VMobject):
        self.key = key
        self.value = value
        super().__init__([MathTex(key), MathTex("\\Rightarrow"), value])
        self.arrange(RIGHT)


class Map(VGroup):
    def __init__(self, *rows: MapRow):
        self.rows = rows
        super().__init__(*rows)
        self.arrange(DOWN, aligned_edge=LEFT)


class MapMerge(MeineLiebeScene):

    def construct(self) -> None:
        Circle.set_default(stroke_width = 3, radius = 0.4)
        RegularPolygram.set_default(radius = 0.4, density = 1, stroke_width = 3)
        MathTex.set_default(font_size = 60)

        WHITE_BLUE = interpolate_color(WHITE, BLUE, 0.5)
        WHITE_ORANGE = interpolate_color(WHITE, ORANGE, 0.5)

        map_l = Map(
            MapRow("a", RegularPolygram(3, color=WHITE)),
            MapRow("b", RegularPolygram(4, color=WHITE)),
            MapRow("c", RegularPolygram(5, color=WHITE))
        )

        map_r = Map(
            MapRow("b", RegularPolygram(3, density=2, color=BLUE)),
            MapRow("c", RegularPolygram(4, density=2, color=ORANGE)),
            MapRow("d", RegularPolygram(5, density=2, color=BLUE))
        )

        map_m = Map(
            MapRow("a", RegularPolygram(3, color=WHITE)),
            MapRow("b", VGroup(RegularPolygram(4, color=WHITE_BLUE), RegularPolygram(3, density=2, color=WHITE_BLUE))),
            MapRow("c", VGroup(RegularPolygram(5, color=WHITE_ORANGE), RegularPolygram(4, density=2, color=WHITE_ORANGE))),
            MapRow("d", RegularPolygram(5, density=2, color=BLUE))
        )


        VGroup(map_l, map_m, map_r).arrange(RIGHT, buff=LARGE_BUFF)

        self.next_section("Write")

        plus = VGroup(
            Circle(color=BLUE),
            MathTex("\\oplus"),
            RegularPolygram(4, color=ORANGE),
            MathTex("="),
            VGroup(Circle(), RegularPolygram(4)).set_color(WHITE_ORANGE)
        ).arrange(RIGHT).shift(UP * 3)

        self.play(Write(VGroup(map_l, plus, map_r)))

        self.next_section("Merge")

        self.play(
            ReplacementTransform(map_l[0].copy(), map_m[0])
        )

        self.play(
            ReplacementTransform(map_l[1].copy(), map_m[1]),
            ReplacementTransform(map_r[0].copy(), map_m[1])
        )

        self.play(
            ReplacementTransform(map_l[2].copy(), map_m[2]),
            ReplacementTransform(map_r[1].copy(), map_m[2])
        )

        self.play(
            ReplacementTransform(map_r[2].copy(), map_m[3])
        )

        self.next_section("Unwrite")

        self.play(Unwrite(VGroup(map_l, map_r, plus, map_m)))

        self.save_section_frame()

class ThumbnailScene(Scene):
    def construct(self):
        Circle.set_default(stroke_width = 10, radius = 0.4)
        RegularPolygram.set_default(radius = 0.4, density = 1, stroke_width = 10)
        MathTex.set_default(font_size = 60)

        plus = VGroup(
            Circle(color=BLUE),
            MathTex("\\oplus"),
            RegularPolygram(4, color=ORANGE),
            MathTex("="),
            MathTex("?")
        ).arrange(RIGHT).scale(2.5)

        self.add(plus)
