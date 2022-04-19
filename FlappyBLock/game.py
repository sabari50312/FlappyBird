import pygame
from random import randint
#CONSTANTS
WIDTH, HEIGHT = 4 00, 600  #Screen height and width
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  #Pygame surface object
P_HEIGHT = 38  #Player height DO NOT CHANGE
P_WIDTH = 54  #Player width DO NOT CHANGE
BGCOLOR = (20, 200, 200)  #Background color
VELOCITY = 12  #Initial downwards velocity
FPS = 65  #FPS duh
BIRD_SIZE = (P_WIDTH, P_HEIGHT)  #DO NOT CHANGE
BIRD_IMG = pygame.image.load("birb.png").convert_alpha()  #Player image
JUMP_HEIGHT = 7  #Jump height Feel free to experiment though 7 works pretty well
GRAV = 0.9  #Gravity value Feel free to experiment though 0.9 works pretty well


#The blocks class
class obstacles:

    def __init__(self, width, gap, velocity):
        self.x = WIDTH + width - 20
        self.width = width
        self.velocity = velocity
        self.height1 = randint(90, 400)
        self.height2 = (HEIGHT - gap) - self.height1

    def move(self):
        self.x -= self.velocity

    def draw(self):
        pygame.draw.rect(WIN, (10, 200, 50),
                         (self.x, 0, self.width, self.height1))
        pygame.draw.rect(
            WIN, (10, 200, 50),
            (self.x, HEIGHT - self.height2, self.width, self.height2))


#The birdy class
class player:

    def __init__(self, x, y):
        self.jumpcount = JUMP_HEIGHT
        self.isjump = False
        self.velocity = VELOCITY
        self.neg = 1
        self.rect = pygame.Rect(P_WIDTH, P_HEIGHT, x, y)

    def draw(self):
        WIN.blit(BIRD_IMG,
                 (self.rect.x, self.rect.y))  #Draw the birdy on screen

    def grav(self):
        self.rect.y += self.velocity  #Move bird down
        self.velocity += GRAV  #Accelerate bird


#All draw function calls
def draw_window():
    WIN.fill(BGCOLOR)
    bird.draw()
    block.draw()
    pygame.display.update()


#The jump function. Yes it only handles jumping. Yes jumping is a lil complicated
def jump_handler():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        bird.isjump = True
    if bird.isjump:
        bird.velocity = 0
        if bird.jumpcount >= -1 * JUMP_HEIGHT:
            if bird.jumpcount >= 0:
                bird.neg = 1
            else:
                bird.neg = -0.2
            bird.rect.y -= (bird.jumpcount**2 * bird.neg)
            bird.jumpcount -= 1
        else:
            bird.jumpcount = JUMP_HEIGHT
            bird.isjump = False
            bird.velocity = VELOCITY


#Function to make everything stay ON the screen. If it works dont fix it
def boundaries_handler():
    global run
    if block.x < -block.width:
        block.__init__(100, 190, 4)

    if bird.rect.y <= 0:
        bird.rect.y = 1
    if bird.rect.y > HEIGHT:
        run = False


#Function that handles collisions. Mess with this to enable noclip :)
def collision_handler():
    x = bird.rect.x
    y = bird.rect.y


#Variables
clock = pygame.time.Clock()
block = obstacles(100, 190, 4)
bird = player(100, HEIGHT / 2)
run = True

#MAIN
while (run):
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    bird.grav()
    block.move()
    #collision_handler()
    jump_handler()
    boundaries_handler()
    draw_window()

pygame.quit()
