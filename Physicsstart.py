import pygame
import time
import math
from pygame import gfxdraw

WIDTH, HEIGHT = 900, 500
global start
global stop
global vectormovetime
global vectormovestop
global ismoving
ismoving = True
start = time.time()
stop = 0.0
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("engine")

FPS = 60


b = []

def draw_window():
    WIN.fill((0, 0, 0))
    
    for x in range(len(b)):
        b[x].update()
        
    pygame.display.update()

class shape(pygame.Surface):
    def __init__(self, width, height, xspeed, yspeed, angleval, points):
        self.points = points
        a = [(0, 0)] * len(self.points)
        self.points2 = a
        self.width = width
        self.height = height
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.ismoving = True
        self.rolling = False
        self.angleval = angleval
        self.velocity = 0
      #  self.radius = int(math.sqrt(2 * math.pow(self.width / 2, 2)))
        self.radius = int(self.width / 2)
        totalx = 0
        totaly = 0
        self.center = (totalx, totaly)
    def update(self):
        for e in range(len(self.points2)):
            self.points2[e] = (self.points[e][0] + self.center[0], self.points[e][1] + self.center[1])
        rotate_thing()
        #for e in range(len(self.points2)):
         #   pygame.gfxdraw.circle(WIN, int(self.center[0]), int(self.center[1]), self.radius, (240, 240, 20))
        pygame.gfxdraw.polygon(WIN, self.points2, (30, 144, 255))

def gravity(x):
    if (math.fabs(b[x].yspeed) > 0):
        b[x].ismoving = True
    if (b[x].ismoving):
        if (b[x].center[1] < HEIGHT - (b[x].radius)):
            b[x].velocity = math.sqrt(math.pow(b[x].xspeed, 2) + math.pow(b[x].yspeed, 2))
            b[x].rolling = False
            stop = time.time()
            b[x].yspeed = b[x].yspeed + (9.8 * (stop - start))

def mouseclick():
    for r in range(len(b)):
        print("clicking")
        pygame.event.get()
        if  pygame.mouse.get_pos()[0] < (b[r].center[0] + (b[r].width / 2)) and pygame.mouse.get_pos()[0] > (b[r].center[0] - (b[r].width / 2 )) and pygame.mouse.get_pos()[1] > (b[r].center[1] - (b[r].width / 2)) and pygame.mouse.get_pos()[1] < b[r].center[1] + (b[r].width / 2):
            global start
            global stop
            global vectormovetime
            global vectormovestop
            global colliding
            print("within")
            colliding = False
            b[r].ismoving = True
            queueX = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[0]]
            queueY = [pygame.mouse.get_pos()[1], pygame.mouse.get_pos()[1], pygame.mouse.get_pos()[1], pygame.mouse.get_pos()[1], pygame.mouse.get_pos()[1]]
            start = time.time()
            vectormovetime = time.time()
            while (pygame.mouse.get_pressed() == (1, 0, 0)):
                b[r].xspeed = 0
                b[r].yspeed = 0
                vectormovestop = time.time()
                if (vectormovestop - vectormovetime > 1/60):
                    vectormovetime = time.time()
                    for e in range(len(b)):
                        if (e != r):
                            collidingwall(e)
                            gravity(e)
                            vectorMovement(e)
                pygame.event.get()
                b[r].center = pygame.mouse.get_pos()
                draw_window()
                stop = time.time()
                if (stop - start) > 0.02:
                    Yspeed = (pygame.mouse.get_pos()[1])
                    Xspeed = (pygame.mouse.get_pos()[0])
                    queueX.append(Xspeed)
                    queueX.pop(0)
                    queueY.append(Yspeed)
                    queueY.pop(0)
                    start = time.time()
                b[r].xspeed = queueX[len(queueX) - 1] - queueX[0]
                b[r].yspeed = queueY[len(queueY) - 1] - queueY[0]
            draw_window()
            queueX.clear
            queueY.clear
            start = time.time()

def isMoving(r):
    if b[r].xspeed != 0 or b[r].yspeed != 0:
        return True

