from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Final, Sequence

import numpy as np
from manim import (
    BLUE,
    GREEN,
    ORANGE,
    ORIGIN,
    PI,
    PINK,
    PURPLE,
    RED,
    RIGHT,
    TAU,
    TEAL,
    UP,
    WHITE,
    YELLOW,
    Circle,
    Dot,
    Ellipse,
    ManimColor,
    Mobject,
    Polygon,
    Rectangle,
    RoundedRectangle,
    Scene,
    VGroup,
    VMobject,
)
from manim.typing import Vector3D


class Boundary(ABC):
    _GRAD_EPS: float = 1e-6

    @abstractmethod
    def sdf_many(self, points: np.ndarray) -> np.ndarray:
        """Signed distance for an (N, 2) array of points -> (N,).

        <0 inside, >0 outside.
        """

    def normal_many(self, points: np.ndarray) -> np.ndarray:
        """Outward unit normals, (N, 2).

        Default: numerical gradient of the sdf.
        """
        e = self._GRAD_EPS
        ex, ey = np.array([e, 0.0]), np.array([0.0, e])
        g = np.stack(
            [
                self.sdf_many(points + ex) - self.sdf_many(points - ex),
                self.sdf_many(points + ey) - self.sdf_many(points - ey),
            ],
            axis=1,
        )
        norm = np.linalg.norm(g, axis=1, keepdims=True)
        return g / np.maximum(norm, 1e-12)

    def sdf(self, p: np.ndarray) -> float:
        point = np.asarray(p, dtype=float)[None, :2]
        return float(self.sdf_many(point)[0])

    def normal(self, p: np.ndarray) -> np.ndarray:
        point = np.asarray(p, dtype=float)[None, :2]
        return self.normal_many(point)[0]

    def to_mobject(self, **kwargs) -> VMobject:
        raise NotImplementedError(f"{type(self).__name__} has no mobject")


class RectBoundary(Boundary):
    def __init__(self, left, right, bottom, top):
        self.c = np.array([(left + right) / 2, (bottom + top) / 2])
        self.h = np.array([(right - left) / 2, (top - bottom) / 2])

    def sdf_many(self, points):
        q = np.abs(points - self.c) - self.h
        outside = np.linalg.norm(np.maximum(q, 0.0), axis=1)
        return outside + np.minimum(q.max(axis=1), 0.0)

    def to_mobject(self, **kwargs):
        kwargs.setdefault("color", WHITE)
        return Rectangle(
            width=2 * self.h[0], height=2 * self.h[1], **kwargs
        ).move_to(np.append(self.c, 0.0))


class CircleBoundary(Boundary):
    def __init__(self, center, radius):
        self.c = np.asarray(center, dtype=float)[:2]
        self.radius = radius

    def sdf_many(self, points):
        return np.linalg.norm(points - self.c, axis=1) - self.radius

    def normal_many(self, points):
        d = points - self.c
        norm = np.linalg.norm(d, axis=1, keepdims=True)
        return d / np.maximum(norm, 1e-12)

    def to_mobject(self, **kwargs):
        kwargs.setdefault("color", WHITE)
        return Circle(radius=self.radius, **kwargs).move_to(
            np.append(self.c, 0.0)
        )


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

    def sdf_many(self, points):
        # first-order approximation; exact on the zero level set, which is
        # what collisions use
        q = points - self.c
        k0 = np.linalg.norm(q / self.r, axis=1)
        k1 = np.linalg.norm(q / self.r ** 2, axis=1)
        return np.where(
            k1 > 0, k0 * (k0 - 1) / np.maximum(k1, 1e-12), -self.r.min()
        )

    def normal_many(self, points):
        g = (points - self.c) / self.r ** 2
        norm = np.linalg.norm(g, axis=1, keepdims=True)
        return g / np.maximum(norm, 1e-12)

    def to_mobject(self, **kwargs):
        kwargs.setdefault("color", WHITE)
        return Ellipse(
            width=2 * self.r[0], height=2 * self.r[1], **kwargs
        ).move_to(np.append(self.c, 0.0))


class StadiumBoundary(Boundary):
    """Capsule: a horizontal segment of half-length `h`, inflated by `r`."""

    def __init__(self, center, h, r):
        self.c = np.asarray(center, dtype=float)[:2]
        self.h, self.r = h, r

    def sdf_many(self, points):
        q = points - self.c
        qx = q[:, 0] - np.clip(q[:, 0], -self.h, self.h)
        return np.hypot(qx, q[:, 1]) - self.r

    def to_mobject(self, **kwargs):
        kwargs.setdefault("color", WHITE)
        return RoundedRectangle(
            width=2 * (self.h + self.r),
            height=2 * self.r,
            corner_radius=self.r,
            **kwargs,
        ).move_to(np.append(self.c, 0.0))


