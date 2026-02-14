import numpy as np
from manim import *


class Intro(Scene):
    def construct(self):
        p = Paragraph("This video is not a tax advice.", "Never commit any tax fraud.")
        self.play(Write(p[0]))
        self.wait()
        self.play(Write(p[1]))
        self.wait()


class AProgrammerGuy(Scene):
    def construct(self):
        zl_line = Paragraph("1 zł ≈ 0.24 € ≈ 0.28 $", "median ≈ 7,000 zł ≈ 1,700 €", "programmers: 21,000 zł ≈ 5,700", line_spacing=1)
        question_mark = Paragraph("?").scale(3).set_color(ORANGE)
        three_median = Paragraph("3 median ≈ 21,000 zł")
        for line in zl_line:
            self.play(Write(line))
            self.wait()

        self.play(ReplacementTransform(zl_line, question_mark))
        self.wait()

        self.play(ReplacementTransform(question_mark, three_median))
        self.wait()


class TaxStructure(Scene):
    def construct(self):
        Text.set_default(font_size=36)

        social_tax_label = Text("Social tax:").set_color(ORANGE)
        social_value = Text("14% + 23% of the median").next_to(social_tax_label, RIGHT)
        social_group = VGroup(social_tax_label, social_value).arrange(RIGHT).move_to(ORIGIN)

        income_tax_label = Text("Income tax:").set_color(ORANGE)

        axes = Axes(
            x_range=[0, 2, -1],
            y_range=[0, 38, -1],
            x_length=4,
            y_length=2.5,
            tips=False
        )
        axes.get_x_axis().add_numbers([0.35, 1.43], font_size=30, num_decimal_places=2)
        axes.get_y_axis().add_numbers([12, 32], font_size=30)

        labels = axes.get_axis_labels(x_label=Tex("salary, medians", font_size=36), y_label=Tex("tax, \\%", font_size=36))

        coords = [(0, 0), (0.35, 0), (0.35, 12), (1.43, 12), (1.43, 32), (2, 32)]
        points = [axes.coords_to_point(x, y) for x, y in coords]
        graph = VMobject().set_points_as_corners(points).set_color(ORANGE)

        lineV = axes.get_vertical_line(axes.input_to_graph_point(1.43, graph)).set_color(BLUE)
        lineH1 = axes.get_horizontal_line(axes.input_to_graph_point(0.35 + 0.001, graph)).set_color(BLUE)
        lineH2 = axes.get_horizontal_line(axes.input_to_graph_point(1.43 + 0.001, graph)).set_color(BLUE)

        income_tax_plot_group = VGroup(axes, labels, graph, lineV, lineH1, lineH2)
        income_tax_group = VGroup(income_tax_label, income_tax_plot_group).arrange(RIGHT).move_to(ORIGIN)

        hidden_tax_label = Text("Hidden tax:").set_color(ORANGE)
        hidden_tax_value = Text("20%")
        hidden_tax_group = VGroup(hidden_tax_label, hidden_tax_value).arrange(RIGHT)

        VGroup(social_group, income_tax_group, hidden_tax_group).arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT).move_to(ORIGIN)

        self.play(Write(social_tax_label), Write(social_value))
        self.wait()
        self.play(Write(income_tax_label), Write(axes), Write(labels), run_time=3)
        self.play(Write(graph), Write(lineV), Write(lineH1), Write(lineH2), run_time=2)
        self.wait()
        self.play(Write(hidden_tax_label), Write(hidden_tax_value))
        self.wait()


class TaxSimulation(Scene):
    def construct(self):
        table_data = [
            ["Jan", 3, 1.95, "35%"],
            ["Feb", 3, 1.95, "35%"],
            ["Mar", 3, 1.70, "43%"],
            ["Apr", 3, 1.70, "43%"],
            ["May", 3, 1.70, "43%"],
            ["Jun", 3, 1.70, "43%"],
            ["Jul", 3, 1.70, "43%"],
            ["Aug", 3, 1.70, "43%"],
            ["Sep", 3, 1.32, "56%"],
            ["Oct", 3, 1.27, "57%"],
            ["Nov", 3, 1.27, "57%"],
            ["Dec", 3, 1.27, "57%"]
        ]

        chart = BarChart(
            values=list(map(lambda x: x[2], table_data)),
            bar_names=list(map(lambda x: x[0], table_data)),
            y_range=[0, 3, 0.25],
            x_length=8,
            y_length=5,
            bar_colors=[BLUE, GREEN, YELLOW, RED],
            axis_config={"font_size": 24},
        )
        c_bar_lbls = chart.get_bar_labels(font_size=24)
        chart_group = VGroup(chart, c_bar_lbls)
        total_tax_label = Text("Total tax = 56%", font_size=36).set_color(ORANGE)

        main_group = VGroup(total_tax_label, chart_group).arrange(DOWN, buff=MED_LARGE_BUFF).move_to(ORIGIN)

        self.play(Write(chart_group), run_time=2)
        self.wait()
        self.play(Write(total_tax_label))
        self.wait()


