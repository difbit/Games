import pygame, sys
from pygame.locals import *
import random
import math

pygame.init()

FPS = 70
fps_clock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, 32)
pygame.mouse.set_visible(True)

GRAY  = (128, 128, 128)
BLACK = (  0,   0,   0)

def main():
    bar_one = bar(1800, 40, 10)
    bar_two = bar(100, 40, 10)
    while True:
        DISPLAYSURF.fill(BLACK)

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

        bar_two.move()
        bar_one.draw()
        bar_two.draw()
        pygame.display.update()
        fps_clock.tick(FPS)


class bar(object):

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
            self.v = 10
        if self.y >= 950:
            self.v = -10


if __name__=='__main__':
    main()
