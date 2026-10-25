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
    velocity: float = 7.0
    spawn_rate: float = 280.0
    hold_time: float = 4.0
    mirror_radius: float = 0.07
    veil_opacity: float = 0.8
    points_radius = 0.03

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        path = letter_path(cls.passes)
        travel_time = travel_length(cls.passes) / cls.velocity
        cls.firing_time = math.ceil(travel_time + cls.hold_time)
        cls.simulation_time = math.ceil(cls.firing_time + travel_time + 1.0)
        cls.boundary = MirrorPath(path, half_length=mirror_half_lengths(path), radius=cls.mirror_radius)
        cls.cannon = WideCannon(
            origin=path[0],
            direction=heading(path),
            width=BEAM_WIDTH,
            velocity=cls.velocity,
            spawn_rate=cls.spawn_rate,
            firing_time=cls.firing_time,
            distribution=Normal(2),
            coloring=Gradient(RAINBOW),
            sound=Sample(ASSETS_DIR / "bubble.wav", gain=-22, every=150, every_jitter=50, gain_jitter=4),
        )

    def construct(self) -> None:
        w, h, far = WINDOW_HALF_WIDTH, WINDOW_HALF_HEIGHT, 20.0
        strips = (
            (far, 2 * far, LEFT, w),
            (far, 2 * far, RIGHT, w),
            (2 * w, far, UP, h),
            (2 * w, far, DOWN, h),
        )
        for width, height, side, half in strips:
            veil = Rectangle(width=width, height=height, fill_color=BLACK, fill_opacity=self.veil_opacity, stroke_width=0)
            veil.next_to(side * half, side, buff=0)
            self.add_foreground_mobjects(veil)
        super().construct()


class AShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter A With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter A in a 15-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The A is pointed: two legs meet at a peak at the top, with a
crossbar a quarter of the way up. The letter is drawn in two straight passes. Between passes the beam leaves the frame,
where three hidden mirrors turn it around and send it back for the next stroke, and one mirror sits on the letter
itself. Outside the letter's box a dark veil dims the hidden mirrors and the beam's detours, so you can still follow
them. The dots move at speed 7, 280 per second, 2,521 in total. Each new dot is a slightly different color, moving
through blue, teal, green, yellow, orange, red, pink and purple, so the letter is drawn in changing hues. Roughly one
dot in every 150 makes a soft bubble sound as it appears, with random timing and loudness. The cannon fires for 9
seconds, long enough to light the whole letter at once for 4 seconds; then it stops, and the last dots finish the letter
and leave the frame just before the video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter a, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Four Mirrors
    """
    passes = [[(L, B), (0.0, T), (R, B)], [(L, -1.0), (R, -1.0)]]


class BShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter B With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter B in a 17-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The B is a stem with two square bowls, the upper one a little
narrower than the lower one. The letter is drawn in three straight passes. Between passes the beam leaves the frame,
where five hidden mirrors turn it around and send it back for the next stroke, and four mirrors sit on the letter
itself. Outside the letter's box a dark veil dims the hidden mirrors and the beam's detours, so you can still follow
them. The dots move at speed 7, 280 per second, 2,801 in total. Each new dot is a slightly different color, moving
through blue, teal, green, yellow, orange, red, pink and purple, so the letter is drawn in changing hues. Roughly one
dot in every 150 makes a soft bubble sound as it appears, with random timing and loudness. The cannon fires for 10
seconds, long enough to light the whole letter at once for 4 seconds; then it stops, and the last dots finish the letter
and leave the frame just before the video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter b, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Nine Mirrors
    """
    passes = [[(L, B), (L, T)], [(L, T), (1.0, T), (1.0, 0.5), (L, 0.5)], [(L, B), (R, B), (R, -0.5), (L, -0.5)]]


class CShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter C With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter C in a 9-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The C is pointed: its top and bottom bars meet a chevron on the
left side. The whole letter is drawn in one pass that turns at three mirrors. Outside the letter's box a dark veil dims
the beam as it comes in and goes out. The dots move at speed 7, 280 per second, 1,681 in total. Each new dot is a
slightly different color, moving through blue, teal, green, yellow, orange, red, pink and purple, so the letter is drawn
in changing hues. Roughly one dot in every 150 makes a soft bubble sound as it appears, with random timing and loudness.
The cannon fires for 6 seconds, long enough to light the whole letter at once for 4 seconds; then it stops, and the last
dots finish the letter and leave the frame just before the video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter c, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Three Mirrors
    """
    passes = [[(R, T), (-0.5, T), (L, 0.0), (-0.5, B), (R, B)]]


class DShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter D With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter D in a 11-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The D is a stem whose top and bottom bars slant in to meet at a
point on the right. The whole letter is drawn in one pass that turns at four mirrors. Outside the letter's box a dark
veil dims the beam as it comes in and goes out. The dots move at speed 7, 280 per second, 1,961 in total. Each new dot
is a slightly different color, moving through blue, teal, green, yellow, orange, red, pink and purple, so the letter is
drawn in changing hues. Roughly one dot in every 150 makes a soft bubble sound as it appears, with random timing and
loudness. The cannon fires for 7 seconds, long enough to light the whole letter at once for 4 seconds; then it stops,
and the last dots finish the letter and leave the frame just before the video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter d, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Four Mirrors
    """
    passes = [[(L, B), (L, T), (0.5, T), (R, 0.0), (0.5, B), (L, B)]]


class EShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter E With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter E in a 13-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The E is a stem with three full bars. The letter is drawn in two
straight passes. Between passes the beam leaves the frame, where two hidden mirrors turn it around and send it back for
the next stroke, and two mirrors sit on the letter itself. Outside the letter's box a dark veil dims the hidden mirrors
and the beam's detours, so you can still follow them. The dots move at speed 7, 280 per second, 2,241 in total. Each new
dot is a slightly different color, moving through blue, teal, green, yellow, orange, red, pink and purple, so the letter
is drawn in changing hues. Roughly one dot in every 150 makes a soft bubble sound as it appears, with random timing and
loudness. The cannon fires for 8 seconds, long enough to light the whole letter at once for 4 seconds; then it stops,
and the last dots finish the letter and leave the frame just before the video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter e, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Four Mirrors
    """
    passes = [[(R, T), (L, T), (L, B), (R, B)], [(R, 0.0), (L, 0.0)]]


class FShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter F With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter F in a 11-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The F is a stem with a top bar and a middle bar just above the
centre. The letter is drawn in two straight passes. Between passes the beam leaves the frame, where two hidden mirrors
turn it around and send it back for the next stroke, and one mirror sits on the letter itself. Outside the letter's box
a dark veil dims the hidden mirrors and the beam's detours, so you can still follow them. The dots move at speed 7, 280
per second, 1,961 in total. Each new dot is a slightly different color, moving through blue, teal, green, yellow,
orange, red, pink and purple, so the letter is drawn in changing hues. Roughly one dot in every 150 makes a soft bubble
sound as it appears, with random timing and loudness. The cannon fires for 7 seconds, long enough to light the whole
letter at once for 4 seconds; then it stops, and the last dots finish the letter and leave the frame just before the
video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter f, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Three Mirrors
    """
    passes = [[(L, 0.3), (R, 0.3)], [(R, T), (L, T), (L, B)]]


class GShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter G With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter G in a 11-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The G is square, with its inner bar running across the middle.
The whole letter is drawn in one pass that turns at four mirrors. Outside the letter's box a dark veil dims the beam as
it comes in and goes out. The dots move at speed 7, 280 per second, 1,961 in total. Each new dot is a slightly different
color, moving through blue, teal, green, yellow, orange, red, pink and purple, so the letter is drawn in changing hues.
Roughly one dot in every 150 makes a soft bubble sound as it appears, with random timing and loudness. The cannon fires
for 7 seconds, long enough to light the whole letter at once for 4 seconds; then it stops, and the last dots finish the
letter and leave the frame just before the video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter g, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Four Mirrors
    """
    passes = [[(R, T), (L, T), (L, B), (R, B), (R, 0.0), (L, 0.0)]]


class HShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter H With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter H in a 17-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The H is two legs joined by a crossbar. The letter is drawn in
three straight passes. Between passes the beam leaves the frame, where five hidden mirrors turn it around and send it
back for the next stroke; every stroke on the letter itself is a straight line with no mirror on it. Outside the
letter's box a dark veil dims the hidden mirrors and the beam's detours, so you can still follow them. The dots move at
speed 7, 280 per second, 2,801 in total. Each new dot is a slightly different color, moving through blue, teal, green,
yellow, orange, red, pink and purple, so the letter is drawn in changing hues. Roughly one dot in every 150 makes a soft
bubble sound as it appears, with random timing and loudness. The cannon fires for 10 seconds, long enough to light the
whole letter at once for 4 seconds; then it stops, and the last dots finish the letter and leave the frame just before
the video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter h, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Five Mirrors
    """
    passes = [[(L, T), (L, B)], [(R, B), (R, T)], [(L, 0.0), (R, 0.0)]]


class IShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter I With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter I in a 17-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The I is a stem with short serifs at the top and bottom. The
letter is drawn in three straight passes. Between passes the beam leaves the frame, where six hidden mirrors turn it
around and send it back for the next stroke; every stroke on the letter itself is a straight line with no mirror on it.
Outside the letter's box a dark veil dims the hidden mirrors and the beam's detours, so you can still follow them. The
dots move at speed 7, 280 per second, 2,801 in total. Each new dot is a slightly different color, moving through blue,
teal, green, yellow, orange, red, pink and purple, so the letter is drawn in changing hues. Roughly one dot in every 150
makes a soft bubble sound as it appears, with random timing and loudness. The cannon fires for 10 seconds, long enough
to light the whole letter at once for 4 seconds; then it stops, and the last dots finish the letter and leave the frame
just before the video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter i, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Six Mirrors
    """
    passes = [[(-0.9, T), (0.9, T)], [(0.0, T), (0.0, B)], [(0.9, B), (-0.9, B)]]


class JShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter J With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter J in a 9-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The J has a top serif, a stem and a square foot. The whole
letter is drawn in one pass that turns at two mirrors. Outside the letter's box a dark veil dims the beam as it comes in
and goes out. The dots move at speed 7, 280 per second, 1,681 in total. Each new dot is a slightly different color,
moving through blue, teal, green, yellow, orange, red, pink and purple, so the letter is drawn in changing hues. Roughly
one dot in every 150 makes a soft bubble sound as it appears, with random timing and loudness. The cannon fires for 6
seconds, long enough to light the whole letter at once for 4 seconds; then it stops, and the last dots finish the letter
and leave the frame just before the video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter j, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Two Mirrors
    """
    passes = [[(R, T), (0.5, T), (0.5, B), (L, B)]]


class KShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter K With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter K in a 13-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The K is a stem with two arms that meet just right of it in the
middle. The letter is drawn in two straight passes. Between passes the beam leaves the frame, where two hidden mirrors
turn it around and send it back for the next stroke, and one mirror sits on the letter itself. Outside the letter's box
a dark veil dims the hidden mirrors and the beam's detours, so you can still follow them. The dots move at speed 7, 280
per second, 2,241 in total. Each new dot is a slightly different color, moving through blue, teal, green, yellow,
orange, red, pink and purple, so the letter is drawn in changing hues. Roughly one dot in every 150 makes a soft bubble
sound as it appears, with random timing and loudness. The cannon fires for 8 seconds, long enough to light the whole
letter at once for 4 seconds; then it stops, and the last dots finish the letter and leave the frame just before the
video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter k, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Three Mirrors
    """
    passes = [[(1.1, B), (-0.9, 0.0), (1.1, T)], [(L, T), (L, B)]]


class LShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter L With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter L in a 9-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The L is a stem and a foot. The whole letter is drawn in one
pass that turns at one mirror. Outside the letter's box a dark veil dims the beam as it comes in and goes out. The dots
move at speed 7, 280 per second, 1,681 in total. Each new dot is a slightly different color, moving through blue, teal,
green, yellow, orange, red, pink and purple, so the letter is drawn in changing hues. Roughly one dot in every 150 makes
a soft bubble sound as it appears, with random timing and loudness. The cannon fires for 6 seconds, long enough to light
the whole letter at once for 4 seconds; then it stops, and the last dots finish the letter and leave the frame just
before the video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter l, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: One Mirror
    """
    passes = [[(L, T), (L, B), (R, B)]]


class MShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter M With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter M in a 11-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The M has two outer legs and a middle point that dips below the
centre. The whole letter is drawn in one pass that turns at three mirrors. Outside the letter's box a dark veil dims the
beam as it comes in and goes out. The dots move at speed 7, 280 per second, 1,961 in total. Each new dot is a slightly
different color, moving through blue, teal, green, yellow, orange, red, pink and purple, so the letter is drawn in
changing hues. Roughly one dot in every 150 makes a soft bubble sound as it appears, with random timing and loudness.
The cannon fires for 7 seconds, long enough to light the whole letter at once for 4 seconds; then it stops, and the last
dots finish the letter and leave the frame just before the video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter m, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Three Mirrors
    """
    passes = [[(L, B), (L, T), (0.0, -0.8), (R, T), (R, B)]]


class NShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter N With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter N in a 11-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The N is two legs joined by a diagonal. The whole letter is
drawn in one pass that turns at two mirrors. Outside the letter's box a dark veil dims the beam as it comes in and goes
out. The dots move at speed 7, 280 per second, 1,961 in total. Each new dot is a slightly different color, moving
through blue, teal, green, yellow, orange, red, pink and purple, so the letter is drawn in changing hues. Roughly one
dot in every 150 makes a soft bubble sound as it appears, with random timing and loudness. The cannon fires for 7
seconds, long enough to light the whole letter at once for 4 seconds; then it stops, and the last dots finish the letter
and leave the frame just before the video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter n, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Two Mirrors
    """
    passes = [[(L, B), (L, T), (R, B), (R, T)]]


class OShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter O With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter O in a 11-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The O is six-sided, pointed at the top and bottom, and its two
ends cross at the top. The whole letter is drawn in one pass that turns at five mirrors. Outside the letter's box a dark
veil dims the beam as it comes in and goes out. The dots move at speed 7, 280 per second, 1,961 in total. Each new dot
is a slightly different color, moving through blue, teal, green, yellow, orange, red, pink and purple, so the letter is
drawn in changing hues. Roughly one dot in every 150 makes a soft bubble sound as it appears, with random timing and
loudness. The cannon fires for 7 seconds, long enough to light the whole letter at once for 4 seconds; then it stops,
and the last dots finish the letter and leave the frame just before the video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter o, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Five Mirrors
    """
    passes = [[(0.0, T), (L, 1.0), (L, -1.0), (0.0, B), (R, -1.0), (R, 1.0), (0.0, T)]]


class PShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter P With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter P in a 11-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The P is a stem with a square bowl. The whole letter is drawn in
one pass that turns at three mirrors. Outside the letter's box a dark veil dims the beam as it comes in and goes out.
The dots move at speed 7, 280 per second, 1,961 in total. Each new dot is a slightly different color, moving through
blue, teal, green, yellow, orange, red, pink and purple, so the letter is drawn in changing hues. Roughly one dot in
every 150 makes a soft bubble sound as it appears, with random timing and loudness. The cannon fires for 7 seconds, long
enough to light the whole letter at once for 4 seconds; then it stops, and the last dots finish the letter and leave the
frame just before the video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter p, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Three Mirrors
    """
    passes = [[(L, B), (L, T), (R, T), (R, 0.0), (L, 0.0)]]


class QShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter Q With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter Q in a 15-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The Q is a rectangle with a diagonal tail cutting the
bottom-right corner. The letter is drawn in two straight passes. Between passes the beam leaves the frame, where two
hidden mirrors turn it around and send it back for the next stroke, and three mirrors sit on the letter itself. Outside
the letter's box a dark veil dims the hidden mirrors and the beam's detours, so you can still follow them. The dots move
at speed 7, 280 per second, 2,521 in total. Each new dot is a slightly different color, moving through blue, teal,
green, yellow, orange, red, pink and purple, so the letter is drawn in changing hues. Roughly one dot in every 150 makes
a soft bubble sound as it appears, with random timing and loudness. The cannon fires for 9 seconds, long enough to light
the whole letter at once for 4 seconds; then it stops, and the last dots finish the letter and leave the frame just
before the video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter q, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Five Mirrors
    """
    passes = [[(R, -0.7), (0.2, B)], [(L, B), (L, T), (R, T), (R, B), (L, B)]]


class RShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter R With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter R in a 11-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The R is a stem with a square bowl and a diagonal leg that
starts from the bowl's lower bar. The whole letter is drawn in one pass that turns at four mirrors. Outside the letter's
box a dark veil dims the beam as it comes in and goes out. The dots move at speed 7, 280 per second, 1,961 in total.
Each new dot is a slightly different color, moving through blue, teal, green, yellow, orange, red, pink and purple, so
the letter is drawn in changing hues. Roughly one dot in every 150 makes a soft bubble sound as it appears, with random
timing and loudness. The cannon fires for 7 seconds, long enough to light the whole letter at once for 4 seconds; then
it stops, and the last dots finish the letter and leave the frame just before the video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter r, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Four Mirrors
    """
    passes = [[(L, B), (L, T), (R, T), (R, 0.0), (-0.3, 0.0), (R, B)]]


class SShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter S With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter S in a 11-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The S is angular, with a slanted middle stroke. The whole letter
is drawn in one pass that turns at four mirrors. Outside the letter's box a dark veil dims the beam as it comes in and
goes out. The dots move at speed 7, 280 per second, 1,961 in total. Each new dot is a slightly different color, moving
through blue, teal, green, yellow, orange, red, pink and purple, so the letter is drawn in changing hues. Roughly one
dot in every 150 makes a soft bubble sound as it appears, with random timing and loudness. The cannon fires for 7
seconds, long enough to light the whole letter at once for 4 seconds; then it stops, and the last dots finish the letter
and leave the frame just before the video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter s, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Four Mirrors
    """
    passes = [[(R, T), (L, T), (L, 0.4), (R, -0.4), (R, B), (L, B)]]


class TShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter T With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter T in a 11-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The T is a bar and a stem. The letter is drawn in two straight
passes. Between passes the beam leaves the frame, where three hidden mirrors turn it around and send it back for the
next stroke; every stroke on the letter itself is a straight line with no mirror on it. Outside the letter's box a dark
veil dims the hidden mirrors and the beam's detours, so you can still follow them. The dots move at speed 7, 280 per
second, 1,961 in total. Each new dot is a slightly different color, moving through blue, teal, green, yellow, orange,
red, pink and purple, so the letter is drawn in changing hues. Roughly one dot in every 150 makes a soft bubble sound as
it appears, with random timing and loudness. The cannon fires for 7 seconds, long enough to light the whole letter at
once for 4 seconds; then it stops, and the last dots finish the letter and leave the frame just before the video ends,
so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter t, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Three Mirrors
    """
    passes = [[(L, T), (R, T)], [(0.0, T), (0.0, B)]]


class UShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter U With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter U in a 11-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The U is square. The whole letter is drawn in one pass that
turns at two mirrors. Outside the letter's box a dark veil dims the beam as it comes in and goes out. The dots move at
speed 7, 280 per second, 1,961 in total. Each new dot is a slightly different color, moving through blue, teal, green,
yellow, orange, red, pink and purple, so the letter is drawn in changing hues. Roughly one dot in every 150 makes a soft
bubble sound as it appears, with random timing and loudness. The cannon fires for 7 seconds, long enough to light the
whole letter at once for 4 seconds; then it stops, and the last dots finish the letter and leave the frame just before
the video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter u, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Two Mirrors
    """
    passes = [[(L, T), (L, B), (R, B), (R, T)]]


class VShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter V With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter V in a 9-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The V is two diagonals meeting at a point at the bottom. The
whole letter is drawn in one pass that turns at one mirror. Outside the letter's box a dark veil dims the beam as it
comes in and goes out. The dots move at speed 7, 280 per second, 1,681 in total. Each new dot is a slightly different
color, moving through blue, teal, green, yellow, orange, red, pink and purple, so the letter is drawn in changing hues.
Roughly one dot in every 150 makes a soft bubble sound as it appears, with random timing and loudness. The cannon fires
for 6 seconds, long enough to light the whole letter at once for 4 seconds; then it stops, and the last dots finish the
letter and leave the frame just before the video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter v, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: One Mirror
    """
    passes = [[(L, T), (0.0, B), (R, T)]]


class WShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter W With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter W in a 13-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The W has four diagonals, with its middle peak at full height.
The whole letter is drawn in one pass that turns at three mirrors. Outside the letter's box a dark veil dims the beam as
it comes in and goes out. The dots move at speed 7, 280 per second, 2,241 in total. Each new dot is a slightly different
color, moving through blue, teal, green, yellow, orange, red, pink and purple, so the letter is drawn in changing hues.
Roughly one dot in every 150 makes a soft bubble sound as it appears, with random timing and loudness. The cannon fires
for 8 seconds, long enough to light the whole letter at once for 4 seconds; then it stops, and the last dots finish the
letter and leave the frame just before the video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter w, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Three Mirrors
    """
    passes = [[(L, T), (-0.75, B), (0.0, T), (0.75, B), (R, T)]]


class XShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter X With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter X in a 13-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The X is two crossing diagonals. The letter is drawn in two
straight passes. Between passes the beam leaves the frame, where two hidden mirrors turn it around and send it back for
the next stroke; every stroke on the letter itself is a straight line with no mirror on it. Outside the letter's box a
dark veil dims the hidden mirrors and the beam's detours, so you can still follow them. The dots move at speed 7, 280
per second, 2,241 in total. Each new dot is a slightly different color, moving through blue, teal, green, yellow,
orange, red, pink and purple, so the letter is drawn in changing hues. Roughly one dot in every 150 makes a soft bubble
sound as it appears, with random timing and loudness. The cannon fires for 8 seconds, long enough to light the whole
letter at once for 4 seconds; then it stops, and the last dots finish the letter and leave the frame just before the
video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter x, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Two Mirrors
    """
    passes = [[(L, T), (R, B)], [(L, B), (R, T)]]


class YShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter Y With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter Y in a 19-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The Y is a wide V with a stem below it. The letter is drawn in
two straight passes. Between passes the beam leaves the frame, where three hidden mirrors turn it around and send it
back for the next stroke, and one mirror sits on the letter itself. The stem ends on the mirror at the point of the V,
so the beam bounces straight back and retraces the whole letter in reverse before it leaves the way it came in, which
makes this the longest letter of the alphabet. Outside the letter's box a dark veil dims the hidden mirrors and the
beam's detours, so you can still follow them. The dots move at speed 7, 280 per second, 3,081 in total. Each new dot is
a slightly different color, moving through blue, teal, green, yellow, orange, red, pink and purple, so the letter is
drawn in changing hues. Roughly one dot in every 150 makes a soft bubble sound as it appears, with random timing and
loudness. The cannon fires for 11 seconds, long enough to light the whole letter at once for 4 seconds; then it stops,
and the last dots finish the letter and leave the frame just before the video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter y, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Four Mirrors
    """
    passes = [[(L, 1.6), (0.0, -0.2), (R, 1.6)], [(0.0, B), (0.0, -0.2)]]


class ZShortLight(LetterShortLight):
    """
Title:
A Wide Beam of Dots Draws the Letter Z With Mirrors

Description:
A wide beam of dots bounces off mirrors and draws the whole letter Z in a 11-second vertical Short, holds it, then
switches off and drains away.

The beam is 0.8 wide and the dots are spread across it on a bell curve, so every stroke is dense in the middle and soft
at the edges. The letter fills a box 3 wide and 4 tall. The Z is a top bar, a diagonal and a bottom bar. The whole
letter is drawn in one pass that turns at two mirrors. Outside the letter's box a dark veil dims the beam as it comes in
and goes out. The dots move at speed 7, 280 per second, 1,961 in total. Each new dot is a slightly different color,
moving through blue, teal, green, yellow, orange, red, pink and purple, so the letter is drawn in changing hues. Roughly
one dot in every 150 makes a soft bubble sound as it appears, with random timing and loudness. The cannon fires for 7
seconds, long enough to light the whole letter at once for 4 seconds; then it stops, and the last dots finish the letter
and leave the frame just before the video ends, so it loops cleanly.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the mirrors: the angle of incidence equals the angle of reflection. The mirror
positions and angles are computed from the strokes the beam should follow, each dot's starting position is drawn with
NumPy from a fixed seed, and the exact moment each dot meets a mirror is found by bisection.

#shorts #alphabet #manim

Tags:
letter z, alphabet, mirror reflection, wide beam, normal distribution, ray reflection, mirrors, light simulation,
particle stream, manim, python, simulation, physics visualization, shorts

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Two Mirrors
    """
    passes = [[(L, T), (R, T), (L, B), (R, B)]]


del BoundaryScene, LetterShortLight
