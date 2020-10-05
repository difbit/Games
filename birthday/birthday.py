import pygame, sys
from pygame.locals import *
import random
import math


"""Move turtle with arrow keys and stop
with spacebar. Collect 25 cake to win
the game.
"""

pygame.init()

FPS = 70
fps_clock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((800, 600), pygame.FULLSCREEN, 32)
pygame.display.set_caption('Turtles like cake')
# turtle cursor set invisible
pygame.mouse.set_visible(False)

# RGB values for colors
# BGCOLOR = (255, 138,  30)
BGCOLOR = ( 34,  13, 140)
BLACK   = (  0,   0,   0)
GREEN   = (112, 250,  58)
BROWN   = (142,  20,  28)
FIRE    = (242,  20,  28)
T_GREEN = ( 80, 150,  37)
BLUE    = ( 94,  83, 225)
W_BLUE  = ( 94,  73, 215)
BGCOLOR = ( 34,  13, 140)
YELLOW  = (255, 242,   0)
GOLD    = (255, 215,  14)
GRAY    = (128, 128, 128)
D_GREEN = ( 76, 133,  10)

cosine_function = []
cosine = []

for i in range(-10, 11):
    cosine_function.append(2*i)
for i in range(0, 20):
    cosine_function.append(cosine_function[20 - i])

for i in range(0, len(cosine_function)):
    cosine.append(10 * math.sin((cosine_function[i])*(math.pi/180)))

CURRENT_COSINE = 0

UP_whale    = 'up_whale'
DOWN_whale  = 'down_whale'
LEFT_whale  = 'left_whale'
RIGHT_whale = 'right_whale'

