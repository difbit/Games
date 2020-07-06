import pygame, sys
import random
from pygame.locals import *
import math
import ctypes
from sys import platform

pygame.init()

FPS = 60
fps_clock = pygame.time.Clock()
true_res = (0, 0)

# A hack for windows screens
if platform == "win32":
    ctypes.windll.user32.SetProcessDPIAware()
    true_res = (ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1))
DISPLAYSURF = pygame.display.set_mode(true_res, pygame.FULLSCREEN)
pygame.display.set_caption('Particles')
pygame.mouse.set_visible(False)

# BGCOLOR = (165, 118,  30)
BGCOLOR = (0, 0,  0)
GREEN   = (100, 170,  38)
GREY    = (128, 128, 128)

mass = 0
M = 0 # g/mol, molar mass
hydrogen = True
if hydrogen:
    M = 1.008 # g/mol
energy_loss = True
e_amount = 10
HEIGHT = DISPLAYSURF.get_height()
WIDTH = DISPLAYSURF.get_width()
SPEED = 200
RATE_OF_PARTICLES = 1000
# Boltzmann's constant
k = 1.3805 * 10**(-23) # J/K
# Avogadro's constant
N_a = 6.022 * 10**23 # l/mol
mass = M / N_a

"""
Formula for mass is derived from amount of substance, n:

    n = N / N_a     , where N = amount of particles

    n = m / M       , where m = mass and M = molar mass

So we get:

    N / N_a = m / M

Thus mass can be calculated by this formula:

    m = (N * M) / N_a

For one particle N = 1:

    m = M / N_a

Formula for temperature can be derived from this known formula:

    E_k = (3 / 2) * k * T       , where T = temperature and E_k is the
                                  average kinetic energy of particles
    T = (2 / 3) * (E_k / k)

Kinetic energy of one particle is the good old E = (1 / 2) * m * v**2
"""

def get_color():
    first = random.choice(range(50, 225))
    second = random.choice(range(50, 225))
    third = random.choice(range(50, 225))
    return (first, second, third)

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        pygame.quit()
        sys.exit()
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        pygame.quit()
        sys.exit()
    return keyUpEvents[0].key

def random_angle():
    return random.choice(range(1, 361, 2))

def main():
    pygame.time.set_timer(USEREVENT+2, RATE_OF_PARTICLES)
    PARTICLE_STASH = []
    while True:
        avg_velocity = 0
        checkForKeyPress()
        DISPLAYSURF.fill(BGCOLOR)

        p_info = generate_info_particles(
            PARTICLE_STASH, WIDTH, HEIGHT, SPEED)

        FONT_POSI = pygame.font.Font('freesansbold.ttf', 24)
        show_posi = FONT_POSI.render('Number of particles: %r' % \
        (len(PARTICLE_STASH)), True, GREY)
        DISPLAYSURF.blit(show_posi, (WIDTH / 2, 15))
        show_avg_velo = FONT_POSI.render('Average velocity: %r m/s' % \
        (p_info[0]), True, GREY)
        DISPLAYSURF.blit(show_avg_velo, (WIDTH / 2, 35))
        show_avg_kinet = FONT_POSI.render('Average kinetic energy: %r J' % \
        (p_info[1]), True, GREY)
        DISPLAYSURF.blit(show_avg_kinet, (WIDTH / 2, 55))
        show_temperature = FONT_POSI.render('Temperature: %r K' % \
        (p_info[2]), True, GREY)
        DISPLAYSURF.blit(show_temperature, (WIDTH / 2, 75))

        fps_clock.tick(FPS)
        pygame.display.update()


def generate_info_particles(stash, width, height, speed):
    """Creates particles and gives info about them"""
    velocities = 0
    avg_velocity = 0
    avg_kinetic = 0
    temperature = 0

    for event in pygame.event.get():
        if event.type == USEREVENT+2:
            stash.append(Particle(
                int(width / 2),
                int(height / 2),
                speed,
                random_angle(),
                get_color()
                ))

    fps_clock = pygame.time.Clock()
    elapsed = fps_clock.tick(60)
    sec = elapsed / 1000.0

    for partic in stash:
        velocities += partic.v
        partic.move(sec)
        partic.draw()

    if stash:
        avg_velocity = velocities / len(stash)
        # Average kinetic energy
        avg_kinetic = (1 / 2) * mass * avg_velocity**2
        temperature = (2 / 3) * (avg_kinetic / k)
    return avg_velocity, float(avg_kinetic), float(temperature)


def generate_particles(stash, width, height, speed):
    """General particle creator"""
    for event in pygame.event.get():
        if event.type == USEREVENT+2:
            stash.append(Particle(
                int(width / 2),
                int(height / 2),
                speed,
                random_angle(),
                get_color()
                ))

    fps_clock = pygame.time.Clock()
    elapsed = fps_clock.tick(60)
    sec = elapsed / 1000.0

    for partic in stash:
        partic.move(sec)
        partic.draw()


class Particle(object):

    def __init__(self, x, y, v, THETA, color):
        self.x = x
        self.y = y
        self.v = v
        self.THETA = THETA
        self.color = color

    def draw(self):
        pygame.draw.circle(DISPLAYSURF, self.color, (int(self.x), \
        int(self.y)), 3, 0)

    def move(self, sec):
        self.vx = self.v * math.cos(self.THETA * math.pi/180)
        self.vy = self.v * math.sin(self.THETA * math.pi/180)
        self.x = self.x + self.vx * sec
        self.y = self.y - self.vy * sec

        diff_angle = 90 - self.THETA

        add_angle = 360 - self.THETA
        if self.vx > 0:
            if (self.y <= -2 and self.vy > 0
            or self.y >= HEIGHT and self.vy < 0):
                self.THETA += 2 * add_angle
                if energy_loss:
                    self.v -= e_amount
        if self.vx < 0:
            if (self.y <= -2 and self.vy > 0
            or self.y >= HEIGHT and self.vy < 0):
                self.THETA += 2 * add_angle
                if energy_loss:
                    self.v -= e_amount

        if self.x <= 0:
            if self.vy < 0 or self.vy > 0:
                self.THETA += 2 * diff_angle
                if energy_loss:
                    self.v -= e_amount
        if self.x >= DISPLAYSURF.get_width():
            if self.vy < 0 or self.vy > 0:
                self.THETA += 2 * diff_angle
                if energy_loss:
                    self.v -= e_amount

if __name__ == "__main__":
    main()
