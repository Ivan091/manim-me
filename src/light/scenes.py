from manim import (
    BLACK,
    BLUE,
    GREEN,
    LEFT,
    ORANGE,
    PI,
    PINK,
    PURPLE,
    RED,
    RIGHT,
    TAU,
    TEAL,
    UP,
    YELLOW,
    Rectangle,
    Scene,
)

from light.boundaries import (
    Boundary,
    CircleBoundary,
    EllipseBoundary,
    MirrorPath,
    PolygonBoundary,
    RingBoundary,
    StadiumBoundary,
    cross,
    regular_polygon,
    star,
)
from light.cannon import Cannon, RadialCannon, StreamCannon
from light.coloring import Gradient, Palette
from light.lettering import vertical_math_path
from light.world import World


class BoundaryScene(Scene):
    simulation_time: int = 15
    boundary: Boundary
    cannon: Cannon = RadialCannon()
    points_radius: float = 0.017

    def construct(self) -> None:
        world = World(self.boundary, self.cannon, self.simulation_time)
        self.add(world.to_mobject(self.points_radius))
        self.wait(self.simulation_time)


class CircleLight(BoundaryScene):
    """
Title:
Light Bouncing Inside a Circle (Off-Center Source)

Description:
5,760 points of light start from one spot inside a circle and bounce off its wall for 15 seconds. The source is
off-center, so the pattern is not symmetric.

The circle has radius 2 and the source sits one third of the radius above the center. The points leave in 5,760 evenly
spaced directions at speed 1.3. The directions pointing left are blue and the directions pointing right are orange, so
you can follow where each half of the light ends up.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the wall: the angle of incidence equals the angle of reflection. The
simulation is vectorised with NumPy, so all 5,760 points advance together every frame, and the exact moment each point
meets the wall is found by bisection.

#manim #simulation #math

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
    cannon = RadialCannon(
        origin=UP * (2 / 3),
        coloring=Palette([1, 1], start_angle=PI / 2),
    )


class HexagonLight(BoundaryScene):
    """
Title:
Light Bouncing Inside a Hexagon

Description:
5,760 points of light start at the center of a regular hexagon and bounce off its walls for 15 seconds.

The hexagon has a circumradius of 2 and the source sits at its center. The points leave in 5,760 evenly spaced
directions at speed 1.3. The directions are split into six equal 60-degree sectors, one color each, so you can follow
where every sector of the light travels.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the wall: the angle of incidence equals the angle of reflection. The
simulation is vectorised with NumPy, so all 5,760 points advance together every frame, and the exact moment each point
meets the wall is found by bisection.

#manim #simulation #math

Tags:
hexagon billiard, polygon billiard, mathematical billiards, dynamical billiards, reflection, light simulation, manim,
python, simulation, mathematics, physics visualization

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Six Colors
    """

    # vertices on the x-axis, so half-width = R
    boundary = PolygonBoundary(regular_polygon(6, 2.0))
    cannon = RadialCannon(coloring=Palette([1, 1, 1, 1, 1, 1]))


class StarLight(BoundaryScene):
    """
Title:
Light Bouncing Inside a Five-Pointed Star

Description:
5,760 points of light start at the center of a five-pointed star and bounce around its concave walls for 15 seconds.

The star has an outer radius of 2.1 and an inner radius of 0.92, so its tips span about 4 units across, and the source
sits at its center. The points leave in 5,760 evenly spaced directions at speed 1.3. The directions are split into five
equal 72-degree sectors, one color each.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the wall: the angle of incidence equals the angle of reflection. The
simulation is vectorised with NumPy, so all 5,760 points advance together every frame, and the exact moment each point
meets the wall is found by bisection.

#manim #simulation #math

Tags:
star billiard, non-convex billiard, mathematical billiards, dynamical billiards, reflection, light simulation, manim,
python, simulation, mathematics, physics visualization

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Five Colors
    """

    # widest tips at ±outer·cos(18°) ≈ ±0.951·outer, so outer = 2.1 gives ±2.0
    boundary = PolygonBoundary(star(5, 2.1, 0.92))
    cannon = RadialCannon(
        coloring=Palette(
            [1, 1, 1, 1, 1], start_angle=PI / 2 - TAU / 10 - TAU / 5
        ),
    )


class CrossLight(BoundaryScene):
    """
Title:
Light Bouncing Inside a Cross-Shaped Room

Description:
5,760 points of light start at the center of a cross-shaped room and bounce off its walls for 15 seconds.

