from dataclasses import dataclass, field
from typing import Any, Callable

import numpy as np
from manim import Dot, ManimColor, Scene, VGroup, config

from light.boundaries import Boundary
from light.cannon import Cannon


@dataclass(slots=True)
class World:
    boundary: Boundary
    cannon: Cannon
    duration: float
    # 0 = ideal point reflection; dot radius is draw-only
    wall_radius: float = 0.0
    max_bounces: int = 8
    view_margin: float = 0.5
    pos: np.ndarray = field(init=False)  # (N, 2), updated in place
    vel: np.ndarray = field(init=False)  # (N, 2), updated in place
    colors: list[ManimColor] = field(init=False)
    alive: int = field(init=False, default=0)
    elapsed: float = field(init=False, default=0.0)

    def __post_init__(self):
        count = self.cannon.amount_for(self.duration)
        self.pos = self.cannon.positions(count)
        self.vel = self.cannon.velocities(count)
        self.colors = self.cannon.colors(count)
        self._fire()

    def step(self, dt: float) -> int:
        self.elapsed += dt
        before = self.alive
        self._fire()
        self._move(dt)
        return self.alive - before

    def to_mobject(self, dot_radius: float, scene: Scene) -> VGroup:
        dots = [
            Dot(np.append(self.pos[i], 0.0), radius=dot_radius, color=c, num_components=4)
            for i, c in enumerate(self.colors)
        ]
        dots_group = VGroup()
        draw = self._draw(dots, dots_group, dot_radius + self.view_margin)
        draw()
        dots_group.add_updater(lambda _: draw())
        view = VGroup(self.boundary.to_mobject(), dots_group)
        view.add_updater(lambda _, dt: self._tick(scene, dt))
        return view

    def _tick(self, scene: Scene, dt: float):
        start = self.alive
        fired = self.step(dt)
        self.cannon.sound.play(scene, start, fired, dt)

    def _draw(self, dots: list[Dot], group: VGroup, margin: float) -> Callable[[], Any]:
        p3 = np.zeros((len(dots), 3))
        half = np.array([config.frame_x_radius, config.frame_y_radius]) + margin
        visible = np.zeros(len(dots), dtype=bool)

        def draw():
            n = self.alive
            inside = np.zeros(len(dots), dtype=bool)
            inside[:n] = (np.abs(self.pos[:n]) <= half).all(axis=1)
            gone, arrived = visible & ~inside, inside & ~visible
            if gone.any():
                group.remove(*(dots[i] for i in np.flatnonzero(gone)))
            if arrived.any():
                group.add(*(dots[i] for i in np.flatnonzero(arrived)))
            visible[:] = inside
            p3[:n, :2] = self.pos[:n]
            for i in np.flatnonzero(inside):
                dots[i].move_to(p3[i])

        return draw

    def _fire(self):
        fired = min(self.cannon.fired(self.elapsed), len(self.pos))
        self.alive = max(self.alive, fired)

    def _move(self, dt: float):
        pos, vel = self.pos, self.vel
        b, wr = self.boundary, self.wall_radius
        rem = np.full(len(pos), dt)
        active = np.arange(self.alive)
        for _ in range(self.max_bounces):
            end = pos[active] + vel[active] * rem[active, None]
            out = b.sdf_many(end) + wr > 0
            pos[active[~out]] = end[~out]  # no collision: done for this frame
            active = active[out]
            if active.size == 0:
                break

            p0, v0, r0 = pos[active], vel[active], rem[active]
            # lo: inside, hi: outside
            lo, hi = np.zeros(len(active)), r0.copy()
            # bisect impact time, only for colliding points
            for _ in range(40):
                mid = 0.5 * (lo + hi)
                bad = b.sdf_many(p0 + v0 * mid[:, None]) + wr > 0
                hi = np.where(bad, mid, hi)
                lo = np.where(bad, lo, mid)

            pos[active] = p0 + v0 * lo[:, None]
            n = b.normal_many(pos[active])
            vn = np.einsum("ij,ij->i", v0, n)
            # reflect only if moving outward
            vel[active] = v0 - 2 * (vn * (vn > 0))[:, None] * n
            rem[active] = r0 - lo
        else:
            # bounce budget spent (tight corner)
            pos[active] += vel[active] * rem[active, None]
