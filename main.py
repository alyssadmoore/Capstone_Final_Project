import pygame

# Define some colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (205, 201, 201)

# Set width and height of each cell, as well as margins between cells, in pixels
WIDTH = 20
HEIGHT = 20
MARGIN = 2

# Create a 2 dimensional array to hold information on each cell
# Fill in with zeroes to start with blank grid. Default grid size is 10x10 cells
grid = []
for row in range(10):
    grid.append([])
    for column in range(10):
        grid[row].append(0)

# Possible values in above array are mapped as follows:
# 0 = unclicked
# 1-8 = num bombs around clicked cell
# 9 = clicked, clear
# 10 = flag
# 11 = bomb

# Initialize pygame
pygame.init()

# Set font
font = pygame.font.SysFont("monospace", 10)

# Set screen height and width- 10 rows of cells * 20 pixels each + 2 pixels between each cell = 222 pixels square
WINDOW_SIZE = [222, 222]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Minesweeper")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()


# Draws an X to represent a flag placed on a tile
def draw_x(row, column):
    upper = (MARGIN + WIDTH) * column + MARGIN
    left = (MARGIN + HEIGHT) * row + MARGIN
    lower = upper + WIDTH
    right = left + HEIGHT
    # Test drawing a red X
    # (screen, color, closed, [uppermost point, leftmost point, width, height], thickness)
    pygame.draw.line(screen, RED, (upper, left), (lower, right), 2)
    pygame.draw.line(screen, RED, (upper, right), (lower, left), 2)


def draw_number(row, column, number):
    upper = (MARGIN + WIDTH) * column + MARGIN
    left = (MARGIN + HEIGHT) * row + MARGIN
    label = font.render(number, 1, BLACK)
    screen.blit(label, (upper, left))


# Returns number of bombs around clicked cell
def check_num_bombs(row, column):
    check1 = grid[row-1][column-1]
    check2 = grid[row][column-1]
    check3 = grid[row+1][column-1]
    check4 = grid[row][column+1]
    check5 = grid[row-1][column]
    check6 = grid[row+1][column]
    check7 = grid[row-1][column+1]
    check8 = grid[row+1][column+1]
    checklist = [check1, check2, check3, check4, check5, check6, check7, check8]

    counter = 0
    for x in checklist:
        if x == 11:
            counter += 1

    return counter


# Main loop
def main():
    # Used to loop until the user clicks the close button
    done = False
    while not done:
        # An event means the user did something
        for event in pygame.event.get():
            # If the user clicked the close button, use flag to exit loop
            if event.type == pygame.QUIT:
                done = True
            # Mousedown can mean left, middle, or right button: left is 1, middle is 2, right is 3
            # Left button digs, right button places a flag
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()    # Get mouse position
                    column = pos[0] // (WIDTH + MARGIN)     # Convert x/y screen coordinates to cell coordinates
                    row = pos[1] // (HEIGHT + MARGIN)

                    # TODO "You Lose" screen
                    # If the tile is a bomb, player loses
                    if grid[row][column] == 11:
                        print("You lose")

                    # If we get this far, player has NOT clicked a bomb- check for bombs around clicked tile
                    bombs = check_num_bombs(row, column)
                    grid[row][column] = 1   # No matter what, color tile white
                    # TODO draw 1-8 functions

                elif event.button == 3:
                    pos = pygame.mouse.get_pos()
                    column = pos[0] // (WIDTH + MARGIN)
                    row = pos[1] // (HEIGHT + MARGIN)
                    if grid[row][column] != 1:
                        if grid[row][column] == 9:
                            grid[row][column] = 0
                        else:
                            grid[row][column] = 9

        # Set the screen background
        screen.fill(BLACK)

        # Draws the grid on top of the background
        for row in range(10):
            for column in range(10):
                # Unclicked cells are gray (default)
                color = GRAY
                # Clicked but empty cells are white
                if grid[row][column] == 1:
                    color = WHITE
                # Cells actually created here (screen, color, [uppermost point, leftmost point, width, height])
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])
                # So whole map isn't drawn over X's
                if grid[row][column] == 9:
                    draw_x(row, column)

        # Limit refresh rate to 60 frames per second
        clock.tick(60)

        # Update the screen
        pygame.display.flip()

    # Once we have closed the window, this stops the process
    pygame.quit()


main()
