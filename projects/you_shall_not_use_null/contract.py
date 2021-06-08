import sys

sys.path.append("../../")
from projects.utils.WaitingScene import *


class Contract(WaitingScene):
    def construct(self):
        typeText = Text("Type").move_to([-2.7, 1.5, 0])
        contract = SVGMobject("svg/contract.svg").set_color(WHITE).move_to([2.5, 1.5, 0]).scale(0.5)
        self.play_wait(Write(typeText))
        self.play_wait(Transform(typeText.copy(), contract))

        fieldsTx = Text("fields").set_color(ORANGE)
        methodsTx = Text("methods").set_color(ORANGE).move_to(fieldsTx.get_center() + DOWN).align_to(fieldsTx, LEFT)
        fieldsAndMethodsTx = VGroup(fieldsTx, methodsTx).scale(0.7)
        brace = Brace(fieldsAndMethodsTx, LEFT)
        VGroup(brace, fieldsAndMethodsTx).next_to(contract, RIGHT)
        self.play_wait(FadeIn(brace, shift=RIGHT))
        self.play_wait(Write(fieldsAndMethodsTx))
        self.play_wait(GrowArrow(Arrow(typeText, contract.get_edge_center(LEFT)).set_color(BLUE)))

        objectItem = Text("Object").set_color(ORANGE).move_to([0, -1.5, 0]).scale(0.9)
        angel = SVGMobject("svg/angel.svg").set_color(WHITE).move_to(objectItem)
        angel[1].set_color(YELLOW_D)

        self.play_wait(Write(objectItem))

        arrows_to_obj = VGroup(
            Arrow(objectItem, typeText).set_color(BLUE),
            Arrow(objectItem, contract).set_color(BLUE)
        )

        self.play_wait(GrowArrow(arrows_to_obj[0]))
        self.play_wait(GrowArrow(arrows_to_obj[1]))

        demon = SVGMobject("svg/demon3.svg").set_color(RED_D).move_to(objectItem.get_center() + DOWN * 0.7)
        self.play_wait(Transform(objectItem, Text("null").set_color(demon.get_color()).move_to(objectItem)))

        arrow_repaint = []
        for a in arrows_to_obj:
            arrow_repaint.append(ApplyMethod(a.set_color, demon.get_color(), run_time=3))
        arrow_repaint = AnimationGroup(*arrow_repaint)

        self.play_wait(
            LaggedStart(
                arrow_repaint,
                Transform(
                    objectItem, demon, lag_ratio=1
                ),
                lag_ratio=0.3
            )
        )

        self.play_wait(Write(Cross(contract)
                             .scale(1.5)
                             .move_to(contract.get_center_of_mass())
                             ))

        for a in arrows_to_obj:
            a.clear_updaters(recursive=True)
        npe = Text("NullPointerException").set_color(demon.get_color())
        self.play_wait(ReplacementTransform(VGroup(*self.get_all_vmobjects(), objectItem, *arrows_to_obj), npe))
        self.play_wait(FadeOut(npe))
