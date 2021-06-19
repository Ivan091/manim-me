from manim import *


class WaitingScene(Scene):
    def __init__(self):
        Scene.__init__(self)

    def play_wait(self, *args, wait_time: float = 0.1, **kwargs):
        super().play(*args, **kwargs)
        self.wait(wait_time)

    def get_all_vmobjects(self) -> []:
        vMObjects = []
        for item in self.mobjects:
            if isinstance(item, VMobject):
                vMObjects.append(item)
        return vMObjects
