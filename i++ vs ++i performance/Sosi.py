import sys

sys.path.append("../")

from utils.WaitingScene import *


class Test(WaitingScene):
    def construct(self):
        tr = ValueTracker(0.5)
        sq = Square(4)
        self.add(sq)
        self.add(Circle(3).add_updater(lambda x: x.scale_to_fit_height(tr.get_value())).update())
        self.play(tr.animate(run_time=4).set_value(4), Rotate(sq, angle=np.array(TAU*10), run_time=4))

