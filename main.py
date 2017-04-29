import sys
import random
import pygame
import pygame.locals

# TODO timer

# Absolutes (in pixels where not otherwise stated)
CELL_SIDE_LENGTH = 50      # Side length of each cell- ADJUST THIS TO MAKE ENTIRE SCREEN LARGER OR SMALLER
CELL_MARGIN = 2     # Gap between cells
GRID_HEIGHT = 10    # How many cells are in the grid
GRID_WIDTH = 10
X_BOARD_MARGIN = 50   # Gap between grid and sides of board
Y_BOARD_MARGIN = 50
DIFFICULTY = 0.1    # TODO later features, will affect board size and mine ratio
FPS = 30    # frames per second (window refresh speed)

# Relatives (so board size can easily be changed)
NUM_MINES = 1 + int(GRID_WIDTH * GRID_HEIGHT * DIFFICULTY)  # Default about 10% of the board is mines
WINDOW_HEIGHT = (CELL_SIDE_LENGTH * GRID_HEIGHT) + (CELL_MARGIN * GRID_HEIGHT) + (Y_BOARD_MARGIN * 2)
WINDOW_WIDTH = (CELL_SIDE_LENGTH * GRID_WIDTH) + (CELL_MARGIN * GRID_WIDTH) + (X_BOARD_MARGIN * 2)

# R G B (not all used, but kept so theme can easily be changed)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MIDGREEN = (40, 215, 40)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
DARKBLUE = (20, 20, 60)
MAGENTA = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

BG_COLOR = DARKBLUE     # Background color
CELL_COLOR = GRAY       # Universal cover color
HIGHLIGHT_COLOR = CYAN  # Cell the cursor is currently hovering over
FLAG_COLOR = MIDGREEN

# Symbols
FLAG = 'flag'
MINE = 'mine'
CLEAR = 'clear'


def main():
    pygame.init()
    global CLOCK, SURFACE
    CLOCK = pygame.time.Clock()
    SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    mouse_x = 0  # Stores x-coordinate of mouse event
    mouse_y = 0  # Stores y-coordinate of mouse event
    pygame.display.set_caption('Minesweeper by Alyssa Moore 2017')

    board = get_board()
    revealed_cells = generate_data(False)
    flags = generate_data(False)
    game_over = False

    SURFACE.fill(BG_COLOR)

    # Main loop
    while True:
        left_click = False
        right_click = False

        SURFACE.fill(BG_COLOR)
        draw_board(board, revealed_cells, flags)

        font = pygame.font.SysFont("times new roman", 15)

        # Mouse event handling
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT or (event.type == pygame.locals.KEYUP and event.key == pygame.locals.K_ESCAPE):
                pygame.quit()
                sys.exit()  # Even if the window closes, we still need to manually stop the processes
            elif event.type == pygame.locals.MOUSEMOTION:
                mouse_x, mouse_y = event.pos  # For hovering info
            elif event.type == pygame.locals.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                mouse_x, mouse_y = event.pos
                left_click = True
            elif event.type == pygame.locals.MOUSEBUTTONDOWN and event.button == 3:  # Right click
                mouse_x, mouse_y = event.pos
                right_click = True

        # If user decided to start over, reinitialize board
        if game_over and right_click:
            board = get_board()
            revealed_cells = generate_data(False)
            flags = generate_data(False)
            game_over = False
            right_click = False

        # TODO game over screen, instructions to restart
        if game_over:
            pass

        cell_x, cell_y = get_cell_at_pixel(mouse_x, mouse_y)
        if cell_x is not None and cell_y is not None:   # If mouse is hovering over a cell during mouse event

            # Highlight cell
            if not revealed_cells[cell_x][cell_y] and not game_over:
                highlight_cell(cell_x, cell_y)

            # Digging somewhere
            if not revealed_cells[cell_x][cell_y] and left_click and not game_over:

                flags[cell_x][cell_y] = False

                if board[cell_x][cell_y][0] == MINE:    # If you dig a mine, reveal all cells & game over
                    revealed_cells = generate_data(True)
                    game_over = True

                elif board[cell_x][cell_y][0] == CLEAR:     # If you dig a clear cell, reveal that cell
                    reveal_cells(cell_x, cell_y, board, revealed_cells, flags)

                else:
                    revealed_cells[cell_x][cell_y] = True  # Set the cell as revealed

                draw_board(board, revealed_cells, flags)    # Redraw board after mouse event

            # Placing a flag
            if not revealed_cells[cell_x][cell_y] and right_click and not game_over:
                flags[cell_x][cell_y] = not flags[cell_x][cell_y]
                draw_board(board, revealed_cells, flags)    # Flag is drawn in this method call

            # This block decides whether or not the player has won yet after a mouse event
            win = True
            for x in range(GRID_WIDTH):
                for y in range(GRID_HEIGHT):
                    if (board[x][y][0] == MINE and not flags[x][y]) or (    # If a cell is a mine and not flagged, or
                            board[x][y][0] != MINE and not revealed_cells[x][y]):  # if a cell is clear but not revealed
                        win = False                                                # then the game is not yet complete

            if win:
                game_over = True

        # Redraw the screen and wait for clock tick
        pygame.display.update()
        CLOCK.tick(FPS)


