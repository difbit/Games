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

energy_loss = False
e_amount = 100
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

def random_number():
    return random.choice((2, -2))

def main():
    pygame.time.set_timer(USEREVENT+2, RATE_OF_PARTICLES)
    PARTICLE_STASH = []
    for i in range(0, 2, 2):
        PARTICLE_STASH.append(Particle(
            int(WIDTH / 2),
            int(HEIGHT / 2),
            SPEED,
            random_angle(),
            get_color()
            ))

    while True:
        checkForKeyPress()
        DISPLAYSURF.fill(BGCOLOR)
        for event in pygame.event.get():
            if event.type == USEREVENT+2:
                PARTICLE_STASH.append(Particle(
                    int(WIDTH / 2),
                    int(HEIGHT / 2),
                    SPEED,
                    random_angle(),
                    get_color()
                    ))
        FONT_POSI = pygame.font.Font('freesansbold.ttf', 24)
        show_posi = FONT_POSI.render('Number of particles: %r' % \
        (len(PARTICLE_STASH)), True, GREY)

        DISPLAYSURF.blit(show_posi, (HEIGHT / 2, 15))

        elapsed = fps_clock.tick(FPS)
        sec = elapsed / 1000.0

        for partic in PARTICLE_STASH:
            partic.move(sec)
            partic.draw()
        fps_clock.tick(FPS)
        pygame.display.update()


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
