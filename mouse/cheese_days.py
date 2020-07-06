import pygame, sys
from pygame.locals import *
import random
import math


"""Move mouse with arrow keys and stop
with spacebar. Collect 25 cheese to win
the game.
"""

pygame.init()

FPS = 70
fps_clock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((800, 600), pygame.FULLSCREEN, 32)
pygame.display.set_caption('Mice like cheese')
# Mouse cursor set invisible
pygame.mouse.set_visible(False)

# RGB values for colors
BGCOLOR = (255, 138,  30)
BLACK   = (  0,   0,   0)
GREEN   = (112, 250,  58)
BLUE    = ( 94,  83, 225)
YELLOW  = (255, 242,   0)
GOLD    = (255, 215,  14)
GRAY    = (128, 128, 128)
D_GREEN = ( 76, 153,   0)

cosine_function = []
cosine = []

for i in range(-10, 11):
    cosine_function.append(2*i)
for i in range(0, 20):
    cosine_function.append(cosine_function[20 - i])

for i in range(0, len(cosine_function)):
    cosine.append(10 * math.sin((cosine_function[i])*(math.pi/180)))

CURRENT_COSINE = 0

UP_CAT    = 'up_cat'
DOWN_CAT  = 'down_cat'
LEFT_CAT  = 'left_cat'
RIGHT_CAT = 'right_cat'

CAT_MOVES = (
            UP_CAT,
            DOWN_CAT,
            LEFT_CAT,
            RIGHT_CAT,
            )

def main():
    while True:
        # Main game loop
        WINNER = game()
        if WINNER:
            you_win_screen()
        else:
            game_over_screen()


def game():
    WINNER = False
    # Create three cats and one mouse
    cat_1 = game_cat(200, 200, RIGHT_CAT, 1, GREEN)
    cat_2 = game_cat(400, 400, DOWN_CAT, 1, GREEN)
    fast_cat = game_cat(400, 400, DOWN_CAT, 3, D_GREEN)
    mouse = MouseObject(15, 15)

    # Score shows how much cheese have been grabbed
    SCORE      = 0
    RIGHTLIMIT = 730
    LEFTLIMIT  = 0
    UPLIMIT    = 10
    DOWNLIMIT  = 530

    movingDown  = False
    movingUp    = False
    movingRight = False
    movingLeft  = False

    SPEED_CAT  = False
    ANIMATE    = True
    NEW_CHEESE = True

    while True:
        # Fill surface with BGCOLOR
        DISPLAYSURF.fill(BGCOLOR)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    movingDown  = False
                    movingUp    = False
                    movingRight = True
                    movingLeft  = False
                elif event.key == K_DOWN:
                    movingDown  = True
                    movingUp    = False
                    movingRight = False
                    movingLeft  = False
                elif event.key == K_LEFT:
                    movingDown  = False
                    movingUp    = False
                    movingRight = False
                    movingLeft  = True
                elif event.key == K_UP:
                    movingDown  = False
                    movingUp    = True
                    movingRight = False
                    movingLeft  = False
                # Spacebar stops the mouse
                elif event.key == K_SPACE:
                    movingDown  = False
                    movingUp    = False
                    movingRight = False
                    movingLeft  = False

        # The mouse will move up if UPLIMIT has not been reached
        if movingUp and mouse.y_coord != UPLIMIT:
            mouse.y_coord -= 5
            if mouse.y_coord == UPLIMIT:
                movingUp = False
                # No more moving up
                mouse.y_coord -= 0
        elif movingDown and mouse.y_coord != DOWNLIMIT:
            mouse.y_coord += 5
            if mouse.y_coord == DOWNLIMIT:
                movingDown = False
                mouse.y_coord += 0
        elif movingRight and mouse.x_coord != RIGHTLIMIT:
            mouse.x_coord += 5
            if mouse.x_coord == RIGHTLIMIT:
                movingRight = False
                mouse.x_coord += 0
        elif movingLeft and mouse.x_coord != LEFTLIMIT:
            mouse.x_coord -= 5
            if mouse.x_coord == LEFTLIMIT:
                movingLeft = False
                mouse.x_coord -= 0

        if NEW_CHEESE:
            CHEESE_BLIT = cheese_position()
            NEW_CHEESE = False

        # Make cheese appear
        cheese_pop(CHEESE_BLIT)

        # 'Grab' the cheese
        if abs(mouse.x_coord - CHEESE_BLIT['x']) < 70 \
                and abs(mouse.y_coord - CHEESE_BLIT['y']) < 70:
            # Make more cheese
            NEW_CHEESE = True
            SCORE += 1

        if SCORE >= 15:
            FONT_NICE = pygame.font.Font('freesansbold.ttf', 25)
            nice_score = FONT_NICE.render('Nice!!', True, BLACK)
            DISPLAYSURF.blit(nice_score, (680, 45))
            # This prevents player hitting the cat near (400, 400)
            if abs(mouse.x_coord - 400) >80 and abs(mouse.y_coord - 400) >80:
                SPEED_CAT = True
            else:
                pass

        if SCORE >= 25:
            WINNER = True
            return WINNER

        FONT_SCORE = pygame.font.Font('freesansbold.ttf', 25)
        score_surface = FONT_SCORE.render('Score: %r' % SCORE, True, BLACK)
        DISPLAYSURF.blit(score_surface, (680, 25))

        if (abs(mouse.x_coord - cat_1.catx - 30) < 60 and
                abs(mouse.y_coord - cat_1.caty - 30) < 60)        \
            or (abs(mouse.x_coord - cat_2.catx - 30) < 60 and
                abs(mouse.y_coord - cat_2.caty - 30) < 60)        \
            or ((abs(mouse.x_coord  - fast_cat.catx) < 50 and
                abs(mouse.y_coord - fast_cat.caty) < 50)
                and SPEED_CAT):
            return WINNER

        # New value from cosine list
        animation()

        cheese_position()

        cat_1.move()
        cat_2.move()

        mouse.draw_mouse()
        cat_1.draw()
        cat_2.draw()
        if SPEED_CAT:
            fast_cat.move()
            fast_cat.draw()

        pygame.display.update()
        fps_clock.tick(FPS)
        checkForKeyPress()


