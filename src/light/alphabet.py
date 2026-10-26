from typing import Sequence

import numpy as np

BOX_HALF_WIDTH = 1.5
BOX_HALF_HEIGHT = 2.0
BEAM_WIDTH = 0.8
WINDOW_HALF_WIDTH = BOX_HALF_WIDTH + BEAM_WIDTH / 2
WINDOW_HALF_HEIGHT = BOX_HALF_HEIGHT + BEAM_WIDTH / 2
FIRST_RING = 1.2
RING_GAP = 1.2
HOP = 1.5
MIRROR_SPACING = 1.1
CLEARANCE = BEAM_WIDTH / 2 + 0.05
RAY_REACH = 20.0
MAX_RING = 12
CANNON_DISTANCE = 2.0
EXIT_DISTANCE = 2.0
MIRROR_SLACK = 0.1

L, R, T, B = -BOX_HALF_WIDTH, BOX_HALF_WIDTH, BOX_HALF_HEIGHT, -BOX_HALF_HEIGHT

Point = tuple[float, float]
Pass = Sequence[Point]
Segment = tuple[np.ndarray, np.ndarray]
_WINDOW = np.array([WINDOW_HALF_WIDTH, WINDOW_HALF_HEIGHT])
_SIDE_TANGENTS = (np.array([0.0, 1.0]), np.array([-1.0, 0.0]), np.array([0.0, -1.0]), np.array([1.0, 0.0]))
_SIDE_NORMALS = (np.array([1.0, 0.0]), np.array([0.0, 1.0]), np.array([-1.0, 0.0]), np.array([0.0, -1.0]))


def _unit(start, end) -> np.ndarray:
    v = np.subtract(end, start, dtype=float)
    norm = np.linalg.norm(v)
    if norm < 1e-9:
        raise ValueError(f"zero-length segment at {tuple(start)}")
    return v / norm


def _window_exit(point, direction) -> float:
    hits = []
    for axis in (0, 1):
        if abs(direction[axis]) > 1e-9:
            edge = np.copysign(_WINDOW[axis], direction[axis])
            hits.append((edge - point[axis]) / direction[axis])
    return min(hits)


def _mirror(before, vertex, after) -> Segment:
    d_in, d_out = _unit(before, vertex), _unit(vertex, after)
    m = d_in - d_out
    norm = np.linalg.norm(m)
    if norm < 1e-9:
        raise ValueError(f"the path runs straight through {tuple(np.round(vertex, 2))}, which cannot hold a mirror")
    n = m / norm
    half = BEAM_WIDTH / 2 / abs(d_in @ n) + MIRROR_SLACK
    tangent = np.array([-n[1], n[0]])
    return vertex - half * tangent, vertex + half * tangent


def _point_segment_distance(p, a, b) -> float:
    ab = b - a
    t = np.clip((p - a) @ ab / max(ab @ ab, 1e-12), 0.0, 1.0)
    return float(np.linalg.norm(p - (a + t * ab)))


def _cross(o, a, b) -> float:
    return float((a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]))


def _segment_distance(first: Segment, second: Segment) -> float:
    a, b = first
    c, d = second
    if _cross(a, b, c) * _cross(a, b, d) < 0 and _cross(c, d, a) * _cross(c, d, b) < 0:
        return 0.0
    return min(
        _point_segment_distance(a, c, d),
        _point_segment_distance(b, c, d),
        _point_segment_distance(c, a, b),
        _point_segment_distance(d, a, b),
    )


def _ring_half(ring: int) -> np.ndarray:
    return _WINDOW + FIRST_RING + (ring - 1) * RING_GAP


def _corners(ring: int) -> list[np.ndarray]:
    w, h = _ring_half(ring)
    return [np.array(c, dtype=float) for c in ((w, -h), (w, h), (-w, h), (-w, -h))]


def _ring_hit(point, direction, ring: int) -> tuple[np.ndarray, int]:
    half = _ring_half(ring)
    best = None
    for axis in (0, 1):
        if abs(direction[axis]) < 1e-9:
            continue
        edge = np.copysign(half[axis], direction[axis])
        t = (edge - point[axis]) / direction[axis]
        if t <= 0:
            continue
        hit = point + direction * t
        if abs(hit[1 - axis]) <= half[1 - axis] + 1e-9 and (best is None or t < best[0]):
            side = (0 if direction[axis] > 0 else 2) if axis == 0 else (1 if direction[axis] > 0 else 3)
            best = (t, hit, side)
    if best is None:
        raise ValueError(f"ray from {tuple(np.round(point, 2))} never reaches ring {ring}")
    return best[1], best[2]


def _forced_sense(direction, side: int) -> int:
    along = float(direction @ _SIDE_TANGENTS[side])
    if abs(along) < 1e-9:
        return 0
    return -1 if along > 0 else 1


def _position(point, ring: int) -> float:
    w, h = _ring_half(ring)
    x, y = point
    if abs(y + h) < 1e-6:
        return x + w
    if abs(x - w) < 1e-6:
        return 2 * w + (y + h)
    if abs(y - h) < 1e-6:
        return 2 * w + 2 * h + (w - x)
    return 4 * w + 2 * h + (h - y)