Each arm of the cross is 1.06 wide and reaches 2 units from the center, where the source sits. The points leave in 5,760
evenly spaced directions at speed 1.3. Each of the four colors covers the directions that point toward one arm.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the wall: the angle of incidence equals the angle of reflection. The
simulation is vectorised with NumPy, so all 5,760 points advance together every frame, and the exact moment each point
meets the wall is found by bisection.

#manim #simulation #math

Tags:
cross billiard, non-convex billiard, mathematical billiards, dynamical billiards, reflection, light simulation, manim,
python, simulation, mathematics, physics visualization

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Four Colors
    """

    boundary = PolygonBoundary(cross(0.53, 2.0))
    cannon = RadialCannon(
        coloring=Palette([1, 1, 1, 1], start_angle=-PI / 4),
    )


class EllipseLight(BoundaryScene):
    """
Title:
Light Bouncing Inside an Ellipse, Starting at a Focus

Description:
5,760 points of light start at one focus of an ellipse and bounce off its wall for 15 seconds.

The ellipse is 4 wide and 6 tall, and the source sits at its bottom focus. The points leave in 5,760 evenly spaced
directions at speed 1.3. A ray that leaves one focus of an ellipse reflects through the other focus, so watch the points
gather there.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the wall: the angle of incidence equals the angle of reflection. The
simulation is vectorised with NumPy, so all 5,760 points advance together every frame, and the exact moment each point
meets the wall is found by bisection.

#manim #simulation #math

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
    cannon = RadialCannon(
        origin=boundary.foci[0],  # bottom focus, (0, -2.236)
    )


class StadiumLight(BoundaryScene):
    """
Title:
Light Bouncing Inside a Stadium Shape

Description:
5,760 points of light start at the center of a stadium shape (two half circles joined by straight walls) and bounce off
its walls for 15 seconds.

The stadium is 4 wide and 1.7 tall: a straight segment of half-length 1.15 inflated by a radius of 0.85. The points
leave in 5,760 evenly spaced directions at speed 1.3. The quarter of the directions that point right is blue and the
remaining three quarters are orange.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the wall: the angle of incidence equals the angle of reflection. The
simulation is vectorised with NumPy, so all 5,760 points advance together every frame, and the exact moment each point
meets the wall is found by bisection.

#manim #simulation #math

Tags:
stadium billiard, bunimovich stadium, mathematical billiards, dynamical billiards, reflection, light simulation, manim,
python, simulation, mathematics, physics visualization

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Stadium Billiard
    """

    boundary = StadiumBoundary((0, 0), 1.15, 0.85)  # width 2·(1.15+0.85)=4.0
    cannon = RadialCannon(
        coloring=Palette([1, 3], start_angle=-PI / 4)
    )


class RingLight(BoundaryScene):
    """
Title:
Light Bouncing Between Two Circles: Annular Billiard

Description:
5,760 points of light start inside a ring and bounce off both the outer wall and the inner disc for 15 seconds.

The ring lies between circles of radius 2 and 0.67, and the inner disc is an obstacle. The source sits in the middle of
the band, 1.33 from the center. The points leave in 5,760 evenly spaced directions at speed 1.3.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the wall: the angle of incidence equals the angle of reflection. The
simulation is vectorised with NumPy, so all 5,760 points advance together every frame, and the exact moment each point
meets the wall is found by bisection.

#manim #simulation #math

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
    cannon = RadialCannon(origin=RIGHT * 1.33)  # mid-band


class MathShortLight(BoundaryScene):
    simulation_time = 20
    letter_half_width = 1.0
    visible_half_width = letter_half_width + 0.05
    word_path = vertical_math_path(half_width=letter_half_width)
    boundary = MirrorPath(word_path)
    cannon = StreamCannon(
        origin=word_path[0],
        velocity=2,
        spawn_rate=15.0,
        coloring=Gradient(
            (BLUE, TEAL, GREEN, YELLOW, ORANGE, RED, PINK, PURPLE)
        ),
    )
    points_radius = 0.025

    def construct(self) -> None:
        for side in (LEFT, RIGHT):
            curtain = Rectangle(
                width=10,
                height=10,
                fill_color=BLACK,
                fill_opacity=1,
                stroke_width=0,
            )
            curtain.next_to(side * self.visible_half_width, side, buff=0)
            self.add_foreground_mobjects(curtain)
        super().construct()


del BoundaryScene