def cheese_position():
    # Create dictionary for x-coordinate and y-coordinate
    # which values are random
    return {'x': random.randint(75, 710), 'y': random.randint(75, 525)}


def game_over_screen():
    FONT_FOR_OVER = pygame.font.Font('freesansbold.ttf', 50)
    FONT_START = pygame.font.Font('freesansbold.ttf', 20)
    game_over = FONT_FOR_OVER.render('GAME OVER', True, BLACK)
    play_again = FONT_START.render('Press enter to play again', True, BLACK)
    # Game over text is blitted to the screen surface
    DISPLAYSURF.blit(game_over, (250, 250))
    DISPLAYSURF.blit(play_again, (280, 300))
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    pygame.event.get()
                    main()


def you_win_screen():
    # This is played when the needed score is reached
    FONT_WIN = pygame.font.Font('freesansbold.ttf', 40)
    FONT_START = pygame.font.Font('freesansbold.ttf', 20)
    you_win = FONT_WIN.render('YOU WIN! THE CHEESE IS YOURS!!', True, BLACK)
    play_again = FONT_START.render('Press enter to play again', True, BLACK)
    DISPLAYSURF.blit(you_win, (50, 250))
    pygame.display.update()
    pygame.time.wait(2000)
    DISPLAYSURF.blit(play_again, (280, 300))
    pygame.display.update()
    pygame.time.wait(500)
    WINNER = False
    checkForKeyPress()
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    pygame.event.get()
                    main()


def cheese_pop(posit):
    # Position for cheese object
    RANDOM_X = posit['x']
    RANDOM_Y = posit['y']
    # Create cheese object
    cheese_for_mouse = CheeseObject(RANDOM_X, RANDOM_Y)
    # Draw cheese object
    cheese_for_mouse.draw_cheese()


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


def animation():
    # This function determines which value from cosine list is used
    global CURRENT_COSINE
    CURRENT_COSINE += 1
    if CURRENT_COSINE == len(cosine):
        CURRENT_COSINE = 0


