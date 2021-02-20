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
ball_is_alive = False

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

class paddle():
    def __init__(self):
        self.paddle = pygame.image.load('images/bar.png')
        self.paddle = pygame.transform.scale(self.paddle,(200,30))
        self.rect = self.paddle.get_rect()
        self.rect.x = int((WINDOW_WIDTH /2) - (self.paddle.get_width()/2))
        self.rect.y =  WINDOW_HEIGHT - (self.paddle.get_height() *2)
        self.speed = 7
        self.direction = 0
    
    def move(self):
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.x > 0 :
            self.direction = -1
            self.rect.x -= self.speed
        if key[pygame.K_RIGHT] and self.rect.x < (WINDOW_WIDTH-self.paddle.get_width()) :
            self.direction = 1
            self.rect.x += self.speed 
    
    def draw(self):
        game_window.blit(self.paddle, self.rect)

class game_ball():
    def __init__(self, x, y):
        self.reset(x,y)

    def reset(self, x, y):
        self.ball = pygame.image.load('images/ball.png')
        self.ball = pygame.transform.scale(self.ball, (10, 10))
        self.radius = 5
        self.rect = self.ball.get_rect()
        self.rect.x = x - self.radius
        self.rect.y = y - self.radius*2
        self.speed = 5
        self.direction_x = 1
        self.direction_y = -1
    
    def move(self):
        self.check_collisions(paddle.rect,wall.all_blocks)
        if self.rect.x < 0 or self.rect.x > (WINDOW_WIDTH - self.ball.get_width()):
            self.direction_x = -self.direction_x
        if self.rect.y < 0:
            self.direction_y = -self.direction_y
        if self.rect.y > (WINDOW_HEIGHT - self.ball.get_height()):
            ball_is_alive = False
        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed
    
    def draw(self):
        game_window.blit(self.ball, self.rect)
        
    def check_collisions(self, paddle, blocks):
        collision_limit = 6
        if self.rect.colliderect(paddle):
            #check whether collision is from above, right or left
            if abs(self.rect.bottom - paddle.top) < collision_limit:
                self.direction_y = -self.direction_y
            if abs(self.rect.left - paddle.right) < collision_limit:
                self.direction_x = -self.direction_x
            if abs(self.rect.right - paddle.left) < collision_limit:
                self.direction_x = -self.direction_x

        for row in blocks:
            for block in row:
                multiple_collision = True # variable to manage edge collisions
                if self.rect.colliderect(block[0]):
                    #detect from which direction the ball hits the brick
                    if abs(self.rect.top - block[0].bottom) < collision_limit and multiple_collision:
                        self.direction_y = -self.direction_y
                        multiple_collision = False
                    if abs(self.rect.bottom - block[0].top) < collision_limit and multiple_collision:
                        self.direction_y = -self.direction_y
                        multiple_collision = False
                    if abs(self.rect.left - block[0].right) < collision_limit and multiple_collision:
                        self.direction_x = -self.direction_x
                        multiple_collision = False
                    if abs(self.rect.right - block[0].left) < collision_limit and multiple_collision:
                        self.direction_x = -self.direction_x
                        multiple_collision = False
                    #decrement block's lives
                    if block[1] > 1:
                        block[1] -= 1
                    else:
                        block[0] = (0,0,0,0)
        


def update():
    pygame.display.update()
    pygame.time.Clock().tick(FPS)

wall = brick_wall()
wall.create_wall()
paddle = paddle()
ball = game_ball(int(WINDOW_WIDTH/2),paddle.rect.top)


game_running = True
while game_running:

    #draw objects    
    game_window.fill(background)
    wall.draw_wall()
    paddle.draw()
    ball.draw()

    if ball_is_alive:
        paddle.move()
        ball.move()

    update()
    # Loop through all active events
    for event in pygame.event.get():
        # Handle closure
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.KEYDOWN and ball_is_alive == False:
            if event.key == pygame.K_SPACE:
                ball_is_alive = True
                ball.reset(int(WINDOW_WIDTH/2),paddle.rect.top)
    
    # Update display

pygame.quit()
sys.exit()