def get_board():
    icons = []
    mines = 0

    # Bottom of board is made of only mines and clear cells, which is then selectively covered for gameplay
    # Making randomized array
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if mines < NUM_MINES:
                icons.append((MINE, RED))
                mines += 1
            else:
                icons.append((CLEAR, WHITE))
    random.shuffle(icons)

    # Create static under-board
    board = []
    for x in range(GRID_WIDTH):
        column = []
        for y in range(GRID_HEIGHT):
            column.append(icons[0])
            del icons[0]  # so the next icon[0] is the one after this
        board.append(column)

    # This block determines how many mines are around each cell, and adds the number to the board's array
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            mines = 0

            if x > 0:
                if y > 0:   # If not on the left edge AND not on top edge
                    if board[x - 1][y - 1][0] == MINE:
                        mines += 1
                if board[x - 1][y][0] == MINE:
                    mines += 1
                if y < GRID_HEIGHT - 1:
                    if board[x - 1][y + 1][0] == MINE:
                        mines += 1

            if x < GRID_WIDTH - 1:
                if y > 0:   # If not on right edge AND not on top edge
                    if board[x + 1][y - 1][0] == MINE:
                        mines += 1
                if board[x + 1][y][0] == MINE:
                    mines += 1
                if y < GRID_HEIGHT - 1:
                    if board[x + 1][y + 1][0] == MINE:
                        mines += 1

            if y > 0:   # If not on right or left edge AND not on top edge
                if board[x][y - 1][0] == MINE:
                    mines += 1

            if y < GRID_HEIGHT - 1:     # If not on riht or left edge AND on bottom edge
                if board[x][y + 1][0] == MINE:
                    mines += 1

            # If the cell is clear and there are mines around it, add the number of mines to board array
            if board[x][y][0] != MINE:
                if mines in range(1, 9):
                    board[x][y] = (str(mines), WHITE)

    return board


# Returns a list of lists showing which cells are clear
def generate_data(val):
    clear = []
    for i in range(GRID_WIDTH):
        clear.append([val] * GRID_HEIGHT)
    return clear


# Convert row, column coordinates into x, y pixel coordinates (for drawing shapes)
def get_top_left_coordinates(row, column):
    left = row * (CELL_SIDE_LENGTH + CELL_MARGIN) + X_BOARD_MARGIN
    top = column * (CELL_SIDE_LENGTH + CELL_MARGIN) + Y_BOARD_MARGIN
    return left, top