def _traverse(start, end, ring: int, sense: int) -> list[np.ndarray]:
    w, h = _ring_half(ring)
    perimeter = 4 * w + 4 * h
    a, b = _position(start, ring), _position(end, ring)
    span = (sense * (b - a)) % perimeter
    corners = _corners(ring)
    passed = sorted(
        ((sense * (_position(c, ring) - a)) % perimeter, i)
        for i, c in enumerate(corners)
        if 1e-6 < (sense * (_position(c, ring) - a)) % perimeter < span - 1e-6
    )
    return [corners[i] for _, i in passed]


def _walk(start, ring: int, sense: int, distance: float) -> tuple[np.ndarray, list[np.ndarray], int]:
    w, h = _ring_half(ring)
    perimeter = 4 * w + 4 * h
    target = (_position(start, ring) + sense * distance) % perimeter
    if target < 2 * w:
        point, side = np.array([target - w, -h]), 3
    elif target < 2 * w + 2 * h:
        point, side = np.array([w, target - 2 * w - h]), 0
    elif target < 4 * w + 2 * h:
        point, side = np.array([w - (target - 2 * w - 2 * h), h]), 1
    else:
        point, side = np.array([-w, h - (target - 4 * w - 2 * h)]), 2
    if min(np.linalg.norm(point - c) for c in _corners(ring)) < MIRROR_SPACING:
        return _walk(start, ring, sense, distance + HOP)
    return point, _traverse(start, point, ring, sense), side


def _candidate(exit_point, exit_dir, entry_point, entry_dir, ring: int) -> tuple[list[np.ndarray], int]:
    start, start_side = _ring_hit(exit_point, exit_dir, ring)
    start_sense = _forced_sense(exit_dir, start_side)
    end, end_side = _ring_hit(entry_point, -entry_dir, ring)
    end_sense = -_forced_sense(-entry_dir, end_side)
    if start_sense == 0 or end_sense == 0 or start_sense == end_sense:
        sense = start_sense or end_sense or 1
        return [start, *_traverse(start, end, ring, sense), end], 1
    hop, corners, side = _walk(start, ring, start_sense, HOP)
    landing = hop + _SIDE_NORMALS[side] * RING_GAP
    end, _ = _ring_hit(entry_point, -entry_dir, ring + 1)
    return [start, *corners, hop, landing, *_traverse(landing, end, ring + 1, end_sense), end], 2


def _clear(mirrors: list[Segment], segments: list[Segment]) -> bool:
    return all(_segment_distance(m, s) >= CLEARANCE for m in mirrors for s in segments)


class _Layout:
    def __init__(self, strokes: list[np.ndarray], retrace: bool):
        self.strokes = strokes
        self.retrace = retrace
        self.mirrors: list[Segment] = []
        self.segments: list[Segment] = []
        self.entry_rays: list[Segment] = []
        self.exit_rays: list[Segment] = []
        last = len(strokes) - 1
        for i, stroke in enumerate(strokes):
            self.segments.extend((a, b) for a, b in zip(stroke, stroke[1:]))
            self.mirrors.extend(_mirror(a, b, c) for a, b, c in zip(stroke, stroke[1:], stroke[2:]))
            d_in = _unit(stroke[0], stroke[1])
            t = _window_exit(stroke[0], -d_in)
            reach = CANNON_DISTANCE if i == 0 and not retrace else RAY_REACH
            self.entry_rays.append((stroke[0] - d_in * (t + reach), stroke[0]))
            if i == last and retrace:
                self.exit_rays.append((stroke[-1], stroke[-1]))
                continue
            d_out = _unit(stroke[-2], stroke[-1])
            t = _window_exit(stroke[-1], d_out)
            self.exit_rays.append((stroke[-1], stroke[-1] + d_out * (t + RAY_REACH)))
        junction = strokes[-1][-1] if retrace else None
        for i, stroke in enumerate(strokes):
            others = [s for j in range(len(strokes)) if j != i for s in (self.entry_rays[j], self.exit_rays[j])]
            for a, b, c in zip(stroke, stroke[1:], stroke[2:]):
                blocking = others + [s for s in self.segments if not _is_endpoint(b, s)]
                if junction is not None and np.linalg.norm(b - junction) < 1e-9:
                    blocking = [s for s in blocking if not _is_endpoint(junction, s)]
                if not _clear([_mirror(a, b, c)], blocking):
                    raise ValueError(f"another stroke's beam passes through the mirror at {tuple(np.round(b, 2))}")

    def fixed_segments(self, transition: int) -> list[Segment]:
        rays = []
        for j in range(len(self.strokes)):
            if j != transition + 1:
                rays.append(self.entry_rays[j])
            if j != transition:
                rays.append(self.exit_rays[j])
        return self.segments + rays

    def accept(self, route: list[np.ndarray], transition: int) -> None:
        exit_point = self.strokes[transition][-1]
        entry_point = self.strokes[transition + 1][0]
        chain = [exit_point, *route, entry_point]
        self.segments.extend((a, b) for a, b in zip(chain, chain[1:]))
        self.mirrors.extend(_mirror(a, b, c) for a, b, c in zip(chain, chain[1:], chain[2:]))
        self.entry_rays[transition + 1] = (entry_point, entry_point)
        self.exit_rays[transition] = (exit_point, exit_point)

    def fits(self, route: list[np.ndarray], transition: int) -> bool:
        exit_point = self.strokes[transition][-1]
        entry_point = self.strokes[transition + 1][0]
        chain = [exit_point, *route, entry_point]
        own_segments = [(a, b) for a, b in zip(chain, chain[1:])]
        own_mirrors = [_mirror(a, b, c) for a, b, c in zip(chain, chain[1:], chain[2:])]
        if any(np.linalg.norm(a - b) < MIRROR_SPACING for a, b in zip(route, route[1:])):
            return False
        if not _clear(own_mirrors, self.fixed_segments(transition)):
            return False
        if not _clear(self.mirrors, own_segments):
            return False
        for k, mirror in enumerate(own_mirrors):
            apart = [s for j, s in enumerate(own_segments) if j not in (k, k + 1)]
            if not _clear([mirror], apart):
                return False
        return True