class RingBoundary(Boundary):
    """Region between two concentric circles: the inner disc is an obstacle."""

    def __init__(self, center, r_inner, r_outer):
        self.c = np.asarray(center, dtype=float)[:2]
        self.ri, self.ro = r_inner, r_outer

    def sdf_many(self, points):
        d = np.linalg.norm(points - self.c, axis=1)
        return np.maximum(d - self.ro, self.ri - d)

    def to_mobject(self, **kwargs):
        kwargs.setdefault("color", WHITE)
        c = np.append(self.c, 0.0)
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
    w, arm = arm_half_width, arm_length
    return [
        (w, arm),
        (-w, arm),
        (-w, w),
        (-arm, w),
        (-arm, -w),
        (-w, -w),
        (-w, -arm),
        (w, -arm),
        (w, -w),
        (arm, -w),
        (arm, w),
        (w, w),
    ]


class PolygonBoundary(Boundary):
    """Any simple polygon, convex or not. verts: (N, 2) in order."""

    def __init__(self, verts):
        self.a = np.asarray(verts, dtype=float)[:, :2]
        self.b = np.roll(self.a, -1, axis=0)
        self.ab = self.b - self.a
        self.len2 = (self.ab ** 2).sum(1)

    def sdf_many(self, points):
        ap = points[:, None, :] - self.a[None]  # (N, E, 2)
        t = np.clip((ap * self.ab).sum(-1) / self.len2, 0, 1)
        closest = ap - np.expand_dims(t, -1) * self.ab
        d = np.linalg.norm(closest, axis=-1).min(axis=1)

        # ray-casting inside test
        x, y = points[:, 0:1], points[:, 1:2]
        crosses = (self.a[:, 1] > y) != (self.b[:, 1] > y)
        dy = np.where(self.ab[:, 1] == 0, 1, self.ab[:, 1])
        x_int = self.a[:, 0] + (y - self.a[:, 1]) * self.ab[:, 0] / dy
        inside = ((crosses & (x < x_int)).sum(axis=1) % 2) == 1
        return np.where(inside, -d, d)

    def to_mobject(self, **kwargs):
        kwargs.setdefault("color", WHITE)
        pts = [np.array([x, y, 0.0]) for x, y in self.a]
        return Polygon(*pts, **kwargs)


@dataclass(slots=True)
class World:
    pos: np.ndarray  # (N, 2), updated in place
    vel: np.ndarray  # (N, 2), updated in place
    boundary: Boundary
    # 0 = ideal point reflection; dot radius is draw-only
    wall_radius: float = 0.0
    max_bounces: int = 8

    def step(self, dt: float):
        pos, vel = self.pos, self.vel
        b, wr = self.boundary, self.wall_radius
        rem = np.full(len(pos), dt)
        active = np.arange(len(pos))
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


def draw_dots(pos: np.ndarray, dots: list[Dot]) -> Callable[[Mobject], Any]:
    p3 = np.zeros((len(dots), 3))

    def update(_: Mobject):
        p3[:, :2] = pos  # `pos` is World.pos, mutated in place
        for i, d in enumerate(dots):
            d.move_to(p3[i])

    return update


POINT_PALETTE: Final[tuple[ManimColor, ...]] = (
    BLUE,
    ORANGE,
    GREEN,
    PINK,
    YELLOW,
    PURPLE,
    RED,
    TEAL,
)


class BoundaryScene(Scene):
    simulation_time: int = 15
    boundary: Boundary
    points_origin: Vector3D = ORIGIN
    points_speed: float = 1.3
    points_radius: float = 0.017
    points_count: int = 5760
    colors_fractions: Sequence[float] = ()
    colors_start_angle: float = 0.0

    def point_colors(self) -> list[ManimColor]:
        if not self.colors_fractions:
            return [POINT_PALETTE[0]] * self.points_count
        if len(self.colors_fractions) > len(POINT_PALETTE):
            raise ValueError(
                f"at most {len(POINT_PALETTE)} fractions, "
                f"got {len(self.colors_fractions)}"
            )

        weights = np.asarray(self.colors_fractions, dtype=float)
        edges = np.round(
            np.cumsum(weights) / weights.sum() * self.points_count
        ).astype(int)
        point_ids = np.arange(self.points_count)
        idx = np.searchsorted(edges, point_ids, side="right")

        # rotate the whole color layout:
        # point i has angle i * TAU / points_count
        shift = int(round(self.colors_start_angle / TAU * self.points_count))
        idx = np.roll(idx, shift)
        return [POINT_PALETTE[i] for i in idx]

    def velocities(self, angles: np.ndarray) -> np.ndarray:
        directions = np.stack([np.cos(angles), np.sin(angles)], axis=1)
        return self.points_speed * directions

    def construct(self) -> None:
        angles = np.linspace(0, TAU, self.points_count, endpoint=False)
        origin = np.asarray(self.points_origin, dtype=float)[:2]
        pos = np.tile(origin, (self.points_count, 1))

        world = World(pos, self.velocities(angles), self.boundary)

        def world_updater(_, dt):
            world.step(dt)

        world_group = VGroup(self.boundary.to_mobject())
        world_group.add_updater(world_updater)

        dots = [
            Dot(
                np.append(pos[i], 0.0),
                radius=self.points_radius,
                color=c,
                num_components=4,
            )
            for i, c in enumerate(self.point_colors())
        ]
        dots_group = VGroup(*dots).add_updater(draw_dots(world.pos, dots))

        self.add(world_group)
        self.add_foreground_mobjects(dots_group)
        self.wait(self.simulation_time)