# Convert x, y pixel coordinates to row, column coordinates (for mouse hovering)
def get_cell_at_pixel(x, y):
    for cell_x in range(GRID_WIDTH):
        for cell_y in range(GRID_HEIGHT):
            left, top = get_top_left_coordinates(cell_x, cell_y)
            cell_rect = pygame.Rect(left, top, CELL_SIDE_LENGTH, CELL_SIDE_LENGTH)
            if cell_rect.collidepoint(x, y):    # If currently hovering over a cell
                return cell_x, cell_y
    return None, None  # If not currently hovering over a cell


# Redraws board after mouse event
def draw_board(board, revealed, flags):
    for cell_x in range(GRID_WIDTH):
        for cell_y in range(GRID_HEIGHT):
            left, top = get_top_left_coordinates(cell_x, cell_y)

            if not revealed[cell_x][cell_y]:
                # Draw a gray box over unrevealed cell, so value isn't affected but user can't see the value
                pygame.draw.rect(SURFACE, CELL_COLOR, (left, top, CELL_SIDE_LENGTH, CELL_SIDE_LENGTH))

                if flags[cell_x][cell_y]:   # Flag must be drawn here, activated after mouse event
                    half = int(CELL_SIDE_LENGTH * 0.5)   # Relative point halfway through cell
                    # top point, bottom left point, bottom right point
                    pygame.draw.polygon(SURFACE, FLAG_COLOR, [(half + left, top),
                                                              (left, top + CELL_SIDE_LENGTH - CELL_MARGIN/2),
                                                              (left + CELL_SIDE_LENGTH - CELL_MARGIN/2, top + CELL_SIDE_LENGTH - CELL_MARGIN/2)])

            else:   # Draw revealed cells
                shape, color = get_shape_and_color(board, cell_x, cell_y)
                draw_icon(shape, color, cell_x, cell_y)


# Draws icon passed to it in the stated cell
def draw_icon(shape, color, cell_x, cell_y):

    # Relative point of quarter-way through cell
    quarter = int(CELL_SIDE_LENGTH * 0.25)

    left, top = get_top_left_coordinates(cell_x, cell_y)    # Drawing of all images starts at top left corner

    # Draw the shapes
    if shape == CLEAR:
        pygame.draw.rect(SURFACE, color, (left, top, CELL_SIDE_LENGTH, CELL_SIDE_LENGTH))

    elif shape == MINE:
        pygame.draw.ellipse(SURFACE, color, (left, top, CELL_SIDE_LENGTH, CELL_SIDE_LENGTH))

    # Flag shape in draw_board because it is activated via mouse event

    else:   # Clear with num
        pygame.draw.rect(SURFACE, color, (left, top, CELL_SIDE_LENGTH, CELL_SIDE_LENGTH))
        fontsize = int(CELL_SIDE_LENGTH)
        font = pygame.font.SysFont("times new roman", fontsize)
        label = font.render(shape, 1, BLACK)  # a cell with number corresponds to shapes "1", "2", etc.
        SURFACE.blit(label, (left + quarter, top))


# Returns the shape and color of icon to be created in draw_icon method
def get_shape_and_color(board, cell_x, cell_y):
    # shape value for cell x, y is stored in board[x][y][0], color value in board[x][y][1]
    return board[cell_x][cell_y][0], board[cell_x][cell_y][1]


# Draws a box around the cell the mouse is hovering over, 'highlighting' it
def highlight_cell(cell_x, cell_y):
    left, top = get_top_left_coordinates(cell_x, cell_y)
    # Changes with cell size, but line width is hard-set at 2px (last argument)
    pygame.draw.rect(SURFACE, HIGHLIGHT_COLOR, (left - (CELL_MARGIN / 2), top - (CELL_MARGIN / 2),
                                                     CELL_SIDE_LENGTH + CELL_MARGIN, CELL_SIDE_LENGTH + CELL_MARGIN), 2)


# TODO will reveal clear cells next to clear cell the user clicked (and clear cells next to those clear cells, etc.)
def reveal_cells(x, y, board, cells, flags):
    pass


main()
