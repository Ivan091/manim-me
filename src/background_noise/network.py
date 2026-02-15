import random
from dataclasses import dataclass
from itertools import combinations
from typing import Callable, Any

from manim import *
from manim.typing import Point3D, Vector3D


@dataclass(slots=True)
class Point:
    position: Point3D
    radius: float
    velocity: Vector3D


@dataclass(slots=True)
class World:
    points: list[Point]
    top_bound: float = 4
    bottom_bound: float = -4
    right_bound: float = 7.111
    left_bound: float = -7.111

    def step(self, dt: float):
        for p in self.points:
            nxt = p.position + p.velocity * dt

            r = p.radius
            lo_x, hi_x = self.left_bound + r, self.right_bound - r
            lo_y, hi_y = self.bottom_bound + r, self.top_bound - r

            # reflect x with overshoot correction
            if nxt[0] < lo_x:
                nxt[0] = lo_x + (lo_x - nxt[0])
                p.velocity[0] *= -1
            elif nxt[0] > hi_x:
                nxt[0] = hi_x - (nxt[0] - hi_x)
                p.velocity[0] *= -1

            # reflect y with overshoot correction
            if nxt[1] < lo_y:
                nxt[1] = lo_y + (lo_y - nxt[1])
                p.velocity[1] *= -1
            elif nxt[1] > hi_y:
                nxt[1] = hi_y - (nxt[1] - hi_y)
                p.velocity[1] *= -1

            p.position = nxt


def draw_dots(points: list[Point], dots_static_pool: list[Dot]) -> Callable[[Mobject], Any]:
    def update(_: Mobject):
        for i, d in enumerate(dots_static_pool):
            d.move_to(points[i].position)

    return update


def draw_lines(points: list[Point],
               edges_static_pool: dict[tuple[int, int], Line],
               active_edges: set[tuple[int, int]],
               max_line_len: int) -> Callable[[Mobject], Any]:

    neighbors = [(0, 1), (1, 1), (1, 0), (1, -1)]

    def updater(line_layer: Mobject):
        groups: dict[tuple[int, int], list[int]] = dict()

        def point_group(point: Point) -> tuple[int, int]:
            x, y, _ = point.position
            return int(np.floor(x / max_line_len)), int(np.floor(y / max_line_len))

        for idx, p in enumerate(points):
            xg, yg = point_group(p)
            groups.setdefault((xg, yg), []).append(idx)

        new_active_keys: set[tuple[int, int]] = set()

        for idxs in groups.values():
            for i, j in combinations(idxs, 2):  # i < j guaranteed
                new_active_keys.add((i, j))

        for (cx, cy), idxs in groups.items():
            for dx, dy in neighbors:
                x, y = cx + dx, cy + dy
                for i in idxs:
                    for j in groups.get((x, y), []):
                        a, b = (i, j) if i < j else (j, i)
                        new_active_keys.add((a, b))

        for key in set(active_edges):
            if key not in new_active_keys:
                active_edges.discard(key)
                ln = edges_static_pool[key]
                ln.set_opacity(0)
                line_layer.remove(ln)

        for key in new_active_keys:
            ln = edges_static_pool[key]

            p1, p2 = points[key[0]], points[key[1]]
            dist = np.linalg.norm(p1.position - p2.position)

            if dist < max_line_len:
                if key not in active_edges:
                    line_layer.add(ln)
                    active_edges.add(key)

                t = dist / max_line_len
                ln.set_points_by_ends(p1.position, p2.position)
                ln.set_opacity(1 - t)
                ln.set_color(interpolate_color(RED, BLUE, t))

            elif key in active_edges:
                active_edges.discard(key)
                ln.set_opacity(0)
                line_layer.remove(ln)

    return updater


def random_velocity(min_speed: float = 1.5, max_speed: float = 2) -> Vector3D:
    speed = random.uniform(min_speed, max_speed)
    angle = random.uniform(0, TAU)
    return np.array([np.cos(angle) * speed, np.sin(angle) * speed, 0.0], dtype=float)


class Network(Scene):

    def construct(self):
        simulation_time: int = 600
        max_line_len: int = 2
        points_count: int = 100

        points = [Point(ORIGIN, DEFAULT_DOT_RADIUS, random_velocity()) for _ in range(points_count)]
        world = World(points)
        world_updater = lambda _, dt: world.step(dt)
        world_group = VGroup().add_updater(world_updater)

        dots_static_pool = [Dot(p.position, radius=p.radius) for p in points]
        draw_dots_updater = draw_dots(points, dots_static_pool)
        dots_group = VGroup(dots_static_pool).add_updater(draw_dots_updater)

        edges_static_pool: dict[tuple[int, int], Line] = {
            (i, j): Line(ORIGIN, ORIGIN).set_opacity(0)
            for i in range(len(points))
            for j in range(i + 1, len(points))
        }
        active_edges: set[tuple[int, int]] = set()
        draw_lines_updater = draw_lines(points, edges_static_pool, active_edges, max_line_len)
        edge_group = VGroup(edges_static_pool.values()).add_updater(draw_lines_updater)

        self.add(world_group)
        self.add_foreground_mobjects(dots_group)
        self.add(edge_group)

        for _ in range(simulation_time):
            self.wait(1)