class CircleLight(BoundaryScene):
    """
    Title:
    Light Bouncing Inside a Circle (Off-Center Source)

    Description:
    5,760 points of light start from one spot inside a circle and bounce off its wall for 15 seconds. The source is off-
    center, so the pattern is not symmetric.

    The circle has radius 2 and the source sits one third of the radius above the center. The points leave in 5,760
    evenly spaced directions at speed 1.3. The directions pointing left are blue and the directions pointing right are
    orange, so you can follow where each half of the light ends up.

    Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line
    at constant speed and reflects perfectly off the wall: the angle of incidence equals the angle of reflection. The
    simulation is vectorised with NumPy, so all 5,760 points advance together every frame, and the exact moment each
    point meets the wall is found by bisection.

    #Manim #Simulation #Math

    Tags:
    circle billiard, off-center light source, mathematical billiards, dynamical billiards, reflection, light simulation,
    manim, python, simulation, mathematics, physics visualization

    Category: Science & Technology
    Language: en
    Visibility: public
    Made for kids: no
    Thumbnail text: Off-Center Source
    """

    boundary = CircleBoundary((0, 0), 2.0)
    points_origin = UP * (2 / 3)  # same 1/3-of-radius offset as before
    colors_fractions = [1, 1]
    colors_start_angle = PI / 2


class HexagonLight(BoundaryScene):
    """
    Title:
    Light Bouncing Inside a Hexagon

    Description:
    5,760 points of light start at the center of a regular hexagon and bounce off its walls for 15 seconds.

    The hexagon has a circumradius of 2 and the source sits at its center. The points leave in 5,760 evenly spaced
    directions at speed 1.3. The directions are split into six equal 60-degree sectors, one color each, so you can
    follow where every sector of the light travels.

    Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line
    at constant speed and reflects perfectly off the wall: the angle of incidence equals the angle of reflection. The
    simulation is vectorised with NumPy, so all 5,760 points advance together every frame, and the exact moment each
    point meets the wall is found by bisection.

    #Manim #Simulation #Math

    Tags:
    hexagon billiard, polygon billiard, mathematical billiards, dynamical billiards, reflection, light simulation,
    manim, python, simulation, mathematics, physics visualization

    Category: Science & Technology
    Language: en
    Visibility: public
    Made for kids: no
    Thumbnail text: Six Colors
    """

    # vertices on the x-axis, so half-width = R
    boundary = PolygonBoundary(regular_polygon(6, 2.0))
    colors_fractions = [1, 1, 1, 1, 1, 1]


class StarLight(BoundaryScene):
    """
    Title:
    Light Bouncing Inside a Five-Pointed Star

    Description:
    5,760 points of light start at the center of a five-pointed star and bounce around its concave walls for 15 seconds.

    The star has an outer radius of 2.1 and an inner radius of 0.92, so its tips span about 4 units across, and the
    source sits at its center. The points leave in 5,760 evenly spaced directions at speed 1.3. The directions are split
    into five equal 72-degree sectors, one color each.

    Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line
    at constant speed and reflects perfectly off the wall: the angle of incidence equals the angle of reflection. The
    simulation is vectorised with NumPy, so all 5,760 points advance together every frame, and the exact moment each
    point meets the wall is found by bisection.

    #Manim #Simulation #Math

    Tags:
    star billiard, non-convex billiard, mathematical billiards, dynamical billiards, reflection, light simulation,
    manim, python, simulation, mathematics, physics visualization

    Category: Science & Technology
    Language: en
    Visibility: public
    Made for kids: no
    Thumbnail text: Five Colors
    """

    # widest tips at ±outer·cos(18°) ≈ ±0.951·outer, so outer = 2.1 gives ±2.0
    boundary = PolygonBoundary(star(5, 2.1, 0.92))
    colors_fractions = [1, 1, 1, 1, 1]
    colors_start_angle = PI / 2 - TAU / 10 - TAU / 5


