import math
import pygame
import sys


def rotate_2d(pos, rad):
    x, y = pos
    # s and c are polar coordinates
    s, c = math.sin(rad), math.cos(rad)
    return x*c-y*s, y*c+x*s


class Cam:

    def __init__(self, pos=(0,0,0), rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot)

    def events(self, event):
        if event.type == pygame.MOUSEMOTION:
            x,y = event.rel
            x /= 200
            y /= 200

    def update(self, dt, key):
        s = dt*7

        # Y-axis
        if key[pygame.K_q]:
            self.pos[1]-=s
        if key[pygame.K_e]:
            self.pos[1]+=s

        # Polar coordinates
        x,y = s*math.sin(self.rot[1]),s*math.cos(self.rot[1])

        # Z-axis
        if key[pygame.K_w]:
            self.pos[2]+=s
        if key[pygame.K_s]:
            self.pos[2]-=s

        # X-axis
        if key[pygame.K_a]:
            self.pos[0]-=s
        if key[pygame.K_d]:
            self.pos[0]+=s

pygame.init()
w,h = 400,400
cx,cy = w//2,h//2
screen = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()

# verts = (-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1),
# edges = (0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)
verts = (-1,-1,-4),(1,-1,-4),(1, 1,-4),(-1, 1,-4),(-1,-1, 1),(1,-1, 1),(1, 1, 1),(-1, 1, 1),\
        (-0,-1, 3),(2,-1, 3),(2, 1, 3),(-0, 1, 3),(-0,-1, 5),(2,-1, 5),(2, 1, 5),(-0, 1, 5),\
        ( 2,-1, 3),(2,-1, 5),(2, 1, 5),( 2, 1, 3),\
        ( 4,-1, 3),(4,-1, 5),(4, 1, 5),( 4, 1, 3),#( 2,-1, 5),(4,-1, 5),(4, 1, 5),( 2, 1, 5)
        #( 2,-1, 5),(2,-1, 5),(2, 1, 5),( 2, 1, 5),
edges = ( 0, 1),( 1, 2),( 2, 3),( 3, 0),( 4, 5),( 5, 6),( 6, 7),( 7, 4),\
        ( 0, 4),( 1, 5),( 2, 6),( 3, 7),( 8, 9),( 9,10),(10,11),(11, 8),\
        ( 4, 8),( 5, 9),( 6,10),( 7,11),(12,13),(13,14),(14,15),(15,12),\
        ( 8,12),( 9,13),(10,14),(11,15),(16,17),(17,18),(18,19),(19,16),\
        (14,19),(14,18),(15,19),(16,20),(20,21),(21,22),(22,23),(23,20),
cam = Cam(pos=(0,0,-5))
radian = 0

pygame.event.get()
pygame.mouse.get_rel()
pygame.mouse.set_visible(1)
pygame.event.set_grab(1)

while True:
    dt = clock.tick()/1000

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        cam.events(event)

    screen.fill((155,255,255))

    for edge in edges:
        points = []

        # First one is x, second one is y
        for x,y,z in (verts[edge[0]],verts[edge[1]]):
            x-=cam.pos[0]
            y-=cam.pos[1]
            z-=cam.pos[2]

            x,z = rotate_2d((x,z), cam.rot[1])
            y,z = rotate_2d((y,z), cam.rot[0])

            f = 200/z
            x,y = x*f,y*f
            points+=[(cx+int(x),cy+int(y))]
        pygame.draw.line(screen, (0,0,0),points[0],points[1],1)
        # One circle is drawn at a time
        # (0,0,255) means blue colour
        pygame.draw.circle(screen, (0,0,255), (cx+int(x),cy+int(y)),5)

    pygame.display.flip()
    key = pygame.key.get_pressed()
    cam.update(dt, key)