global colliding
def collidingwall(r):
    print("b[r].yspeed", b[r].yspeed)
    if (b[r].radius + b[r].center[0]) > (WIDTH - 2):
        b[r].angleval = b[r].angleval * -1
        b[r].angleval += b[r].velocity
        print("hitting right")
        b[r].center = (b[r].center[0] - 10, b[r].center[1]) 
        b[r].xspeed = b[r].xspeed * -.9
    if (b[r].center[0] - b[r].radius) < 2:
        b[r].angleval = b[r].angleval * -1
        b[r].angleval -= b[r].velocity
        print("hitting left")
        b[r].center = (b[r].center[0] + 10, b[r].center[1]) 
        b[r].xspeed = b[r].xspeed * -.9
    if (b[r].center[1] > HEIGHT - (b[r].radius + 2) and math.fabs(b[r].yspeed) > 0):
      #  b[r].angleval = b[r].angleval
        b[r].angleval -= b[r].velocity
        if (math.fabs(b[r].yspeed * .3)  < 3):
            b[r].ismoving = False
            print("should stop")
            if (math.fabs(b[r].xspeed) > 0):
       #         b[r].velocity = b[r].velocity * -.01
                b[r].rolling = True
            b[r].yspeed = 0
            if (math.fabs(b[r].xspeed) < 20):
                b[r].xspeed = 0
        b[r].center = (b[r].center[0], b[r].center[1] - 2)
        b[r].yspeed = b[r].yspeed * -.9
    for othershapes in range(len(b)):
        if (othershapes != r):
            if math.fabs(b[r].center[0] - b[othershapes].center[0]) < (b[r].radius + b[othershapes].radius) and math.fabs(b[r].center[1] - b[othershapes].center[1]) < (b[r].radius + b[othershapes].radius):
                b[r].yspeed = (b[r].yspeed + b[othershapes].yspeed) * .9
                b[r].xspeed = (b[r].xspeed + b[othershapes].xspeed) * .9
                b[othershapes].yspeed = (b[r].yspeed + b[othershapes].yspeed) * -.9
                b[othershapes].xspeed = (b[r].xspeed + b[othershapes].xspeed) * -.9

    

def rotate_point(point, angle, center_point=(0, 0)):

    angle_rad = math.radians(angle % 360)
    # Shift the point so that center_point becomes the origin
    new_point = (point[0] - center_point[0], point[1] - center_point[1])
    new_point = (new_point[0] * math.cos(angle_rad) - new_point[1] * math.sin(angle_rad),
                 new_point[0] * math.sin(angle_rad) + new_point[1] * math.cos(angle_rad))
    # Reverse the shifting we have done
    new_point = (new_point[0] + center_point[0], new_point[1] + center_point[1])
    return new_point

def vectorMovement(r):
    if (isMoving(r)):
        gravity(r)
        b[r].center = (b[r].center[0] + .03 * b[r].xspeed, b[r].center[1] + .03 * b[r].yspeed)
        if (b[r].rolling):
            b[r].xspeed = b[r].xspeed * .5
            if (b[r].xspeed < 3):
                b[r].xspeed = 0


def rotate_thing():
    for r in range(len(b)):
        if isMoving(r):
            for a in range(len(b[r].points2)):
                if (b[r].angleval > 0):
                    b[r].angleval -= 1
                if (b[r].angleval < 0):
                    b[r].angleval += 1
                if (b[r].angleval < .2 and b[r].angleval > -.2):
                    b[r].angleval = 0
                b[r].points2[a] = rotate_point(b[r].points2[a], b[r].angleval, b[r].center)


def main():
    a = shape(30, 30, 0, 0, 30, [(-15, -15), (15, -15), (15, 15), (-15, 15)])
    a.center = (100, 100)
    c = shape(30, 30, 0, 0, 30, [(-15, -15), (15, -15), (15, 15), (-15, 15)])
    c.center = (200, 200)
    b.append(a)
    b.append(c)
   # d = shape(30, 30, 0, 0, 30, [(-15, -15), (15, -15), (15, 15), (-15, 15)])
    #b.append(d)
    run = True
    global colliding
    colliding = False
    clock = pygame.time.Clock() 
    global start
    start = time.time()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseclick()
        for x in range(len(b)):
            collidingwall(x)
            gravity(x)
            vectorMovement(x)

        draw_window()
    
    pygame.quit()

if __name__ == "__main__":
    main()


