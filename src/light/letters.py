import math
from typing import Sequence

from manim import (
    BLACK,
    BLUE,
    DOWN,
    GREEN,
    LEFT,
    ORANGE,
    PINK,
    PURPLE,
    RED,
    RIGHT,
    TEAL,
    UP,
    YELLOW,
    Rectangle,
)

from light.alphabet import (
    B,
    BEAM_WIDTH,
    L,
    R,
    T,
    WINDOW_HALF_HEIGHT,
    WINDOW_HALF_WIDTH,
    Pass,
    heading,
    letter_path,
    mirror_half_lengths,
    travel_length,
)
from light.base import ASSETS_DIR, BoundaryScene
from light.boundaries import MirrorPath
from light.cannon import WideCannon
from light.coloring import Gradient
from light.distribution import Normal
from light.sound import Sample

RAINBOW = (BLUE, TEAL, GREEN, YELLOW, ORANGE, RED, PINK, PURPLE)


class LetterShortLight(BoundaryScene):
    passes: Sequence[Pass]
    velocity: float = 3.0
    firing_time: float = 10.0
    points_radius = 0.03

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        path = letter_path(cls.passes)
        cls.boundary = MirrorPath(path, half_length=mirror_half_lengths(path))
        cls.cannon = WideCannon(
            origin=path[0],
            direction=heading(path),
            width=BEAM_WIDTH,
            velocity=cls.velocity,
            spawn_rate=120.0,
            firing_time=cls.firing_time,
            distribution=Normal(2),
            coloring=Gradient(RAINBOW),
            sound=Sample(ASSETS_DIR / "bubble.wav", gain=-15, every=20, every_jitter=4, gain_jitter=3),
        )
        cls.simulation_time = math.ceil(cls.firing_time + travel_length(cls.passes) / cls.velocity + 0.5)

    def construct(self) -> None:
        edges = ((LEFT, WINDOW_HALF_WIDTH), (RIGHT, WINDOW_HALF_WIDTH), (UP, WINDOW_HALF_HEIGHT), (DOWN, WINDOW_HALF_HEIGHT))
        for side, half in edges:
            curtain = Rectangle(width=20, height=20, fill_color=BLACK, fill_opacity=1, stroke_width=0)
            curtain.next_to(side * half, side, buff=0)
            self.add_foreground_mobjects(curtain)
        super().construct()


class AShortLight(LetterShortLight):
    passes = [[(R, B), (0.0, T), (L, B)], [(L, -1.2), (R, -1.2)]]


class BShortLight(LetterShortLight):
    passes = [[(L, B), (L, T)], [(L, T), (1.0, T), (1.0, 0.5), (L, 0.5)], [(L, B), (R, B), (R, -0.5), (L, -0.5)]]


class CShortLight(LetterShortLight):
    passes = [[(R, T), (-0.5, T), (L, 0.0), (-0.5, B), (R, B)]]


class DShortLight(LetterShortLight):
    passes = [[(L, T), (0.5, T), (R, 0.0), (0.5, B), (L, B)], [(L, B), (L, T)]]


class EShortLight(LetterShortLight):
    passes = [[(L, B), (L, T)], [(L, T), (R, T)], [(R, 0.0), (L, 0.0)], [(L, B), (R, B)]]


class FShortLight(LetterShortLight):
    passes = [[(L, B), (L, T)], [(L, T), (R, T)], [(R, 0.0), (L, 0.0)]]


class GShortLight(LetterShortLight):
    passes = [[(R, T), (L, T), (L, B), (R, B), (R, 0.0), (L, 0.0)]]


class HShortLight(LetterShortLight):
    passes = [[(L, 0.0), (R, 0.0)], [(R, B), (R, T)], [(L, T), (L, B)]]


class IShortLight(LetterShortLight):
    passes = [[(L, T), (R, T)], [(0.0, T), (0.0, B)], [(R, B), (L, B)]]


class JShortLight(LetterShortLight):
    passes = [[(R, T), (0.5, T), (0.5, B), (L, B)]]


class KShortLight(LetterShortLight):
    passes = [[(R, T), (L, 0.0)], [(L, 0.0), (R, B)], [(L, B), (L, T)]]


class LShortLight(LetterShortLight):
    passes = [[(L, T), (L, B), (R, B)]]


class MShortLight(LetterShortLight):
    passes = [[(L, B), (L, T), (0.0, -0.8), (R, T), (R, B)]]


class NShortLight(LetterShortLight):
    passes = [[(L, B), (L, T), (R, B), (R, T)]]


class OShortLight(LetterShortLight):
    passes = [[(R, T), (L, T), (L, B), (R, B)], [(R, T), (R, B)]]


class PShortLight(LetterShortLight):
    passes = [[(L, B), (L, T)], [(L, T), (R, T), (R, 0.0), (L, 0.0)]]


class QShortLight(LetterShortLight):
    passes = [[(R, T), (L, T), (L, B), (R, B)], [(0.2, B), (R, -0.7)], [(R, T), (R, B)]]


class RShortLight(LetterShortLight):
    passes = [[(L, B), (L, T)], [(L, T), (R, T), (R, 0.0), (L, 0.0)], [(L, 0.0), (R, B)]]


class SShortLight(LetterShortLight):
    passes = [[(R, T), (L, T), (L, 0.4), (R, -0.4), (R, B), (L, B)]]


class TShortLight(LetterShortLight):
    passes = [[(L, T), (R, T)], [(0.0, T), (0.0, B)]]


class UShortLight(LetterShortLight):
    passes = [[(L, T), (L, B), (R, B), (R, T)]]


class VShortLight(LetterShortLight):
    passes = [[(L, T), (0.0, B), (R, T)]]


class WShortLight(LetterShortLight):
    passes = [[(L, T), (-0.75, B), (0.0, T), (0.75, B), (R, T)]]


class XShortLight(LetterShortLight):
    passes = [[(L, T), (R, B)], [(L, B), (R, T)]]


class YShortLight(LetterShortLight):
    passes = [[(L, T), (0.0, 0.0), (R, T)], [(0.0, B), (0.0, 0.0)]]


class ZShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter Z With Two Mirrors

Description:
A wide beam of dots flies in from the left, bounces off two mirrors and draws the letter Z in a 16-second vertical
Short, then switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so the stroke is dense in the middle and soft
at the edges. The letter is 3 wide and 4 tall. The dots enter along the top bar at speed 3, 120 per second, 1,200 in
total. A mirror at the top-right corner sends them down the diagonal, a mirror at the bottom-left corner sends them
along the bottom bar, and they leave through the right edge. Each new dot is a slightly different color, moving
through blue, teal, green, yellow, orange, red, pink and purple, so the Z is drawn in changing hues. Roughly one dot in
every 20 pops a bubble sound as it appears, with random timing and loudness. After 10 seconds the beam stops, and the
last dots trace the Z and leave just before the video ends.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The
mirror angles are computed from the path the beam should follow, each dot's starting height is drawn with NumPy from a
fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #manim #simulation

Tags:
letter z, mirror reflection, wide beam, normal distribution, bell curve, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Two Mirrors
    """

    passes = [[(L, T), (R, T), (L, B), (R, B)]]


del BoundaryScene, LetterShortLight
