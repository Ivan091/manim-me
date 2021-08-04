from typing import Sequence, Tuple

from manim import *


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


class Ball(Circle):
    def __init__(self, speed: np.ndarray, **kwargs):
        self.speed = speed
        super().__init__(**kwargs)

    def move(self):
        self.shift(self.speed)


class BounceSimulation(VGroup):
    def __init__(
            self,
            balls: Sequence[Ball],
            walls: Sequence[ParametricFunction],
            gravity_constant: float = 0.002,
            speed: float = 0.1,
            ball_buff: float = 1.2,
            **kwargs
    ):
        for item in balls:
            item.speed *= speed
        self.balls = balls
        self.walls = walls
        self.gravity_constant = gravity_constant
        self.ball_buff = ball_buff
        super().__init__(*balls, *walls, **kwargs)

    def ball_updater(self, ball: Ball):
        point, distance = find_closest_point(ball.get_center(), self.walls)
        if distance <= ball.radius * self.ball_buff:
            norm = ball.get_center() - point
            norm = norm / np.linalg.norm(norm)
            ball.speed = ball.speed - 2 * np.dot(ball.speed, norm) * norm
        else:
            ball.speed += DOWN * self.gravity_constant
        ball.move()

    def simulate(self):
        for b in self.balls:
            b.add_updater(lambda m: self.ball_updater(m))


class Bouncing(Scene):

    def func(self, t):
        return [t, 0, 0]

    def construct(self):
        balls = [
            Ball(ORIGIN, radius=0.3).move_to(RIGHT),
            Ball(ORIGIN, radius=0.3).move_to(RIGHT),
            Ball(ORIGIN, radius=0.3).move_to(RIGHT),
        ]
        walls = [ParametricFunction(self.func, t_range=[-2, 2], use_smoothing=False).scale(5).to_edge(DOWN)]

        sim = BounceSimulation(
            balls, walls
        )
        self.add(sim, DecimalNumber(num_decimal_places=5).add_updater(lambda m: m.set_value(balls[0].speed[1])))
        sim.simulate()
        self.wait(5)
