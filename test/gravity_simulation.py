from manim import *

config = {
    'fast': {'gravity_constant': 0.00001, 'speed': 0.009},
    'medium': {'gravity_constant': 0.0000051, 'speed': 0.0045},
    'slow': {'gravity_constant': 0.0000002, 'speed': 0.001}
}


class Planet(Dot):
    def __init__(self, mass: float, speed: np.ndarray, **kwargs):
        self.mass = mass
        self.speed = speed
        super().__init__(radius=mass ** 0.1 * 0.05 + 0.01, **kwargs)

    def move(self):
        self.shift(self.speed)

class StaticPlanet(Planet):
        def __init__(self, mass: float, speed: np.ndarray, **kwargs):
            super().__init__(mass, speed, **kwargs)

        def move(self):
            pass


class GravitySimulation(VGroup):
    def __init__(
            self,
            *planets: Planet,
            gravity_constant: float = 0.0000002,
            speed: float = 0.001,
            acceleration_law=lambda m, r: m / r ** 2,
            **kwargs
    ):
        super().__init__(*planets, **kwargs)
        for item in planets:
            item.speed *= speed
        self.acceleration_law = acceleration_law
        self.planets = planets
        self.gravity_constant = gravity_constant

    def simulate(self, frames_count: int, frame_duration: float = 0.09) -> AnimationGroup:
        animations = []
        init_centers = [p.copy() for p in self.planets]
        for f in range(frames_count):
            for p1 in self.planets:
                for p2 in self.planets:
                    if p1 == p2:
                        continue
                    p1_center = p1.get_center_of_mass()
                    p2_center = p2.get_center_of_mass()

                    r = np.linalg.norm(p1_center - p2_center)
                    dv = ((p2_center - p1_center) / r)
                    p1.speed += dv * self.gravity_constant * self.acceleration_law(p2.mass, r)

            animations.append(
                AnimationGroup(
                    *[p.animate(rate_functions=running_start, run_time=frame_duration).move() for p in self.planets]
                )
            )
            for p in self.planets:
                p.move()

        for j in range(len(init_centers)):
            self.planets[j].move_to(init_centers[j])

        return Succession(
            *animations,
            lag_ratio=frame_duration
        )


class Simulation(Scene):
    def construct(self):
        planets = [
            Planet(1, UP * 10).move_to(LEFT * 2).set_color(RED),
            Planet(1, UP * 2).move_to(LEFT * 4).set_color(BLUE),
            Planet(1, DOWN * 5).move_to(RIGHT * 4).set_color(GREEN),
            Planet(1, LEFT * 10).move_to(DOWN * 2).set_color(YELLOW),
            StaticPlanet(1000, ORIGIN),
        ]
        self.play(
            Write(MathTex(r"g=\frac{m}{r^{2}}").to_corner(UP + LEFT)),
            GravitySimulation(*planets, **config['medium']).simulate(3000, 0.1)
        )


class SimulationRLinear(Scene):
    def construct(self):
        planets = [
            Planet(1, UP * 6).move_to(LEFT * 3).set_color(BLUE),
            StaticPlanet(1000, ORIGIN).move_to(ORIGIN).set_color(YELLOW)
        ]
        tr = TracedPath(planets[0].get_center)
        self.add(tr)
        self.play(
            Write(MathTex(r"g=\frac{m}{r}").to_corner(UP + LEFT)),
            GravitySimulation(*planets, **config['fast'], acceleration_law=lambda m, r: m / r).simulate(180, 0.1)
        )


class SimulationRNormal(Scene):
    def construct(self):
        planets = [
            Planet(1, UP * 6).move_to(LEFT * 3).set_color(BLUE),
            StaticPlanet(1000, ORIGIN).move_to(ORIGIN).set_color(YELLOW)
        ]
        tr = TracedPath(planets[0].get_center)
        self.add(tr)
        self.play(
            Write(MathTex(r"g=\frac{m}{r^{2}}").to_corner(UP + LEFT)),
            GravitySimulation(*planets, **config['fast'], acceleration_law=lambda m, r: m / r ** 2).simulate(2000, 0.1)
        )


class SimulationRTriple(Scene):
    def construct(self):
        planets = [
            Planet(1, UP * 3.7).move_to(LEFT * 3).set_color(BLUE),
            StaticPlanet(1000, ORIGIN).move_to(ORIGIN).set_color(YELLOW)
        ]
        tr = TracedPath(planets[0].get_center)
        self.add(tr)
        self.play(
            Write(MathTex(r"g=\frac{m}{r^{3}}").to_corner(UP + LEFT)),
            GravitySimulation(*planets, **config['fast'], acceleration_law=lambda m, r: m / r ** 3).simulate(3000, 0.1)
        )


class ThumbNail(Scene):
    def construct(self):
        planets = [
            Planet(1, UP * 7.185).move_to(LEFT * 4).set_color(BLUE),
            StaticPlanet(1000, ORIGIN).move_to(LEFT * 2).set_color(YELLOW),
            StaticPlanet(1000, ORIGIN).move_to(RIGHT * 2).set_color(YELLOW),
        ]
        tr = TracedPath(planets[0].get_center)
        self.add(tr)
        self.play(
            GravitySimulation(*planets, **config['fast']).simulate(3000, 0.1)
        )