class CrossLight(BoundaryScene):
    """
    Title:
    Light Bouncing Inside a Cross-Shaped Room

    Description:
    5,760 points of light start at the center of a cross-shaped room and bounce off its walls for 15 seconds.

    Each arm of the cross is 1.06 wide and reaches 2 units from the center, where the source sits. The points leave in
    5,760 evenly spaced directions at speed 1.3. Each of the four colors covers the directions that point toward one
    arm.

    Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line
    at constant speed and reflects perfectly off the wall: the angle of incidence equals the angle of reflection. The
    simulation is vectorised with NumPy, so all 5,760 points advance together every frame, and the exact moment each
    point meets the wall is found by bisection.

    #Manim #Simulation #Math

    Tags:
    cross billiard, non-convex billiard, mathematical billiards, dynamical billiards, reflection, light simulation,
    manim, python, simulation, mathematics, physics visualization

    Category: Science & Technology
    Language: en
    Visibility: public
    Made for kids: no
    Thumbnail text: Four Colors
    """

    boundary = PolygonBoundary(cross(0.53, 2.0))
    colors_fractions = [1, 1, 1, 1]
    colors_start_angle = -PI / 4


class EllipseLight(BoundaryScene):
    """
    Title:
    Light Bouncing Inside an Ellipse, Starting at a Focus

    Description:
    5,760 points of light start at one focus of an ellipse and bounce off its wall for 15 seconds.

    The ellipse is 4 wide and 6 tall, and the source sits at its bottom focus. The points leave in 5,760 evenly spaced
    directions at speed 1.3. A ray that leaves one focus of an ellipse reflects through the other focus, so watch the
    points gather there.

    Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line
    at constant speed and reflects perfectly off the wall: the angle of incidence equals the angle of reflection. The
    simulation is vectorised with NumPy, so all 5,760 points advance together every frame, and the exact moment each
    point meets the wall is found by bisection.

    #Manim #Simulation #Math

    Tags:
    ellipse billiard, ellipse foci, mathematical billiards, dynamical billiards, reflection, light simulation, manim,
    python, simulation, mathematics, physics visualization

    Category: Science & Technology
    Language: en
    Visibility: public
    Made for kids: no
    Thumbnail text: Start at Focus
    """

    boundary = EllipseBoundary((0, 0), 2.0, 3.0)  # 4.0 wide, 6.0 tall
    points_origin = boundary.foci[0]  # bottom focus, (0, -2.236)
    colors_fractions = [1]


class StadiumLight(BoundaryScene):
    """
    Title:
    Light Bouncing Inside a Stadium Shape

    Description:
    5,760 points of light start at the center of a stadium shape (two half circles joined by straight walls) and bounce
    off its walls for 15 seconds.

    The stadium is 4 wide and 1.7 tall: a straight segment of half-length 1.15 inflated by a radius of 0.85. The points
    leave in 5,760 evenly spaced directions at speed 1.3. The quarter of the directions that point right is blue and the
    remaining three quarters are orange.

    Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line
    at constant speed and reflects perfectly off the wall: the angle of incidence equals the angle of reflection. The
    simulation is vectorised with NumPy, so all 5,760 points advance together every frame, and the exact moment each
    point meets the wall is found by bisection.

    #Manim #Simulation #Math

    Tags:
    stadium billiard, Bunimovich stadium, mathematical billiards, dynamical billiards, reflection, light simulation,
    manim, python, simulation, mathematics, physics visualization

    Category: Science & Technology
    Language: en
    Visibility: public
    Made for kids: no
    Thumbnail text: Stadium Billiard
    """

    boundary = StadiumBoundary((0, 0), 1.15, 0.85)  # width 2·(1.15+0.85)=4.0
    colors_fractions = [1, 3]
    colors_start_angle = -PI / 4


class RingLight(BoundaryScene):
    """
    Title:
    Light Bouncing Between Two Circles: Annular Billiard

    Description:
    5,760 points of light start inside a ring and bounce off both the outer wall and the inner disc for 15 seconds.

    The ring lies between circles of radius 2 and 0.67, and the inner disc is an obstacle. The source sits in the middle
    of the band, 1.33 from the center. The points leave in 5,760 evenly spaced directions at speed 1.3.

    Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line
    at constant speed and reflects perfectly off the wall: the angle of incidence equals the angle of reflection. The
    simulation is vectorised with NumPy, so all 5,760 points advance together every frame, and the exact moment each
    point meets the wall is found by bisection.

    #Manim #Simulation #Math

    Tags:
    annular billiard, ring billiard, mathematical billiards, dynamical billiards, reflection, light simulation, manim,
    python, simulation, mathematics, physics visualization

    Category: Science & Technology
    Language: en
    Visibility: public
    Made for kids: no
    Thumbnail text: Inside the Ring
    """

    boundary = RingBoundary((0, 0), 0.67, 2.0)
    points_origin = RIGHT * 1.33  # mid-band, as before
    colors_fractions = [1]


del BoundaryScene