whale_MOVES = (
            UP_whale,
            DOWN_whale,
            LEFT_whale,
            RIGHT_whale,
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
    # Create three whales and one turtle
    whale_1 = game_whale(200, 200, RIGHT_whale, 1, W_BLUE)
    whale_2 = game_whale(400, 400, DOWN_whale, 1, W_BLUE)
    fast_whale = game_whale(400, 400, DOWN_whale, 3, D_GREEN)
    turtle = TurtleObject(15, 15)

    # Score shows how much cake have been grabbed
    SCORE      = 0
    RIGHTLIMIT = 730
    LEFTLIMIT  = 0
    UPLIMIT    = 10
    DOWNLIMIT  = 530

    movingDown  = False
    movingUp    = False
    movingRight = False
    movingLeft  = False

    SPEED_whale  = False
    ANIMATE    = True
    NEW_cake = True

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
                # Spacebar stops the turtle
                elif event.key == K_SPACE:
                    movingDown  = False
                    movingUp    = False
                    movingRight = False
                    movingLeft  = False

        # The turtle will move up if UPLIMIT has not been reached
        if movingUp and turtle.y_coord != UPLIMIT:
            turtle.y_coord -= 5
            if turtle.y_coord == UPLIMIT:
                movingUp = False
                # No more moving up
                turtle.y_coord -= 0
        elif movingDown and turtle.y_coord != DOWNLIMIT:
            turtle.y_coord += 5
            if turtle.y_coord == DOWNLIMIT:
                movingDown = False
                turtle.y_coord += 0
        elif movingRight and turtle.x_coord != RIGHTLIMIT:
            turtle.x_coord += 5
            if turtle.x_coord == RIGHTLIMIT:
                movingRight = False
                turtle.x_coord += 0
        elif movingLeft and turtle.x_coord != LEFTLIMIT:
            turtle.x_coord -= 5
            if turtle.x_coord == LEFTLIMIT:
                movingLeft = False
                turtle.x_coord -= 0

        if NEW_cake:
            cake_BLIT = cake_position()
            NEW_cake = False

        # Make cake appear
        cake_pop(cake_BLIT)

        # 'Grab' the cake
        if abs(turtle.x_coord - cake_BLIT['x']) < 70 \
                and abs(turtle.y_coord - cake_BLIT['y']) < 70:
            pygame.time.wait(100)
            # Make more cake
            NEW_cake = True
            SCORE += 1

        if SCORE >= 10:
            DISPLAYSURF.fill(GREEN)

        if SCORE >= 7:
            FONT_NICE = pygame.font.Font('freesansbold.ttf', 25)
            nice_score = FONT_NICE.render('Hienoa!!', True, BLACK)
            DISPLAYSURF.blit(nice_score, (680, 45))
            # This prevents player hitting the whale near (400, 400)
            if abs(turtle.x_coord - 400) >80 and abs(turtle.y_coord - 400) >80:
                SPEED_whale = True
            else:
                pass

        FONT_SCORE = pygame.font.Font('freesansbold.ttf', 25)
        score_surface = FONT_SCORE.render('Kakut: %r' % SCORE, True, BLACK)
        DISPLAYSURF.blit(score_surface, (680, 25))

        if (abs(turtle.x_coord - whale_1.whalex - 30) < 60 and
                abs(turtle.y_coord - whale_1.whaley - 30) < 60)        \
            or (abs(turtle.x_coord - whale_2.whalex - 30) < 60 and
                abs(turtle.y_coord - whale_2.whaley - 30) < 60)        \
            or ((abs(turtle.x_coord  - fast_whale.whalex) < 50 and
                abs(turtle.y_coord - fast_whale.whaley) < 50)
                and SPEED_whale):
            pygame.time.wait(500)
            return WINNER

        # New value from cosine list
        animation()

        cake_position()

        whale_1.move()
        whale_2.move()

        turtle.draw_turtle()
        whale_1.draw()
        whale_2.draw()
        if SPEED_whale:
            fast_whale.move()
            fast_whale.draw()

        pygame.display.update()
        fps_clock.tick(FPS)
        checkForKeyPress()

        if SCORE >= 10:
            WINNER = True
            pygame.time.wait(700)
#             pygame.time.wait(700)
            return WINNER


def cake_position():
    # Create dictionary for x-coordinate and y-coordinate
    # which values are random
    return {'x': random.randint(75, 710), 'y': random.randint(75, 525)}


def game_over_screen():
    FONT_FOR_OVER = pygame.font.Font('freesansbold.ttf', 50)
    FONT_START = pygame.font.Font('freesansbold.ttf', 20)
    game_over = FONT_FOR_OVER.render('GAME OVER', True, BLACK)
    play_again = FONT_START.render('Paina "enter" pelataksesi uudestaan', True, BLACK)
    # Game over text is blitted to the screen surface
    DISPLAYSURF.blit(game_over, (250, 250))
    DISPLAYSURF.blit(play_again, (230, 300))
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
    you_win = FONT_WIN.render('PALJON ONNEA MIKAEL 10 VUOTTA!!!', True, BLACK)
    play_again = FONT_START.render('Paina "enter" pelataksesi uudestaan', True, BLACK)
    DISPLAYSURF.blit(you_win, (28, 250))
    pygame.display.update()
    pygame.time.wait(2000)
    DISPLAYSURF.blit(play_again, (240, 300))
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


def cake_pop(posit):
    # Position for cake object
    RANDOM_X = posit['x']
    RANDOM_Y = posit['y']
    # Create cake object
    cake_for_turtle = cakeObject(RANDOM_X, RANDOM_Y)
    # Draw cake object
    cake_for_turtle.draw_cake()


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


class game_whale(object):

    def __init__(self, whalex, whaley, whale_direction, speed, fur):
        self.whalex = whalex
        self.whaley = whaley
        self.whale_direction = whale_direction
        # Speed (scalar) too can be modified
        self.speed = speed
        self.fur = fur

    def draw(self):
        # Draw torso
        pygame.draw.ellipse(DISPLAYSURF, self.fur, (self.whalex + 30,
        self.whaley + 41, 65, 43), 0)
        # Draw head
        pygame.draw.ellipse(DISPLAYSURF, self.fur, (self.whalex + 15,
        self.whaley + 46, 50, 30), 0)
        # Draw left eye
        pygame.draw.circle(DISPLAYSURF, BLACK, (self.whalex + 35,
        self.whaley + 68), 1, 0)
        # Draw right eye
        pygame.draw.circle(DISPLAYSURF, BLACK, (self.whalex + 35,
        self.whaley + 52), 1, 0)
        # Draw mouth
        pygame.draw.line(DISPLAYSURF, BLACK, (self.whalex + 15,
        self.whaley + 60), (self.whalex + 21, self.whaley + 51), 1)
        pygame.draw.line(DISPLAYSURF, BLACK, (self.whalex + 15,
        self.whaley + 60), (self.whalex + 21, self.whaley + 69), 1)
        # Draw arms
        pygame.draw.line(DISPLAYSURF, self.fur, (self.whalex + 41,
        self.whaley + 63), ((self.whalex + 63) + 1.8*cosine[CURRENT_COSINE],
        self.whaley + 91 + 0.6*cosine[CURRENT_COSINE]), 14)
        pygame.draw.line(DISPLAYSURF, self.fur, (self.whalex + 41,
        self.whaley + 63), ((self.whalex + 63) + 1.8*cosine[CURRENT_COSINE],
        self.whaley + 35 - 0.6*cosine[CURRENT_COSINE]), 14)
        # Draw lower torso
        pygame.draw.polygon(DISPLAYSURF, self.fur, ((self.whalex + 85,
        self.whaley + 50), (self.whalex + 105, self.whaley + 55),
        (self.whalex + 105, self.whaley + 70), (self.whalex + 85,
        self.whaley + 75)), 0)
        # Draw whale tail
        pygame.draw.polygon(DISPLAYSURF, self.fur, ((self.whalex + 90,
        self.whaley + 61), (self.whalex + 125, self.whaley + 45),
        (self.whalex + 103, self.whaley + 71)), 0)
        pygame.draw.polygon(DISPLAYSURF, self.fur, ((self.whalex + 90,
        self.whaley + 63), (self.whalex + 125, self.whaley + 80),
        (self.whalex + 103, self.whaley + 54)), 0)

    def move(self):
        # Constants to restrict movement
        RIGHTLIMIT = 710
        LEFTLIMIT = 0
        UPLIMIT = 0
        DOWNLIMIT = 490
        if self.whale_direction == RIGHT_whale and self.whalex != RIGHTLIMIT:
            whale_RANDOM_RIGHT = random.choice(range(self.whalex, RIGHTLIMIT))
            if self.whalex+5 < whale_RANDOM_RIGHT:
                self.whalex += self.speed
            else:
                self.whale_direction = random.choice(whale_MOVES)
        elif self.whale_direction == DOWN_whale and self.whaley != DOWNLIMIT:
            whale_RANDOM_DOWN = random.choice(range(self.whaley, DOWNLIMIT))
            if self.whaley+5 < whale_RANDOM_DOWN:
                self.whaley += self.speed
            else:
                self.whale_direction = random.choice(whale_MOVES)
        elif self.whale_direction == LEFT_whale and self.whalex != LEFTLIMIT:
            whale_RANDOM_LEFT = random.choice(range(LEFTLIMIT, self.whalex))
            if self.whalex-5 > whale_RANDOM_LEFT:
                self.whalex -= self.speed
            else:
                self.whale_direction = random.choice(whale_MOVES)
        elif self.whale_direction == UP_whale and self.whaley != UPLIMIT:
            whale_RANDOM_UP = random.choice(range(UPLIMIT, self.whaley))
            if self.whaley-5 > whale_RANDOM_UP:
                self.whaley -= self.speed
            else:
                self.whale_direction = random.choice(whale_MOVES)


class TurtleObject(object):
    def __init__(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord

    def draw_turtle(self):
        # Draw torso
        pygame.draw.ellipse(DISPLAYSURF, T_GREEN, (self.x_coord + 25,
        self.y_coord + 17, 33, 37), 0)
        # Draw head
        pygame.draw.ellipse(DISPLAYSURF, T_GREEN, (self.x_coord + 34,
        self.y_coord, 15, 34), 0)
        # Draw hands
        pygame.draw.line(DISPLAYSURF, T_GREEN, (self.x_coord + 41
        , self.y_coord + 29), (self.x_coord \
        + 62, self.y_coord + 22 + cosine[CURRENT_COSINE]), 4)
        pygame.draw.line(DISPLAYSURF, T_GREEN, (self.x_coord + 41
        , self.y_coord + 29), (self.x_coord \
        + 20, self.y_coord + 22 - cosine[CURRENT_COSINE]), 4)
        # Draw legs
        pygame.draw.line(DISPLAYSURF, T_GREEN, (self.x_coord + 41,
        self.y_coord + 43), (self.x_coord + 53 - cosine[CURRENT_COSINE],
        self.y_coord + 63 + cosine[CURRENT_COSINE]), 4)
        pygame.draw.line(DISPLAYSURF, T_GREEN, (self.x_coord + 41,
        self.y_coord + 43), (self.x_coord + 29 - cosine[CURRENT_COSINE],
        self.y_coord + 63 - cosine[CURRENT_COSINE]), 4)
        # Draw tail
        pygame.draw.lines(DISPLAYSURF, T_GREEN, False, ((self.x_coord + 37,
        self.y_coord + 51),
        (self.x_coord + 41,
        self.y_coord + 57), (self.x_coord + 45, self.y_coord + 51),
        ), 4)
        # Draw eyes
        pygame.draw.circle(DISPLAYSURF, BLACK, (self.x_coord + 38,
        self.y_coord + 8), 2, 0)
        pygame.draw.circle(DISPLAYSURF, BLACK, (self.x_coord + 45,
        self.y_coord + 8), 2, 0)


class cakeObject(object):

    def __init__(self, x_coord, y_coord):
        # Coordinates of cake
        self.x_coord = x_coord
        self.y_coord = y_coord

    def draw_cake(self):
        C_COLOR = GRAY
        F_COLOR = FIRE
        pygame.draw.ellipse(DISPLAYSURF, BROWN, (self.x_coord + 10,
        self.y_coord + 13, 40, 15), 0)
        pygame.draw.ellipse(DISPLAYSURF, BROWN, (self.x_coord + 10,
        self.y_coord + 33, 40, 15), 0)
        pygame.draw.ellipse(DISPLAYSURF, GOLD, (self.x_coord + 10,
        self.y_coord + 33, 40, 15), 2)
        pygame.draw.rect(DISPLAYSURF, BROWN, (self.x_coord + 10,
        self.y_coord + 23, 40, 17), 0)
        pygame.draw.ellipse(DISPLAYSURF, GOLD, (self.x_coord + 10,
        self.y_coord + 13, 40, 15), 2)
        # First row of candles
        pygame.draw.line(DISPLAYSURF, C_COLOR, (
            self.x_coord + 19,
            self.y_coord + 18),
           (self.x_coord + 19,
            self.y_coord + 8), 2)
        pygame.draw.line(DISPLAYSURF, C_COLOR, (
            self.x_coord + 25,
            self.y_coord + 18),
           (self.x_coord + 25,
            self.y_coord + 8), 2)
        pygame.draw.line(DISPLAYSURF, C_COLOR, (
            self.x_coord + 30,
            self.y_coord + 18),
           (self.x_coord + 30,
            self.y_coord + 8), 2)
        pygame.draw.line(DISPLAYSURF, C_COLOR, (
            self.x_coord + 35,
            self.y_coord + 18),
           (self.x_coord + 35,
            self.y_coord + 8), 2)
        pygame.draw.line(DISPLAYSURF, C_COLOR, (
            self.x_coord + 40,
            self.y_coord + 18),
           (self.x_coord + 40,
            self.y_coord + 8), 2)
        # Fire
        pygame.draw.ellipse(DISPLAYSURF, F_COLOR, (
            self.x_coord + 18,
            self.y_coord + 2, 4, 8), 0)
        pygame.draw.ellipse(DISPLAYSURF, F_COLOR, (
            self.x_coord + 24,
            self.y_coord + 2, 4, 8), 0)
        pygame.draw.ellipse(DISPLAYSURF, F_COLOR, (
            self.x_coord + 29,
            self.y_coord + 2, 4, 8), 0)
        pygame.draw.ellipse(DISPLAYSURF, F_COLOR, (
            self.x_coord + 34,
            self.y_coord + 2, 4, 8), 0)
        pygame.draw.ellipse(DISPLAYSURF, F_COLOR, (
            self.x_coord + 39,
            self.y_coord + 2, 4, 8), 0)
        # Second row of candles
        pygame.draw.line(DISPLAYSURF, C_COLOR, (
            self.x_coord + 16,
            self.y_coord + 22),
           (self.x_coord + 16,
            self.y_coord + 12), 2)
        pygame.draw.line(DISPLAYSURF, C_COLOR, (
            self.x_coord + 22,
            self.y_coord + 22),
           (self.x_coord + 22,
            self.y_coord + 12), 2)
        pygame.draw.line(DISPLAYSURF, C_COLOR, (
            self.x_coord + 27,
            self.y_coord + 22),
           (self.x_coord + 27,
            self.y_coord + 12), 2)
        pygame.draw.line(DISPLAYSURF, C_COLOR, (
            self.x_coord + 32,
            self.y_coord + 22),
           (self.x_coord + 32,
            self.y_coord + 12), 2)
        pygame.draw.line(DISPLAYSURF, C_COLOR, (
            self.x_coord + 37,
            self.y_coord + 22),
           (self.x_coord + 37,
            self.y_coord + 11), 2)
        # Fire
        pygame.draw.ellipse(DISPLAYSURF, F_COLOR, (
            self.x_coord + 15,
            self.y_coord + 8, 4, 8), 0)
        pygame.draw.ellipse(DISPLAYSURF, F_COLOR, (
            self.x_coord + 21,
            self.y_coord + 8, 4, 8), 0)
        pygame.draw.ellipse(DISPLAYSURF, F_COLOR, (
            self.x_coord + 26,
            self.y_coord + 8, 4, 8), 0)
        pygame.draw.ellipse(DISPLAYSURF, F_COLOR, (
            self.x_coord + 31,
            self.y_coord + 8, 4, 8), 0)
        pygame.draw.ellipse(DISPLAYSURF, F_COLOR, (
            self.x_coord + 36,
            self.y_coord + 8, 4, 8), 0)

if __name__=='__main__':
    main()
