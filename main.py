import sys
import random
import pygame
import pygame.locals


# Absolutes (in pixels where not otherwise stated)
FPS = 30    # frames per second (window refresh speed)
REVEAL_SPEED = 100  # Speed of box reveal
CELL_SIDE_LENGTH = 20      # Side length of each cell
CELL_MARGIN = 2     # Gap between cells
GRID_HEIGHT = 10   # How many cells are in the grid
GRID_WIDTH = 10
X_BOARD_MARGIN = 50   # Gap between grid and sides of board
Y_BOARD_MARGIN = 50
DIFFICULTY = 0.1    # Later features, will affect board size and mine ratio

# Relatives (so board size can easily be changed)
NUM_MINES = 1 + int(GRID_WIDTH * GRID_HEIGHT * DIFFICULTY)  # Default about 10% of the board is mines, no matter the size (always at least one)
WINDOW_HEIGHT = 250     # Side length of window
WINDOW_WIDTH = 250      # TODO relative window size

# R G B
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (205, 201, 201)

BG_COLOR = BLACK    # Background color
CELL_COLOR = GRAY
HIGHLIGHT_COLOR = BLUE  # Cell the cursor is currently hovering over

# Symbols
FLAG = 'flag'
MINE = 'mine'
REVEALED = 'revealed'


def main():
    pygame.init()
    global FPS_CLOCK, DISPLAY_SURF
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    mouseX = 0  # Stores x-coordinate of mouse event
    mouseY = 0  # Stores y-coordinate of mouse event
    pygame.display.set_caption('Minesweeper')

    board = get_board()
    revealedCells = generate_data(False)
    flags = generate_data(False)
    done = False

    DISPLAY_SURF.fill(BG_COLOR)


def get_board():
    icons = []
    mines = 0

    # Bottom of board is made of only mines and revealed tiles, which is then selectively covered for gameplay
    # Making randomized array
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if mines < NUM_MINES:
                icons.append((MINE, GREEN))
                mines += 1
            else:
                icons.append((REVEALED, WHITE))
    random.shuffle(icons)

    # Create static under-board
    board = []
    for x in range(GRID_WIDTH):
        column = []
        for y in range(GRID_HEIGHT):
            column.append(icons[0])
            del icons[0]  # so the next icon[0] is the one after this
        board.append(column)

    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            mines = 0

            if x > 0:
                if y > 0:
                    if board[x - 1][y - 1][0] == MINE:
                        mines += 1
                if board[x - 1][y][0] == MINE:
                    mines += 1
                if y < GRID_HEIGHT - 1:
                    if board[x - 1][y + 1][0] == MINE:
                        mines += 1

            if x < GRID_WIDTH - 1:
                if y > 0:
                    if board[x + 1][y - 1][0] == MINE:
                        mines += 1
                if board[x + 1][y][0] == MINE:
                    mines += 1
                if y < GRID_HEIGHT - 1:
                    if board[x + 1][y + 1][0] == MINE:
                        mines += 1

            if y > 0:
                if board[x][y - 1][0] == MINE:
                    mines += 1

            if y < GRID_HEIGHT - 1:
                if board[x][y + 1][0] == MINE:
                    mines += 1

            # set number of mines
            if board[x][y][0] != MINE:
                if mines in range(1, 9):
                    board[x][y] = (str(mines), WHITE)

    return board


# Returns a list of lists showing which cells are revealed
def generate_data(val):
    revealed_cells = []
    for i in range(GRID_WIDTH):
        revealed_cells.append([val] * GRID_HEIGHT)
    return revealed_cells


# Convert row, column coordinates into x, y pixel coordinates (for drawing shapes)
def get_top_left_coordinates(row, column):
    left = row * (CELL_SIDE_LENGTH + CELL_MARGIN) + X_BOARD_MARGIN
    top = column * (CELL_SIDE_LENGTH + CELL_MARGIN) + Y_BOARD_MARGIN
    return left, top


# Convert x, y pixel coordinates to row, column coordinates (for mouse hovering)
def get_box_at_pixel(x, y):
    for cell_x in range(GRID_WIDTH):
        for cell_y in range(GRID_HEIGHT):
            left, top = get_top_left_coordinates(cell_x, cell_y)
            cell_rect = pygame.Rect(left, top, CELL_SIDE_LENGTH, CELL_SIDE_LENGTH)
            if cell_rect.collidepoint(x, y):    # If currently hovering over a cell
                return cell_x, cell_y
    return None, None  # If not currently hovering over a cell

