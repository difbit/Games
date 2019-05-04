import pygame, sys
from pygame.locals import *
import random
import time

pygame.init()

FPS = 90
fps_clock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, 32)
pygame.mouse.set_visible(False)

GREEN = (  0, 255,   0)
BLACK = (  0,   0,   0)

def stars():
    letter = random.choice(["1","2","3"])
    index = random.randint(1,160)
    return letter,index

def check_for_key_presses():
    key_up_events = pygame.event.get(KEYUP)
    if len(key_up_events) == 0:
        return None
    if key_up_events[0].key == K_ESCAPE:
        pygame.quit()
        sys.exit()
    return key_up_events[0].key

class DisplayText(object):
    def __init__(self, y, string):
        self.y = y
        self.string = string

    def draw(self):
        FONT_STYLE = pygame.font.Font('freesansbold.ttf', 14)
        string_rendered = FONT_STYLE.render(self.string, True, GREEN)
        DISPLAYSURF.blit(string_rendered, (0, self.y))

    def move(self):
        if self.y == 700 or self.y == 701:
            self.y = 2
            self.string = text_generator()
        else:
            self.y += 2

    #def move_up(self):
    #    self.y -= 1

def text_generator():
    junk = []
    junk[:]
    i = 0
    while i < 450:
        i += 1
        junk.append(" ")
    junk[stars()[1]] = stars()[0]
    str = ' '.join(junk)
    return str

def main():
    TEXT_LIST = []
    for i in range(2, 702, 14):
        TEXT_LIST.append(DisplayText(i, text_generator()))
    TEXT_LIST[0].draw()
    while True:
        DISPLAYSURF.fill(BLACK)
        check_for_key_presses()
        for object in TEXT_LIST:
            object.move()
            object.draw()
        fps_clock.tick(FPS)
        pygame.display.update()

if __name__ == "__main__":
    main()
