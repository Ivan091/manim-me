from dataclasses import dataclass
from typing import Callable, Any, Sequence, Final

from manim import *
from manim.typing import Point3D, Vector3D


@dataclass(slots=True)
class Point:
    position: Point3D
    radius: float
    velocity: Vector3D


import numpy as np
from abc import ABC, abstractmethod


class Boundary(ABC):
    _GRAD_EPS: float = 1e-6

    @abstractmethod
    def sdf(self, p: np.ndarray) -> float:
        """Signed distance from 2D point p to the boundary. <0 inside, >0 outside."""

    def normal(self, p: np.ndarray) -> np.ndarray:
        """Outward unit normal. Default: numerical gradient of the sdf."""
        x, y = p
        eps = self._GRAD_EPS
        g = np.array(
            [
                self.sdf(np.array([x + eps, y])) - self.sdf(np.array([x - eps, y])),
                self.sdf(np.array([x, y + eps])) - self.sdf(np.array([x, y - eps])),
            ]
        )
        n = np.linalg.norm(g)
        return g / n if n > 0 else np.array([1.0, 0.0])

    def to_mobject(self, **kwargs) -> VMobject:
        raise NotImplementedError(f"{type(self).__name__} has no mobject")


class RectBoundary(Boundary):
    def __init__(self, left, right, bottom, top):
        self.c = np.array([(left + right) / 2, (bottom + top) / 2])
        self.h = np.array([(right - left) / 2, (top - bottom) / 2])

    def sdf(self, p: np.ndarray) -> float:
        q = np.abs(p - self.c) - self.h
        outside = np.linalg.norm(np.maximum(q, 0.0))
        inside = np.minimum(q.max(), 0.0)
        return float(outside + inside)

    def to_mobject(self, **kwargs):
        kwargs.setdefault("color", WHITE)
        return Rectangle(
            width=2 * self.h[0], height=2 * self.h[1], **kwargs
        ).move_to(np.append(self.c, 0.0))


class CircleBoundary(Boundary):
    def __init__(self, center, radius):
        self.c = np.asarray(center, dtype=float)[:2]
        self.R = radius

    def sdf(self, p):
        return np.linalg.norm(p - self.c) - self.R

    def normal(self, p, eps: float = 1e-6):
        d = p - self.c
        n = np.linalg.norm(d)
        return d / n if n > 0 else np.array([1.0, 0.0])

    def to_mobject(self, **kwargs):
        kwargs.setdefault("color", WHITE)
        return Circle(radius=self.R, **kwargs).move_to(np.append(self.c, 0.0))


class EllipseBoundary(Boundary):
    def __init__(self, center, a, b):
        self.c = np.asarray(center, dtype=float)[:2]
        self.r = np.array([a, b], dtype=float)

    @property
    def foci(self) -> tuple[np.ndarray, np.ndarray]:
        """Foci as 3D points, ordered (left, right) for a horizontal ellipse
        and (bottom, top) for a vertical one."""
        a, b = self.r
        cx, cy = self.c
        if a >= b:
            c = np.sqrt(a ** 2 - b ** 2)
            return np.array([cx - c, cy, 0.0]), np.array([cx + c, cy, 0.0])
        c = np.sqrt(b ** 2 - a ** 2)
        return np.array([cx, cy - c, 0.0]), np.array([cx, cy + c, 0.0])

    def sdf(self, p):
        # first-order approximation, accurate near the wall, which is where collisions happen
        q = p - self.c
        k0 = np.linalg.norm(q / self.r)
        k1 = np.linalg.norm(q / self.r ** 2)
        return k0 * (k0 - 1) / k1 if k1 > 0 else -self.r.min()

    def normal(self, p):
        g = (p - self.c) / self.r ** 2
        n = np.linalg.norm(g)
        return g / n if n > 0 else np.array([1.0, 0.0])

    def to_mobject(self, **kwargs):
        kwargs.setdefault("color", WHITE)
        return Ellipse(width=2 * self.r[0], height=2 * self.r[1], **kwargs).move_to(np.append(self.c, 0))


