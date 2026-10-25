from abc import ABC, abstractmethod

import numpy as np
from manim import (
    PI,
    TAU,
    WHITE,
    Circle,
    Ellipse,
    Polygon,
    Rectangle,
    RoundedRectangle,
    VGroup,
    VMobject,
)


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
