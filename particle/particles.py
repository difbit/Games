import pygame, sys
import random
from pygame.locals import *

FPS = 90
fps_clock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, 32)
pygame.display.set_caption('Particles')
pygame.mouse.set_visible(False)

BGCOLOR = (255, 138,  30)
GREEN   = (112, 250,  58)
GREY    = (128, 128, 128)

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

def random_number():
    return random.choice((2, -2))

def main():
    pygame.init()
    pygame.time.set_timer(USEREVENT+1, 100)
    PARTICLE_STASH = []
    for i in range(0, 2, 2):
        PARTICLE_STASH.append(Particle(640, 330, random_number(), \
        random_number()))

    while True:
        checkForKeyPress()
        DISPLAYSURF.fill(BGCOLOR)
        for event in pygame.event.get():
            if event.type == USEREVENT+1:
                PARTICLE_STASH.append(Particle(640, 330, \
                random_number(), random_number()))
        FONT_POSI = pygame.font.Font('freesansbold.ttf', 16)
        show_posi = FONT_POSI.render('Number of particles: %r' % \
        (len(PARTICLE_STASH)), True, GREY)

        DISPLAYSURF.blit(show_posi, (960, 15))

        for partic in PARTICLE_STASH:
            partic.move()
            partic.draw()
        fps_clock.tick(FPS)
        pygame.display.update()

class Particle(object):
    def __init__(self, posx, posy, right_speed, down_speed):
        self.posx = posx
        self.posy = posy
        self.right_speed = right_speed
        self.down_speed = down_speed

    def draw(self):
        pygame.draw.circle(DISPLAYSURF, GREEN, (self.posx, \
        self.posy), 5, 0)

    def move(self):
        self.posx += self.right_speed
        self.posy += self.down_speed
        if self.posx > 1275:
            self.right_speed = -2
        elif self.posy > 715:
            self.down_speed = -2
        elif self.posx < 5:
            self.right_speed = 2
        elif self.posy < 5:
            self.down_speed = 2

if __name__ == "__main__":
    main()
