import numpy as np                #It is a Python library that provides a multidimensional array object
import pygame			#It is a python library of gaming features and more 
import sys
import math
import random

from particle import Particle
from sparker import Sparker
import util

FPS = 600  # can lower this to reduce system resource usage
FADE_RATE = 2 #lower values mean fireworks fade out more slowly

# controls
FIREWORK_MOUSE_BUTTON = 1  # left click
SHIMMER_MOUSE_BUTTON = 3   # right click

# colours
BLACK = [0, 0, 0]
BLACK_FADED = [0, 0, 0, FADE_RATE]

BLUE = (0,0,255)			#prints only colour blue using RGB values format
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)			#yellow is a combination of red and green in RGB


ROW_COUNT = 6 			
COLUMN_COUNT = 7

def runGame():
    FPSClock = pygame.time.Clock()
    pygame.display.set_caption("Fireworks")

    if util.FULLSCREEN_MODE:
        screen = pygame.display.set_mode(util.SCREEN_SIZE, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(util.SCREEN_SIZE)

    # every frame blit a low alpha black surf so that all effects fade out slowly
    blackSurf = pygame.Surface(util.SCREEN_SIZE).convert_alpha()
    blackSurf.fill(BLACK_FADED)

    # GAME LOOP
    while 1:
        screen.blit(blackSurf, (0,0))
        dt = FPSClock.tick(FPS) / 60.0

        handleInput()

        for p in Particle.allParticles:
            p.update(dt)
            p.draw(screen)

        for s in Sparker.allSparkers:
            s.update(dt)
            s.draw(screen)

        screen.blit(screen, (0, 0))
        pygame.display.update()

        pygame.display.set_caption("Fireworks  (FPS " + str(round(FPSClock.get_fps(), 1)) + ")")

# click to spawn fireworks, escape to quit
def handleInput():
    for event in pygame.event.get():
        # terminate on system quit or esc key
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        # spawn fireworks on click
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == FIREWORK_MOUSE_BUTTON:
                Sparker(pos=list(pygame.mouse.get_pos()),
                        colour=[random.uniform(0, 255),
                                random.uniform(0, 255),
                                random.uniform(0, 255)],
                        velocity=random.uniform(40, 60),
                        particleSize=random.uniform(10, 20),
                        sparsity=random.uniform(0.05, 0.15),
                        hasTrail=True,
                        lifetime=random.uniform(10, 20),
                        isShimmer=False)

            if event.button == SHIMMER_MOUSE_BUTTON:
                Sparker(pos=list(pygame.mouse.get_pos()),
                        colour=[random.uniform(50, 255),
                                random.uniform(50, 255),
                                random.uniform(50, 255)],
                        velocity=random.uniform(1, 2),
                        particleSize=random.uniform(3, 8),
                        sparsity=random.uniform(0.05, 0.15),
                        hasTrail=False,
                        lifetime=random.uniform(20, 30),
                        isShimmer=True,
                        radius=random.uniform(40, 100),
                        proportion=0.6,
                        focusRad=random.choice([0, 0.4, 3, 6]),
                        weight=random.uniform(0.001, 0.0015))


def create_board():
	board = np.zeros((6,7))
	return board
 
def drop_piece(board, row, col, piece):			#assigns a piece occupies the empty row slot by assigning a piece to it depending on the player
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0 

def get_next_open_row(board,col):		#checks the status of the row being chosen and returns it
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):		
	print(np.flip(board, 0))		#numpy function to change orientation of the board along the xaxis

def winning_move(board, piece):
	for c in range(COLUMN_COUNT-3):		#checks horizontal locations for winning move
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True
	
	for c in range(COLUMN_COUNT):		#checks vertical locations for winning move
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	for c in range(COLUMN_COUNT-3):		#checks postively sloped diagonals
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True	

	for c in range(COLUMN_COUNT-3):		#checks negatively sloped diagonals	
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

RADIUS = int(SQUARESIZE/2 - 5)

size = (width, height)

screen = pygame.display.set_mode(size)			#reads size and displays a window
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:

	for event in pygame.event.get():			#pygame reads the key pressed and the moves made
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
			pygame.draw.rect(screen,BLACK, (0,0, width, SQUARESIZE))
			#Ask player 1 input
			if turn == 0:
		 		posx = event.pos[0]
		 		col  = int(math.floor(posx/SQUARESIZE))

		 		if is_valid_location(board, col):
		 			row = get_next_open_row(board, col)
		 			drop_piece(board, row, col, 1)

		 			if winning_move(board, 1):
		 				label = myfont.render("Player 1 wins!!", 1, RED)
		 				screen.blit(label, (40, 10))			#updates that specific part of the screen with the label
		 				game_over = True
		 				pygame.init()
		 				runGame()

		 	#Ask player 1 input
			else:
				posx = event.pos[0]
				col  =int(math.floor(posx/SQUARESIZE))
				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 2)
					if winning_move(board, 2):
						label = myfont.render("Player 2 wins!!", 1, YELLOW)
						screen.blit(label, (40, 10))			#updates that specific part of the screen with the label
						game_over = True
						pygame.init()
						runGame()
						
			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn%2

			if game_over:
				pygame.time.wait(3000)