class StadiumBoundary(Boundary):
    """Capsule: a horizontal segment of half-length `h`, inflated by radius `r`."""

    def __init__(self, center, h, r):
        self.c = np.asarray(center, dtype=float)[:2]
        self.h, self.r = h, r

    def sdf(self, p):
        q = p - self.c
        q[0] -= np.clip(q[0], -self.h, self.h)
        return np.linalg.norm(q) - self.r

    def to_mobject(self, **kwargs):
        kwargs.setdefault("color", WHITE)
        return RoundedRectangle(
            width=2 * (self.h + self.r), height=2 * self.r, corner_radius=self.r, **kwargs
        ).move_to(np.append(self.c, 0))


class RingBoundary(Boundary):
    """Region between two concentric circles: the inner disc is an obstacle."""

    def __init__(self, center, r_inner, r_outer):
        self.c = np.asarray(center, dtype=float)[:2]
        self.ri, self.ro = r_inner, r_outer

    def sdf(self, p):
        d = np.linalg.norm(p - self.c)
        return max(d - self.ro, self.ri - d)

    def to_mobject(self, **kwargs):
        kwargs.setdefault("color", WHITE)
        c = np.append(self.c, 0)
        return VGroup(
            Circle(radius=self.ro, **kwargs).move_to(c),
            Circle(radius=self.ri, **kwargs).move_to(c),
        )


def regular_polygon(n, radius, rotation=0.0):
    a = rotation + np.linspace(0, TAU, n, endpoint=False)
    return [(radius * np.cos(t), radius * np.sin(t)) for t in a]


def star(n, outer, inner, rotation=PI / 2):
    a = rotation + np.linspace(0, TAU, 2 * n, endpoint=False)
    r = np.where(np.arange(2 * n) % 2 == 0, outer, inner)
    return [(ri * np.cos(t), ri * np.sin(t)) for ri, t in zip(r, a)]


def cross(arm_half_width, arm_length):
    w, L = arm_half_width, arm_length
    return [
        (w, L), (-w, L), (-w, w), (-L, w), (-L, -w), (-w, -w),
        (-w, -L), (w, -L), (w, -w), (L, -w), (L, w), (w, w)
    ]


class PolygonBoundary(Boundary):
    """Any simple polygon, convex or not. verts: (N, 2) in order."""

    def __init__(self, verts):
        self.a = np.asarray(verts, dtype=float)[:, :2]
        self.b = np.roll(self.a, -1, axis=0)
        self.ab = self.b - self.a

    def sdf(self, p):
        a, b, ab = self.a, self.b, self.ab
        ap = p - a
        t = np.clip((ap * ab).sum(1) / (ab * ab).sum(1), 0, 1)
        d = np.linalg.norm(ap - t[:, None] * ab, axis=1).min()

        # ray-casting inside test
        x, y = p
        crosses = (a[:, 1] > y) != (b[:, 1] > y)
        dy = np.where(ab[:, 1] == 0, 1, ab[:, 1])
        x_int = a[:, 0] + (y - a[:, 1]) * ab[:, 0] / dy
        inside = np.count_nonzero(crosses & (x < x_int)) % 2 == 1
        return -d if inside else d

    def to_mobject(self, **kwargs):
        kwargs.setdefault("color", WHITE)
        pts = [np.array([x, y, 0.0]) for x, y in self.a]
        return Polygon(*pts, **kwargs)


@dataclass(slots=True)
class World:
    points: list[Point]
    boundary: Boundary
    wall_radius: float = 0.0  # 0 = ideal point reflection; Point.radius is draw-only
    max_bounces: int = 8

    def _impact_time(self, pos, vel, rem: float) -> float:
        lo, hi = 0.0, rem  # lo: inside, hi: outside
        for _ in range(40):
            mid = 0.5 * (lo + hi)
            if self.boundary.sdf((pos + vel * mid)[:2]) + self.wall_radius > 0:
                hi = mid
            else:
                lo = mid
        return lo

    def step(self, dt: float):
        b, wr = self.boundary, self.wall_radius
        for p in self.points:
            pos, vel = p.position, p.velocity
            rem = dt
            for _ in range(self.max_bounces):
                end = pos + vel * rem
                if b.sdf(end[:2]) + wr <= 0:  # common case: one sdf call, no collision
                    pos, rem = end, 0.0
                    break
                t = self._impact_time(pos, vel, rem)
                pos = pos + vel * t
                n = b.normal(pos[:2])
                vn = vel[:2] @ n
                if vn > 0:  # only reflect if moving outward
                    vel[:2] -= 2 * vn * n
                rem -= t
            else:
                pos = pos + vel * rem  # bounce budget spent (tight corner)
            p.position = pos