class game_cat(object):

    def __init__(self, catx, caty, cat_direction, speed, fur):
        self.catx = catx
        self.caty = caty
        self.cat_direction = cat_direction
        # Speed (scalar) too can be modified
        self.speed = speed
        self.fur = fur

    def draw(self):
        # Draw torso
        pygame.draw.ellipse(DISPLAYSURF, self.fur, (self.catx + 30,
        self.caty + 43, 60, 40), 0)
        # Draw head
        pygame.draw.circle(DISPLAYSURF, self.fur, (self.catx + 40,
        self.caty + 37), 17, 0)
        # Draw left ear
        pygame.draw.polygon(DISPLAYSURF, self.fur, ((self.catx + 20,
        self.caty + 10), (self.catx + 37, self.caty + 25),
        (self.catx + 27, self.caty + 35)), 0)
        # Draw right ear
        pygame.draw.polygon(DISPLAYSURF, self.fur, ((self.catx + 60,
        self.caty + 10), (self.catx + 30, self.caty + 35),
        (self.catx + 51, self.caty + 33)), 0)
        # Draw whiskers
        pygame.draw.line(DISPLAYSURF, GRAY, (self.catx + 7,
        self.caty + 30), (self.catx + 32, self.caty + 37), 1)
        pygame.draw.line(DISPLAYSURF, GRAY, (self.catx + 7,
        self.caty + 35), (self.catx + 32, self.caty + 38), 1)
        pygame.draw.line(DISPLAYSURF, GRAY, (self.catx + 7,
        self.caty + 40), (self.catx + 32, self.caty + 39), 1)
        pygame.draw.line(DISPLAYSURF, GRAY, (self.catx + 67,
        self.caty + 30), (self.catx + 42, self.caty + 37), 1)
        pygame.draw.line(DISPLAYSURF, GRAY, (self.catx + 67,
        self.caty + 35), (self.catx + 42, self.caty + 38), 1)
        pygame.draw.line(DISPLAYSURF, GRAY, (self.catx + 67,
        self.caty + 40), (self.catx + 42, self.caty + 39), 1)
        # Draw left eye
        pygame.draw.circle(DISPLAYSURF, BLACK, (self.catx + 32,
        self.caty + 30), 2, 0)
        # Draw right eye
        pygame.draw.circle(DISPLAYSURF, BLACK, (self.catx + 42,
        self.caty + 30), 2, 0)
        # Draw mouth
        pygame.draw.line(DISPLAYSURF, BLACK, (self.catx + 36,
        self.caty + 38), (self.catx + 30, self.caty + 42), 2)
        pygame.draw.line(DISPLAYSURF, BLACK, (self.catx + 36,
        self.caty + 38), (self.catx + 43, self.caty + 42), 2)
        # Draw nose
        pygame.draw.circle(DISPLAYSURF, BLACK, (self.catx + 37,
        self.caty + 37), 3, 0)
        # Draw legs and use cosine list for animation
        pygame.draw.line(DISPLAYSURF, self.fur, (self.catx + 37,
        self.caty + 71), ((self.catx + 34) + cosine[CURRENT_COSINE],
        self.caty + 102), 6)
        pygame.draw.line(DISPLAYSURF, self.fur, (self.catx + 50,
        self.caty + 78), ((self.catx + 50) - cosine[CURRENT_COSINE],
        self.caty + 109), 6)
        pygame.draw.line(DISPLAYSURF, self.fur, (self.catx + 69,
        self.caty + 65), ((self.catx + 66) + cosine[CURRENT_COSINE],
        self.caty + 97), 6)
        pygame.draw.line(DISPLAYSURF, self.fur, (self.catx + 82,
        self.caty + 72), ((self.catx + 82) - cosine[CURRENT_COSINE],
        self.caty + 103), 6)
        # Draw tail
        pygame.draw.lines(DISPLAYSURF, self.fur, False, ((self.catx + 82,
        self.caty + 57), (self.catx + 100, self.caty + 50),
        (self.catx + 109, self.caty + 40), (self.catx + 120,
        self.caty + 20)), 6)

    def move(self):
        # Constants to restrict movement
        RIGHTLIMIT = 710
        LEFTLIMIT = 0
        UPLIMIT = 0
        DOWNLIMIT = 490
        if self.cat_direction == RIGHT_CAT and self.catx != RIGHTLIMIT:
            CAT_RANDOM_RIGHT = random.choice(range(self.catx, RIGHTLIMIT))
            if self.catx+5 < CAT_RANDOM_RIGHT:
                self.catx += self.speed
            else:
                self.cat_direction = random.choice(CAT_MOVES)
        elif self.cat_direction == DOWN_CAT and self.caty != DOWNLIMIT:
            CAT_RANDOM_DOWN = random.choice(range(self.caty, DOWNLIMIT))
            if self.caty+5 < CAT_RANDOM_DOWN:
                self.caty += self.speed
            else:
                self.cat_direction = random.choice(CAT_MOVES)
        elif self.cat_direction == LEFT_CAT and self.catx != LEFTLIMIT:
            CAT_RANDOM_LEFT = random.choice(range(LEFTLIMIT, self.catx))
            if self.catx-5 > CAT_RANDOM_LEFT:
                self.catx -= self.speed
            else:
                self.cat_direction = random.choice(CAT_MOVES)
        elif self.cat_direction == UP_CAT and self.caty != UPLIMIT:
            CAT_RANDOM_UP = random.choice(range(UPLIMIT, self.caty))
            if self.caty-5 > CAT_RANDOM_UP:
                self.caty -= self.speed
            else:
                self.cat_direction = random.choice(CAT_MOVES)


