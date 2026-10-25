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
    path_length,
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
        cls.simulation_time = math.ceil(cls.firing_time + path_length(path) / cls.velocity + 0.5)

    def construct(self) -> None:
        edges = ((LEFT, WINDOW_HALF_WIDTH), (RIGHT, WINDOW_HALF_WIDTH), (UP, WINDOW_HALF_HEIGHT), (DOWN, WINDOW_HALF_HEIGHT))
        for side, half in edges:
            curtain = Rectangle(width=20, height=20, fill_color=BLACK, fill_opacity=1, stroke_width=0)
            curtain.next_to(side * half, side, buff=0)
            self.add_foreground_mobjects(curtain)
        super().construct()


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
