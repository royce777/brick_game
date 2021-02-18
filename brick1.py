import pygame, sys

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

pygame.init()

background = (0,0,0)
red = (255,0,0)
yellow = (255,255,0)
green = (0,128,0)

game_window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Brick Smasher")

FPS = 60

columns = 8
rows = 6
class brick_wall():
    def __init__(self):
        self.width = WINDOW_WIDTH // columns
        self.height = 30

    def create_wall(self):
        self.all_blocks = []
        single_block = [] # this will contain the shape itself and its lives
        for row in range(rows):
            block_row = [] # this will contain all single blocks of a row
            for column in range(columns):
                block_x = column * self.width
                block_y = row * self.height
                rectangle = pygame.Rect(block_x, block_y, self.width, self.height)
                if row < 2:
                    lives = 3
                elif row < 4:
                    lives = 2
                elif row < 6:
                    lives = 1
                single_block = [rectangle, lives]
                block_row.append(single_block)
            self.all_blocks.append(block_row)
        
    def draw_wall(self):
        for row in self.all_blocks:
            for block in row:
                if block[1] == 3:
                    colour = red
                elif block[1] == 2:
                    colour = yellow
                elif block[1] == 1:
                    colour = green
                pygame.draw.rect(game_window, colour, block[0])
                pygame.draw.rect(game_window, background, block[0], 2)

class bar():
    def __init__(self):
        self.bar = pygame.image.load('images/bar.png')
        self.bar = pygame.transform.scale(self.bar,(200,30))
        self.x = int((WINDOW_WIDTH /2) - (self.bar.get_width()/2))
        self.y =  WINDOW_HEIGHT - (self.bar.get_height() *2)
        self.speed = 7
        self.direction = 0
    
    def move(self):
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.x > 0 :
            self.direction = -1
            self.x -= self.speed
        if key[pygame.K_RIGHT] and self.x < (WINDOW_WIDTH-self.bar.get_width()) :
            self.direction = 1
            self.x += self.speed 
    
    def draw(self):
        game_window.blit(self.bar, (self.x,self.y))

class game_ball():
    def __init__(self, x, y):
        self.ball = pygame.image.load('images/ball.png')
        self.ball = pygame.transform.scale(self.ball, (20, 20))
        self.radius = 10
        self.rect = self.ball.get_rect()
        self.rect.x = x - self.radius
        self.rect.y = y - self.radius
        self.speed = 10
        self.direction_x = 1
        self.direction_y = 1
    
    def move(self):
        print(self.ball.get_rect().left)
        if self.rect.x > 0 and self.rect.x < (WINDOW_WIDTH - self.ball.get_width()):
            self.rect.x += self.direction_x * self.speed
            print('here i am')
        else:
            self.direction_x = -self.direction_x
            self.rect.x += self.direction_x * self.speed
        if self.rect.y > 0 and self.rect.y < (WINDOW_HEIGHT - self.ball.get_height()):
            self.rect.y += self.direction_y * self.speed
        else:
            self.direction_y = -self.direction_y
            self.rect.y += self.direction_y * self.speed
    
    def draw(self):
        game_window.blit(self.ball, self.rect)


        


def update():
    pygame.display.update()
    pygame.time.Clock().tick(FPS)

wall = brick_wall()
wall.create_wall()
bar = bar()
ball = game_ball(int(WINDOW_WIDTH/2),bar.y)


game_running = True
while game_running:
    game_window.fill(background)
    wall.draw_wall()
    bar.draw()
    bar.move()
    ball.draw()
    ball.move()
    update()
    # Loop through all active events
    for event in pygame.event.get():
        # Handle closure
        if event.type == pygame.QUIT:
            game_running = False
    
    # Update display

pygame.quit()
sys.exit()