class MouseObject(object):
    def __init__(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord

    def draw_mouse(self):
        # Draw torso
        pygame.draw.ellipse(DISPLAYSURF, BLUE, (self.x_coord + 30,
        self.y_coord + 17, 23, 37), 0)
        # Draw head
        pygame.draw.circle(DISPLAYSURF, BLUE, (self.x_coord + 41,
        self.y_coord + 10), 10, 0)
        # Draw left ear
        pygame.draw.circle(DISPLAYSURF, BLUE, (self.x_coord + 32,
        self.y_coord), 6, 0)
        # Draw right ear
        pygame.draw.circle(DISPLAYSURF, BLUE, (self.x_coord + 47,
        self.y_coord), 6, 0)
        # Draw nose
        pygame.draw.polygon(DISPLAYSURF, BLUE, ((self.x_coord + 35,
        self.y_coord + 4), (self.x_coord + 55, self.y_coord + 13),
        (self.x_coord + 37, self.y_coord + 17)), 0)

        # Draw hands
        pygame.draw.line(DISPLAYSURF, BLUE, (self.x_coord + 41
        , self.y_coord + 29), (self.x_coord \
        + 62, self.y_coord + 22 + cosine[CURRENT_COSINE]), 4)
        pygame.draw.line(DISPLAYSURF, BLUE, (self.x_coord + 41
        , self.y_coord + 29), (self.x_coord \
        + 20, self.y_coord + 22 - cosine[CURRENT_COSINE]), 4)
        # Draw legs
        pygame.draw.line(DISPLAYSURF, BLUE, (self.x_coord + 41,
        self.y_coord + 43), (self.x_coord + 53 - cosine[CURRENT_COSINE],
        self.y_coord + 63 + cosine[CURRENT_COSINE]), 4)
        pygame.draw.line(DISPLAYSURF, BLUE, (self.x_coord + 41,
        self.y_coord + 43), (self.x_coord + 29 - cosine[CURRENT_COSINE],
        self.y_coord + 63 - cosine[CURRENT_COSINE]), 4)
        # Draw tail
        pygame.draw.lines(DISPLAYSURF, BLUE, False, ((self.x_coord + 45,
        self.y_coord + 47),
        (self.x_coord + 25, self.y_coord + 42), (self.x_coord + 19,
        self.y_coord + 40), (self.x_coord + 8, self.y_coord + 37),
        (self.x_coord, self.y_coord + 27)), 4)
        # Draw eyes
        pygame.draw.circle(DISPLAYSURF, BLACK, (self.x_coord + 38,
        self.y_coord + 8), 2, 0)
        pygame.draw.circle(DISPLAYSURF, BLACK, (self.x_coord + 45,
        self.y_coord + 8), 2, 0)


class CheeseObject(object):

    def __init__(self, x_coord, y_coord):
        # Coordinates of cheese
        self.x_coord = x_coord
        self.y_coord = y_coord

    def draw_cheese(self):
        pygame.draw.polygon(DISPLAYSURF, YELLOW, ((self.x_coord,
        self.y_coord + 30), (self.x_coord + 27, self.y_coord),
        (self.x_coord + 70, self.y_coord + 10), (self.x_coord + 68,
        self.y_coord + 35), (self.x_coord + 3, self.y_coord + 50)), 0)
        # Draw edges
        pygame.draw.polygon(DISPLAYSURF, GOLD, ((self.x_coord,
        self.y_coord + 30), (self.x_coord + 27, self.y_coord),
        (self.x_coord + 70, self.y_coord + 10), (self.x_coord,
        self.y_coord + 30), (self.x_coord + 3, self.y_coord + 50),
        (self.x_coord + 68, self.y_coord + 35), (self.x_coord + 70,
        self.y_coord + 10)), 3)
        # Draw hole into cheese
        pygame.draw.circle(DISPLAYSURF, GOLD, (self.x_coord + 10,
        self.y_coord + 34), 7, 2)
        pygame.draw.circle(DISPLAYSURF, GOLD, (self.x_coord + 25,
        self.y_coord + 36), 6, 2)
        pygame.draw.circle(DISPLAYSURF, GOLD, (self.x_coord + 50,
        self.y_coord + 27), 9, 2)
        pygame.draw.circle(DISPLAYSURF, GOLD, (self.x_coord + 47,
        self.y_coord + 11), 6, 2)
        pygame.draw.circle(DISPLAYSURF, GOLD, (self.x_coord + 28,
        self.y_coord + 13), 5, 2)


if __name__=='__main__':
    main()