def _is_endpoint(point, segment: Segment) -> bool:
    return bool(np.linalg.norm(point - segment[0]) < 1e-9 or np.linalg.norm(point - segment[1]) < 1e-9)


def retraces(passes: Sequence[Pass]) -> bool:
    strokes = [np.asarray(p, dtype=float) for p in passes]
    end = strokes[-1][-1]
    return any(np.linalg.norm(end - point) < 1e-9 for stroke in strokes[:-1] for point in stroke[1:-1])


def letter_path(passes: Sequence[Pass]) -> list[Point]:
    strokes = [np.asarray(p, dtype=float) for p in passes]
    layout = _Layout(strokes, retraces(passes))
    first_dir = _unit(strokes[0][0], strokes[0][1])
    points: list[np.ndarray] = [strokes[0][0] - first_dir * (_window_exit(strokes[0][0], -first_dir) + CANNON_DISTANCE)]
    ring = 1
    for transition, (stroke, following) in enumerate(zip(strokes, strokes[1:])):
        points.extend(stroke[1:-1])
        exit_dir = _unit(stroke[-2], stroke[-1])
        entry_dir = _unit(following[0], following[1])
        for candidate_ring in range(ring, MAX_RING + 1):
            route, used = _candidate(stroke[-1], exit_dir, following[0], entry_dir, candidate_ring)
            if layout.fits(route, transition):
                break
        else:
            raise ValueError(f"no clear route from pass {transition + 1} to pass {transition + 2}; reorder or redirect passes")
        layout.accept(route, transition)
        points.extend(route)
        ring = candidate_ring + used
    last = strokes[-1]
    points.extend(last[1:-1])
    if layout.retrace:
        points.append(last[-1])
    else:
        last_dir = _unit(last[-2], last[-1])
        t = _window_exit(last[-1], last_dir)
        points.append(last[-1] + last_dir * (t + EXIT_DISTANCE))
    cleaned = [points[0]]
    for p in points[1:]:
        if np.linalg.norm(p - cleaned[-1]) > 1e-6:
            cleaned.append(p)
    return [(float(x), float(y)) for x, y in cleaned]


def mirror_half_lengths(path: Sequence[Point]) -> list[float]:
    p = np.asarray(path, dtype=float)
    return [float(np.linalg.norm(b - a) / 2) for a, b in (_mirror(*triple) for triple in zip(p, p[1:], p[2:]))]


def path_length(path: Sequence[Point]) -> float:
    p = np.asarray(path, dtype=float)
    return float(np.linalg.norm(np.diff(p, axis=0), axis=1).sum())


def heading(path: Sequence[Point]) -> float:
    d = _unit(path[0], path[1])
    return float(np.arctan2(d[1], d[0]))


def visible_segments(passes: Sequence[Pass]) -> list[tuple[Point, Point]]:
    segments = []
    strokes = [np.asarray(p, dtype=float) for p in passes]
    for i, stroke in enumerate(strokes):
        d_in = _unit(stroke[0], stroke[1])
        t = _window_exit(stroke[0], -d_in)
        segments.append((tuple(stroke[0] - d_in * t), tuple(stroke[0])))
        segments.extend((tuple(a), tuple(b)) for a, b in zip(stroke, stroke[1:]))
        if i == len(strokes) - 1 and retraces(passes):
            continue
        d_out = _unit(stroke[-2], stroke[-1])
        t = _window_exit(stroke[-1], d_out)
        segments.append((tuple(stroke[-1]), tuple(stroke[-1] + d_out * t)))
    return segments


def travel_length(passes: Sequence[Pass]) -> float:
    length = path_length(letter_path(passes))
    return 2 * length if retraces(passes) else length
