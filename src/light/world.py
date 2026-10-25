from dataclasses import dataclass

import numpy as np

from light.boundaries import Boundary


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
