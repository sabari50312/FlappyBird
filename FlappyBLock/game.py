import pygame
from random import choice

pygame.init()

#CONSTANTS
WIDTH, HEIGHT = 400, 600  #Screen height and width
P_HEIGHT = 24  #Player height DO NOT CHANGE
P_WIDTH = 34  #Player width DO NOT CHANGE

JUMP_HEIGHT = 7  #Jump height Feel free to experiment though 7 works pretty well
BLOCK_WIDTH = 52  #52
BLOCK_GAP = 150  #150
BLOCK_VEL = 4  #4
GRAV = 0.3  #Gravity value Feel free to experiment though 0.3 works pretty well
VELOCITY = 3  #Initial downwards velocity 3 works
BIRD_SIZE = (P_WIDTH, P_HEIGHT)  #DO NOT CHANGE
FPS = 60  #FPS duh

WIN = pygame.display.set_mode((WIDTH, HEIGHT))  #Pygame surface object
my_font = pygame.font.SysFont('Comic Sans MS', 30)  #Pygame surface for text

BIRD_IMG = pygame.image.load("birb.png").convert_alpha()  #Player image
BG = pygame.image.load("bg.png").convert_alpha()  #Background image
PIPE_TOP = pygame.image.load("pipe2.png").convert_alpha()  #Top pipe image
PIPE_BOTTOM = pygame.image.load(
    "pipe1.png").convert_alpha()  #Bottom pipe image

RUN = True


class obstacles:
    '''The blocks class'''

    def __init__(self, width, gap, velocity):
        self.x = WIDTH + width - 20  #x coordinate of pipes
        self.width = width  #width of pipes
        self.velocity = velocity  #velocity of pipes
        self.height1 = choice([90, 130, 170, 210, 250, 290, 330,
                               370])  #height of top pipes
        self.height2 = (HEIGHT - gap) - self.height1  #height of bottom pipe
        self.rect1 = pygame.Rect(self.x, 0, self.width,
                                 self.height1)  #Top pipe hitbox
        self.rect2 = pygame.Rect(self.x, HEIGHT - self.height2, self.width,
                                 self.height2)  #Bottom pipe hitbox

    def move(self):
        '''Function to move the pipes'''
        self.rect1.x -= self.velocity
        self.rect2.x -= self.velocity

    def draw(self):
        '''Draw pipes to screen'''
        #pygame.draw.rect(WIN, (0, 0, 0), self.rect1)
        #pygame.draw.rect(WIN, (0, 0, 0), self.rect2)
        WIN.blit(PIPE_TOP, (self.rect1.x, self.rect1.height - 379))  #Top pipe
        WIN.blit(PIPE_BOTTOM, (self.rect2.x, self.rect2.y))  #Bottom pipe


class player:
    '''The birdy class'''

    def __init__(self, x, y):
        self.jumpcount = JUMP_HEIGHT  #Jump height of bird
        self.isjump = False
        self.velocity = VELOCITY  #Downwards velocity of bird
        self.neg = 1  #Variable for jump function
        self.rect = pygame.Rect(x, y, P_WIDTH, P_HEIGHT)  #Bird hitbox
        self.score = 0  #Score
        self.score_updated = False  #Variable for score functionality

    def draw(self):
        '''Draw birdy to screen'''
        #pygame.draw.rect(WIN, (255, 0, 0), self.rect)
        WIN.blit(BIRD_IMG,
                 (self.rect.x, self.rect.y))  #Draw the birdy on screen

    def grav(self):
        '''Move the bird'''
        self.rect.y += self.velocity  #Move bird down
        self.velocity += GRAV  #Accelerate bird


#All draw function calls
def draw_window():
    text_surface = my_font.render(str(bird.score), False, (0, 0, 0))
    WIN.blit(BG, (0, 0))
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
                bird.neg = -0.2
            bird.rect.y -= (bird.jumpcount**2 * bird.neg) / 2
            bird.jumpcount -= 1
        else:
            bird.jumpcount = JUMP_HEIGHT
            bird.isjump = False
            bird.velocity = VELOCITY


#Function to make everything stay ON the screen. If it works dont fix it
def boundaries_handler():
    global RUN
    #If block goes out of screen create new block
    if block.rect1.x < -block.width:
        block.__init__(BLOCK_WIDTH, BLOCK_GAP, BLOCK_VEL)
        bird.score_updated = False

    #If bird goes through gap
    if bird.rect.x > block.rect1.x + block.width and not bird.score_updated:
        bird.score += 1
        bird.score_updated = True

    #If bird tries to go out of top of screen
    if bird.rect.y < 0:
        bird.rect.y = 0

    #If bird falls down
    if bird.rect.y > HEIGHT:
        RUN = False


#Function that handles collisions. Mess with this to enable noclip :)
def collision_handler():
    if pygame.Rect.colliderect(bird.rect, block.rect1):
        pygame.time.delay(500)
        pygame.quit()

    if pygame.Rect.colliderect(bird.rect, block.rect2):
        pygame.time.delay(500)
        pygame.quit()


'''Global variables are the worst and I do not reccomend using them. Only used them here just for easy writing of code'''
clock = pygame.time.Clock()  #Pygame clock object
block = obstacles(BLOCK_WIDTH, BLOCK_GAP, BLOCK_VEL)  #Pipes object
bird = player(100, HEIGHT / 2)  #Bird object

#MAIN loop
while (True):
    text1 = my_font.render("Press space to start", True, (255, 255, 255))
    text2 = my_font.render("Any to quit", True, (255, 255, 255))
    WIN.blit(text1, dest=(60, HEIGHT // 2 - 30))
    WIN.blit(text2, dest=(60, HEIGHT // 2))

    pygame.display.update()
    event = pygame.event.wait()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            while (RUN):
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        RUN = False
                collision_handler()
                bird.grav()
                block.move()
                jump_handler()
                boundaries_handler()
                draw_window()
            break
        else:
            break
pygame.quit()
