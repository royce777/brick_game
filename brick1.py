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

class ball():
    def __init__(self, x, y):
        self.ball = pygame.image.load('images/ball.png')
        self.ball = pygame.transform.scale(ball, (20, 20))
        self.radius = 10
        self.x = x - self.radius
        self.y = y - self.radius
        self.speed_x = 10
        self.speed_y = 10
        self.direction_x = 0
        self.direction_y = 0
    
    def move(self):
        

        


def update():
    pygame.display.update()
    pygame.time.Clock().tick(FPS)

wall = brick_wall()
wall.create_wall()
bar = bar()


game_running = True
while game_running:
    game_window.fill(background)
    wall.draw_wall()
    bar.draw()
    bar.move()
    update()
    # Loop through all active events
    for event in pygame.event.get():
        # Handle closure
        if event.type == pygame.QUIT:
            game_running = False
    
    # Update display

pygame.quit()
sys.exit()