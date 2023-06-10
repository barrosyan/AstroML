import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT), OPENGL | DOUBLEBUF)
pygame.display.set_caption("Planet Simulation")

glClearColor(0.0, 0.0, 0.0, 1.0)

planet_list = []

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600 * 24  # 1 day

    def __init__(self, x, y, z, radius, color, mass):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0
        self.z_vel = 0

    def draw_sphere(self, radius):
        slices = 20
        stacks = 20

        for i in range(slices):
            lat0 = math.pi * (-0.5 + (i - 1) / slices)
            z0 = math.sin(lat0) * radius
            zr0 = math.cos(lat0) * radius

            lat1 = math.pi * (-0.5 + i / slices)
            z1 = math.sin(lat1) * radius
            zr1 = math.cos(lat1) * radius

            glBegin(GL_TRIANGLE_STRIP)
            for j in range(stacks + 1):
                lng = 2 * math.pi * (j - 1) / stacks
                x = math.cos(lng) * zr0
                y = math.sin(lng) * zr0
                glVertex3f(x, y, z0)

                x = math.cos(lng) * zr1
                y = math.sin(lng) * zr1
                glVertex3f(x, y, z1)
            glEnd()

    def draw(self):
        glColor3f(*self.color)

        if len(self.orbit) > 2:
            glBegin(GL_LINE_STRIP)
            for point in self.orbit:
                x, y, z = point
                glVertex3f(x, y, z)
            glEnd()

        glTranslatef(self.x, self.y, self.z)
        self.draw_sphere(self.radius)

    def attraction(self, other):
        other_x, other_y, other_z = other.x, other.y, other.z
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance_z = other_z - self.z
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2 + distance_z ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        phi = math.atan2(distance_z, math.sqrt(distance_x ** 2 + distance_y ** 2))
        force_x = math.cos(theta) * math.cos(phi) * force
        force_y = math.sin(theta) * math.cos(phi) * force
        force_z = math.sin(phi) * force
        return force_x, force_y, force_z

    def update_position(self, planets):
        total_fx = total_fy = total_fz = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy, fz = self.attraction(planet)
            total_fx += fx
            total_fy += fy
            total_fz += fz

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        self.z_vel += total_fz / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.z += self.z_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y, self.z))


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 0, 8, DARK_GREY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                run = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluPerspective(45, (WIDTH / HEIGHT), 0.1, 1000.0)
        gluLookAt(0, 0, 100, 0, 0, 0, 0, 1, 0)

        for planet in planets:
            planet.update_position(planets)
            planet.draw()

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