def draw_dots(points: list[Point], dots_static_pool: list[Dot]) -> Callable[[Mobject], Any]:
    def update(_: Mobject):
        for i, d in enumerate(dots_static_pool):
            d.move_to(points[i].position)

    return update


POINT_PALETTE: Final[tuple[ManimColor, ...]] = (
    BLUE, ORANGE, GREEN, PINK, YELLOW, PURPLE, RED, TEAL,
)


class BoundaryScene(Scene):
    boundary: Boundary
    points_origin: Vector3D = ORIGIN
    points_speed: float = 1.3
    points_radius: float = 0.017
    simulation_time: int = 15
    points_count: int = 5760
    fractions: Sequence[float] = ()
    colors_start_angle: float = 0.0

    def point_colors(self) -> list[ManimColor]:
        if not self.fractions:
            return [POINT_PALETTE[0]] * self.points_count
        if len(self.fractions) > len(POINT_PALETTE):
            raise ValueError(f"at most {len(POINT_PALETTE)} fractions, got {len(self.fractions)}")

        weights = np.asarray(self.fractions, dtype=float)
        edges = np.round(np.cumsum(weights) / weights.sum() * self.points_count).astype(int)
        idx = np.searchsorted(edges, np.arange(self.points_count), side="right")

        # rotate the whole color layout: point i has angle i * TAU / points_count
        shift = int(round(self.colors_start_angle / TAU * self.points_count))
        idx = np.roll(idx, shift)
        return [POINT_PALETTE[i] for i in idx]

    def velocity(self, angle: float) -> Vector3D:
        return np.array([np.cos(angle) * self.points_speed, np.sin(angle) * self.points_speed, 0.0], dtype=float)

    def construct(self) -> None:
        angles = np.linspace(0, TAU, self.points_count, endpoint=False)
        points = [Point(self.points_origin, self.points_radius, self.velocity(angle)) for angle in angles]

        world = World(points, self.boundary)
        world_updater = lambda _, dt: world.step(dt)
        world_group = VGroup(self.boundary.to_mobject()).add_updater(world_updater)

        dots = [
            Dot(p.position, radius=p.radius, color=c)
            for p, c in zip(points, self.point_colors())
        ]
        dots_group = VGroup(*dots).add_updater(draw_dots(points, dots))

        self.add(world_group)
        self.add_foreground_mobjects(dots_group)
        self.wait(self.simulation_time)


class CircleLight(BoundaryScene):
    boundary = CircleBoundary((0, 0), 2.0)
    points_origin = UP * (2 / 3)  # same 1/3-of-radius offset as before
    fractions = [1, 1]
    colors_start_angle = PI / 2


class HexagonLight(BoundaryScene):
    boundary = PolygonBoundary(regular_polygon(6, 2.0))  # vertices on the x-axis, so half-width = R
    fractions = [1, 1, 1, 1, 1, 1]


class StarLight(BoundaryScene):
    # widest tips at ±outer·cos(18°) ≈ ±0.951·outer, so outer = 2.1 gives ±2.0
    boundary = PolygonBoundary(star(5, 2.1, 0.92))
    fractions = [1, 1, 1, 1, 1]
    colors_start_angle = PI / 2 - TAU / 10 - TAU / 5


class CrossLight(BoundaryScene):
    boundary = PolygonBoundary(cross(0.53, 2.0))
    fractions = [1, 1, 1, 1]
    colors_start_angle = -PI / 4


class EllipseLight(BoundaryScene):
    boundary = EllipseBoundary((0, 0), 2.0, 3.0)  # your original size already fits: 4.0 wide, 6.0 tall
    points_origin = boundary.foci[0]  # bottom focus, (0, -2.236)
    fractions = [1]


class StadiumLight(BoundaryScene):
    boundary = StadiumBoundary((0, 0), 1.15, 0.85)  # width 2·(1.15 + 0.85) = 4.0
    fractions = [1, 3]
    colors_start_angle = -PI / 4


class RingLight(BoundaryScene):
    boundary = RingBoundary((0, 0), 0.67, 2.0)
    points_origin = RIGHT * 1.33  # mid-band, as before
    fractions = [1]


del BoundaryScene
