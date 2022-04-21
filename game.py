import pygame
from random import randint

pygame.init()

#CONSTANTS
WIDTH, HEIGHT = 500, 700  #Screen height and width
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  #Pygame surface object
P_HEIGHT = 38  #Player height DO NOT CHANGE
P_WIDTH = 54  #Player width DO NOT CHANGE
BGCOLOR = (255, 255, 255)  #Background color
RED = (255, 0, 0)
VELOCITY = 7  #Initial downwards velocity 7 works
FPS = 65  #FPS duh
BIRD_SIZE = (P_WIDTH, P_HEIGHT)  #DO NOT CHANGE
BIRD_IMG = pygame.image.load("birb.png").convert_alpha()  #Player image
JUMP_HEIGHT = 7  #Jump height Feel free to experiment though 7 works pretty well
GRAV = 0.8  #Gravity value Feel free to experiment though 0.8 works pretty well
BLOCK_WIDTH = 140  #180
BLOCK_GAP = 210  #210
BLOCK_VEL = 4  #4
my_font = pygame.font.SysFont('Comic Sans MS', 30)


#The blocks class
class obstacles:

    def __init__(self, width, gap, velocity):
        self.x = WIDTH + width - 20
        self.width = width
        self.velocity = velocity
        self.height1 = randint(90, 400)
        self.height2 = (HEIGHT - gap) - self.height1
        self.rect1 = pygame.Rect(self.x, 0, self.width, self.height1)
        self.rect2 = pygame.Rect(self.x, HEIGHT - self.height2, self.width,
                                 self.height2)

    def move(self):
        self.rect1.x -= self.velocity
        self.rect2.x -= self.velocity

    def draw(self):
        pygame.draw.rect(WIN, (10, 200, 50), self.rect1)
        pygame.draw.rect(WIN, (10, 200, 50), self.rect2)


#The birdy class
class player:

    def __init__(self, x, y):
        self.jumpcount = JUMP_HEIGHT
        self.isjump = False
        self.velocity = VELOCITY
        self.neg = 1
        self.rect = pygame.Rect(x, y, P_WIDTH, P_HEIGHT)
        self.score = 0
        self.score_updated = False

    def draw(self):
        pygame.draw.rect(WIN, (255, 0, 0), self.rect)
        WIN.blit(BIRD_IMG,
                 (self.rect.x, self.rect.y))  #Draw the birdy on screen

    def grav(self):
        self.rect.y += self.velocity  #Move bird down
        self.velocity += GRAV  #Accelerate bird


#All draw function calls
def draw_window():
    text_surface = my_font.render(str(bird.score), False, (0, 0, 0))

    WIN.fill(BGCOLOR)
    bird.draw()
    block.draw()
    WIN.blit(text_surface, dest=(WIDTH // 2, 30))

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
                bird.neg = -0.1
            bird.rect.y -= (bird.jumpcount**2 * bird.neg)
            bird.jumpcount -= 1
        else:
            bird.jumpcount = JUMP_HEIGHT
            bird.isjump = False
            bird.velocity = VELOCITY


#Function to make everything stay ON the screen. If it works dont fix it
def boundaries_handler():
    global run
    if block.rect1.x < -block.width:
        block.__init__(BLOCK_WIDTH, BLOCK_GAP, BLOCK_VEL)
        bird.score_updated = False

    if bird.rect.x > block.rect1.x + block.width and not bird.score_updated:
        bird.score += 1
        bird.score_updated = True

    if bird.rect.y < 0:
        bird.rect.y = 0

    if bird.rect.y > HEIGHT:
        run = False


#Function that handles collisions. Mess with this to enable noclip :)
def collision_handler():
    if pygame.Rect.colliderect(bird.rect, block.rect1):
        pygame.time.delay(500)
        pygame.quit()

    if pygame.Rect.colliderect(bird.rect, block.rect2):
        pygame.time.delay(500)
        pygame.quit()


#Variables
clock = pygame.time.Clock()
block = obstacles(BLOCK_WIDTH, BLOCK_GAP, BLOCK_VEL)
bird = player(100, HEIGHT / 2)
run = True

#MAIN
while (True):
    text1 = my_font.render("Press space to start", True, (255, 255, 255))
    text2 = my_font.render("Any to quit", True, (255, 255, 255))
    WIN.blit(text1, dest=(60, HEIGHT // 2 - 30))
    WIN.blit(text2, dest=(60, HEIGHT // 2))

    pygame.display.update()
    event = pygame.event.wait()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            while (run):
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                collision_handler()
                bird.grav()
                block.move()
                jump_handler()
                boundaries_handler()
                print(bird.score)
                draw_window()
            break
        else:
            break
pygame.quit()
