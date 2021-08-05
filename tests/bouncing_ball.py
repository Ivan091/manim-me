from typing import Sequence, Tuple

from manim import *

from _utils.WaitingScene import WaitingScene


def find_closest_point(point: np.ndarray, mobs: Sequence[Mobject]) -> Tuple[np.ndarray, float]:
    closestPoint = mobs[0].get_all_points()[0]
    curDist = np.linalg.norm(closestPoint - point)
    for mob in mobs:
        for p in mob.get_all_points():
            newDist = np.linalg.norm(p - point)
            if newDist < curDist:
                closestPoint = p
                curDist = newDist
    return closestPoint, curDist


colors = [
    RED,
    GREEN,
    BLUE,
    ORANGE,
    PURPLE,
    GOLD
]


class Ball(Circle):
    def __init__(self, speed: np.ndarray = ORIGIN, **kwargs):
        self.speed = np.copy(speed)
        super().__init__(**kwargs)


class BounceSimulation(VGroup):
    def __init__(
            self,
            balls: Sequence[Ball],
            walls: Sequence[ParametricFunction],
            scene: Scene,
            gravity_constant: float = 0.002,
            speed_multiplier: float = 0.1,
            ball_buff: float = 1.2,
            **kwargs
    ):
        for ball in balls:
            ball.speed *= speed_multiplier
        self.balls = balls
        self.walls = walls
        self.scene = scene
        self.gravity_constant = gravity_constant
        self.ball_buff = ball_buff
        super().__init__(*balls, *walls, **kwargs)

    def ball_updater(self, ball: Ball):
        point, distance = find_closest_point(ball.get_center(), self.walls)
        if distance <= ball.radius * self.ball_buff:
            norm = ball.get_center() - point
            norm = norm / np.linalg.norm(norm)
            ball.speed -= 2 * np.dot(ball.speed, norm) * norm
            self.scene.add_sound("assets/ball_hit1.wav", gain=-20)
            ball.shift(ball.speed * 1.2)
        else:
            ball.speed += DOWN * self.gravity_constant
            ball.shift(ball.speed)
        ball.speed *= 0.99999999

    def simulate(self):
        for b in self.balls:
            b.add_updater(lambda m, dt: self.ball_updater(m))


class Bouncing(WaitingScene):

    def func(self, t):
        return [t, t ** 2, 0]

    def construct(self):
        sim = BounceSimulation(
            [Ball(ORIGIN, radius=0.3, arc_center=UP * 2 + RIGHT * (j / 2.0 + 0.5), color=colors[j]) for j in range(6)],
            [ParametricFunction(self.func, t_range=[-2, 2], use_smoothing=False, stroke_width=4).scale(5).to_edge(DOWN)],
            self,
        )
        self.add(*sim.walls)
        self.play(Write(VGroup(*sim.balls)), Write(Tex("Parabola").to_edge(DL)))
        sim.simulate()
        self.wait(60)


class BouncingThumbnail(WaitingScene):

    def func(self, t):
        return [t, t ** 2, 0]

    def construct(self):
        self.add(ParametricFunction(self.func, t_range=[-2, 2], use_smoothing=False, stroke_width=4).scale(5).to_edge(DOWN),
                 Circle(2))
