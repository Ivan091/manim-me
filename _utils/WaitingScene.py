from manim import *


class WaitingScene(Scene):
    def __init__(self, wait_time: float = 0.5, **kwargs):
        super().__init__(**kwargs)
        self.wait_time = wait_time

    def play(self, *args, **kwargs):
        super().play(*args, **kwargs)
        super().play(Wait(run_time=self.wait_time))

    def get_all_vmobjects(self) -> []:
        vMObjects = []
        for item in self.mobjects:
            if isinstance(item, VMobject):
                vMObjects.append(item)
        return vMObjects
