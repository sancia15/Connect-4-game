import numpy as np
import pygame,sys,random,math
from pygame.locals import *

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):      
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else: 
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            #print(event.pos)
            # Ask for Player 1 Input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40,10))
                        game_over = True
                        celebration=fireworksss()
                        screen.blit(celebration, ())


            # # Ask for Player 2 Input
            else:               
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = myfont.render("Player 2 wins!!", 1, YELLOW)
                        screen.blit(label, (40,10))
                        game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)

def fireworksss():
    #A clock object for keeping track of fps
    clock = pygame.time.Clock()

    #The font used on the panel. 18 pixels high
    font = pygame.font.Font("freesansbold.ttf",18)
    TEXTCOLOR = (255,255,255)

    #Set up the screen
    screen = pygame.display.set_mode((1024,640))
    pygame.display.set_caption("FWSIM Clone")

    #List[s] of colors
    COLORS = [[255,255,255], #White
              [255,64,0],    #Red
              [255,128,0],   #Orange
              [255,204,0],   #Yellow-orange
              [192,255,0],   #Yellow-green
              [64,255,0],    #Bright green
              [0,255,128],   #Sea green
              [0,255,255],   #Aqua
              [0,128,255],   #Turquoise
              [0,48,255],    #Bright blue
              [128,0,255],   #Indigo
              [255,0,255]]   #Magenta

    REDWHITEBLUE = [[255,255,255], #White
                    [255,64,0],    #Red
                    [0,48,255]]    #Bright blue

    #Random rgb color
    def randcolor():
        return [random.randint(128,255),random.randint(0,255),random.randint(0,255)]

    #Find in a list
    def locate(item,listx):
        for i in range(0,len(listx)):
            if listx[i] == item:
                return i

    #Parse the FWML

    clock.tick()
            
    fwml = open("Sample.fwml","r")

    lines = fwml.readlines()

    fwml.close()

    colorpalette = lines[0]
    if colorpalette == "SPECTRUM        \n":
        colorpalette = COLORS
    elif colorpalette == "REDWHITEBLUE    \n":
        colorpalette = REDWHITEBLUE

    ticks = []
    for line in lines[1:]:
        ticks.append(int(line[0:4]))

    timers = []
    for line in lines[1:]:
        timers.append(int(line[5:8]))

    locations = []
    for line in lines[1:]:
        locations.append([int(line[9:13]),
                          int(line[14:18])])


    sizes = []
    for line in lines[1:]:
        sizes.append(int(line[19:22]))
        
    angles = []
    for line in lines[1:]:
        angles.append(int(line[23:26]))
        
    colors = []
    for line in lines[1:]:
        colors.append(int(line[27:30]))

    densities = []
    for line in lines[1:]:
        densities.append(int(line[31:34]))


    #A firework    
    class Firework(pygame.sprite.Sprite):

        #Init function
        def __init__(self,location,size,angle,color,timer,density):
            pygame.sprite.Sprite.__init__(self)
            
            self.location = location
            self.velocity = [math.sin(float(angle))*3,
                        -math.cos(float(angle))*3]
            self.size = size
            
            self.color = color
            self.image = pygame.surface.Surface((size,size))
            self.image.fill(color)
            
            self.angle = float(angle)

            self.ps = []

            self.timer = timer
            self.density = density

        def explode(self,exp):
            if exp == "NORMAL":
                for i in range(self.density):
                    particle = Particle(self.location[:],[0,0.05],self.size,random.randint(0,360),self.color,random.randint(70,80))
                    self.ps.append(particle)
                  
        #Update and render
        def update(self):

            self.timer -= 1

            if self.ps:
                for p in self.ps:
                    p.update()
                return

            if self.timer <= 0:
                self.explode("NORMAL")
                return

            if self.location[0] < 0 or self.location[0] > screen.get_width() or self.location[1] < 0 or self.location[1] > screen.get_height():
                return             

            self.location[0] += self.velocity[0]
            self.location[1] += self.velocity[1]
            
            screen.blit(self.image,self.location)

    class Particle(pygame.sprite.Sprite):

        #Init function
        def __init__(self,location,acceleration,size,angle,color,death):
            pygame.sprite.Sprite.__init__(self)
             
            self.location = location
            self.velocity = [math.sin(float(angle))*3,
                        -math.cos(float(angle))*3]
            self.acceleration = acceleration
            self.size = size
            
            self.color = color
            self.image = pygame.surface.Surface((size,size))
            self.image.fill(color)
            
            self.angle = float(angle)
            self.life = 0
            self.death = death
     
        #Update and render
        def update(self):

            self.life += 1

            if self.life >= self.death:
                return

            if self.location[0] < 0 or self.location[0] > screen.get_width() or self.location[1] < 0 or self.location[1] > screen.get_height():
                return

            self.velocity[0] += self.acceleration[0]
            self.velocity[1] += self.acceleration[1]

            self.location[0] += self.velocity[0]
            self.location[1] += self.velocity[1]
            
            screen.blit(self.image,self.location)

    fireworks = []

    phase = 0

    loadtime = clock.tick()
    print("Loading time: " + str(loadtime) + " Milliseconds")

    while True:

        screen.fill((0,0,0))

        if phase in ticks:
            index = locate(phase,ticks)
            fw = Firework(locations[index],sizes[index],angles[index],colorpalette[colors[index]],timers[index],densities[index])
            fireworks.append(fw)

        for fw in fireworks:
            fw.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


        pygame.display.update()
        
        phase += 1

        clock.tick(100)

        
