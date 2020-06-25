import pygame, sys
from pygame.locals import *
import random
import math

pygame.init()

FPS = 60
fps_clock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, 32)
pygame.mouse.set_visible(True)

GRAY  = (128, 128, 128)
BLACK = (  0,   0,   0)
SPEED = 25
BALL_SPEED = 300

def main():
    elapsed = 0.
    bar_one = Bar(1800, 40, SPEED)
    bar_two = Bar(100, 40, SPEED)
    ball = Ball(400, 300, BALL_SPEED, 0, 0, 30)
    while True:
        DISPLAYSURF.fill(BLACK)

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

        elapsed = fps_clock.tick(FPS)
        sec = elapsed / 1000.0
        ball.draw()
        ball.play(sec)
        bar_one.play()
        bar_two.move()
        bar_one.draw()
        bar_two.draw()
        pygame.display.update()


class Bar(object):

    def __init__(self, x, y, v):
        self.x = x
        self.y = y
        self.v = v

    def draw(self):
        pygame.draw.rect(
            DISPLAYSURF, GRAY, ((self.x, self.y, 15, 130))
        )

    def move(self):
        self.y += self.v
        if self.y <= 0:
            self.v = SPEED
        elif self.y >= 950:
            self.v = -SPEED

    def play(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.y >= 10:
            self.y -= SPEED
        elif keys[pygame.K_DOWN] and self.y <= 940:
            self.y += SPEED


class Ball(object):

    def __init__(self, x, y, v, vx, vy, THETA):
        self.x = x
        self.y = y
        self.v = v
        self.THETA = THETA

    def draw(self):
        pygame.draw.rect(
            DISPLAYSURF, GRAY, ((self.x, self.y, 15, 15))
        )

    def play(self, sec):
        self.vx = self.v * math.cos(self.THETA * math.pi/180)
        self.vy = self.v * math.sin(self.THETA * math.pi/180)
        self.x = self.x + self.vx * sec
#         self.x = 0.001 * sec
        self.y = self.y + self.vy * sec
#         self.y = 0.001 * sec
#         if self.x >

        if self.y <= 0:
            self.vy = self.vy
        elif self.y >= 950:
            self.vy = -self.vy

        if self.x <= 5:
            self.vx = self.vx
        elif self.x >= 950:
            self.vx = -self.vx



if __name__=='__main__':
    main()