class B2BandB2BTaxes(Scene):
    def construct(self):
        Text.set_default(font_size=36)

        social_tax_label = Text("Social tax:").set_color(ORANGE)
        social_tax_value = Text("14% + 24% of the median").next_to(social_tax_label, RIGHT)
        social_tax_group = VGroup(social_tax_label, social_tax_value).arrange(RIGHT).move_to(ORIGIN)

        turnover_tax_label = Text("Turnover tax:").set_color(ORANGE)
        turnover_tax_value = Text("12%")
        turnover_tax_group = VGroup(turnover_tax_label, turnover_tax_value).arrange(RIGHT)

        VGroup(social_tax_group, turnover_tax_group).arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT).move_to(ORIGIN)

        self.play(Write(social_tax_label), Write(social_tax_value))
        self.wait()
        self.play(Write(turnover_tax_label), Write(turnover_tax_value))
        self.wait()


class B2BSimulation(Scene):
    def construct(self):
        table_data = [
            ["Jan", 2.40],
            ["Feb", 2.40],
            ["Mar", 2.40],
            ["Apr", 2.40],
            ["May", 2.40],
            ["Jun", 2.40],
            ["Jul", 2.40],
            ["Aug", 2.40],
            ["Sep", 2.40],
            ["Oct", 2.40],
            ["Nov", 2.40],
            ["Dec", 2.40]
        ]

        chart = BarChart(
            values=list(map(lambda x: x[1], table_data)),
            bar_names=list(map(lambda x: x[0], table_data)),
            y_range=[0, 3, 0.25],
            x_length=8,
            y_length=5,
            bar_colors=[BLUE, GREEN, YELLOW, RED],
            axis_config={"font_size": 24},
        )
        c_bar_lbls = chart.get_bar_labels(font_size=24)
        chart_group = VGroup(chart, c_bar_lbls)
        total_tax_label = Text("Total tax = 20%", font_size=36).set_color(ORANGE)

        main_group = VGroup(total_tax_label, chart_group).arrange(DOWN, buff=MED_LARGE_BUFF).move_to(ORIGIN)

        self.play(Write(chart_group), run_time=2)
        self.wait()
        self.play(Write(total_tax_label))
        self.wait()


class B2BvsEmployment(Scene):
    def construct(self):
        Text.set_default(font_size=36)

        data = [
            [1, "Jan", 1.95, 2.40],
            [2, "Feb", 1.95, 2.40],
            [3, "Mar", 1.70, 2.40],
            [4, "Apr", 1.70, 2.40],
            [5, "May", 1.70, 2.40],
            [6, "Jun", 1.70, 2.40],
            [7, "Jul", 1.70, 2.40],
            [8, "Aug", 1.70, 2.40],
            [9, "Sep", 1.32, 2.40],
            [10, "Oct", 1.27, 2.40],
            [11, "Nov", 1.27, 2.40],
            [12, "Dec", 1.27, 2.40]
        ]

        axes = Axes(
            x_range=[0, 12, 1],
            y_range=[1, 4, 0.25],
            x_length=8,
            y_length=5,
            tips=False
        )

        labels = axes.get_axis_labels(x_label=Tex("month", font_size=36), y_label=Tex("income", font_size=36))

        axes.get_x_axis().add_labels({row[0]: row[1] for row in data}, font_size=30)
        axes.get_y_axis().add_numbers([1, 1.5, 2, 2.5, 3, 3.5, 4])

        points_gross = [axes.coords_to_point(x, y) for (x, y) in [(1, 3), (12, 3)]]
        graph_baseline = VMobject().set_points_as_corners(points_gross)
        graph_baseline_legend = axes.get_graph_label(graph_baseline, label=Tex("gross", font_size=36), dot=True).arrange(LEFT, center=True)

        points_employment = [axes.coords_to_point(row[0], row[2]) for row in data]
        graph_employment = VMobject().set_points_as_corners(points_employment).set_color(ORANGE)
        graph_employment_legend = axes.get_graph_label(graph_employment, label=Tex("employment net", font_size=36), dot=True).set_color(
            ORANGE).arrange(LEFT, center=True)

        points_b2b = [axes.coords_to_point(row[0], row[3]) for row in data]
        graph_b2b = VMobject().set_points_as_corners(points_b2b).set_color(BLUE)
        graph_b2b_legend = axes.get_graph_label(graph_b2b, label=Tex("b2b net", font_size=36), dot=True).set_color(BLUE).arrange(LEFT,
                                                                                                                                 center=True)

        legend_group = VGroup(graph_baseline_legend, graph_b2b_legend, graph_employment_legend).arrange(DOWN, aligned_edge=LEFT).next_to(
            axes, RIGHT, buff=MED_LARGE_BUFF)

        main_group = VGroup(axes, labels, legend_group, graph_baseline, graph_employment, graph_b2b).move_to(ORIGIN)

        self.play(Write(main_group), run_time=7)
        self.wait()


class B2BDisadvantages(Scene):
    def construct(self):
        paragraph = Paragraph("Mobility", "Narrow market", "No paid vacation", "No sick paid leave", "No paid paternity leave",
                              "Access to healthcare", "Access to pension", line_spacing=1)
        for i in [1, 2, 3, 4]:
            paragraph[i].set_color(ORANGE)
        for i in [0, 5, 6]:
            paragraph[i].set_color(BLUE)

        self.play(Write(paragraph), run_time=10)

