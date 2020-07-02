import pygame, sys
import random
from pygame.locals import *
import math

pygame.init()

FPS = 60
fps_clock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, 32)
pygame.display.set_caption('Particles')
pygame.mouse.set_visible(False)

# BGCOLOR = (165, 118,  30)
BGCOLOR = (0, 0,  0)
GREEN   = (100, 170,  38)
GREY    = (128, 128, 128)

energy_loss = True
e_amount = 10
HEIGHT = DISPLAYSURF.get_height()
WIDTH = DISPLAYSURF.get_width()
SPEED = 200
RATE_OF_PARTICLES = 100

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
        velocities = 0
        avg_velocity = 0
        checkForKeyPress()
        DISPLAYSURF.fill(BGCOLOR)

        generate_particles(PARTICLE_STASH, WIDTH, HEIGHT, SPEED)

        for partic in PARTICLE_STASH:
            velocities += partic.v
        if PARTICLE_STASH:
            avg_velocity = velocities / len(PARTICLE_STASH)

        FONT_POSI = pygame.font.Font('freesansbold.ttf', 24)
        show_posi = FONT_POSI.render('Number of particles: %r' % \
        (len(PARTICLE_STASH)), True, GREY)
        DISPLAYSURF.blit(show_posi, (WIDTH / 2, 15))
        show_avg_velo = FONT_POSI.render('Average velocity: %r' % \
        (avg_velocity), True, GREY)
        DISPLAYSURF.blit(show_avg_velo, (WIDTH / 2, 35))

        fps_clock.tick(FPS)
        pygame.display.update()

def generate_particles(stash, width, height, speed):
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
