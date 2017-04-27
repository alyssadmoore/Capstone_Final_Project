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
font = pygame.font.SysFont("monospace", 15)

# Set screen height and width- 10 rows of cells * 20 pixels each + 2 pixels between each cell = 222 pixels square
WINDOW_SIZE = [222, 222]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Minesweeper")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()


# Draws the value that was passed to it into the cell at given row/column
def draw_number(row, column, value):
    upper = (MARGIN + WIDTH) * column + MARGIN
    left = (MARGIN + HEIGHT) * row + MARGIN
    label = font.render(str(value), 1, BLACK)
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


grid[0][0] = 11


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

                # Left click (dig)
                if event.button == 1:
                    pos = pygame.mouse.get_pos()    # Get mouse position
                    column = pos[0] // (WIDTH + MARGIN)     # Convert x/y screen coordinates to cell coordinates
                    row = pos[1] // (HEIGHT + MARGIN)

                    # TODO "You Lose" screen
                    # If the tile is a bomb, player loses
                    if grid[row][column] == 11:
                        print("You lose")
                        done = True

                    # Only continue if the grid is unclicked or has a number
                    if grid[row][column] < 1 or grid[row][column] > 8:

                        # If tile is not a bomb, check for bombs around the tile
                        bombs = check_num_bombs(row, column)

                        if 0 < bombs < 9:
                            grid[row][column] = bombs   # Cell will have value of number of bombs around it
                        else:
                            grid[row][column] = 9   # If there are no bombs, set grid to 9 (zero is unclicked tile)

                # Right click (set/unset flag)
                elif event.button == 3:
                    pos = pygame.mouse.get_pos()
                    column = pos[0] // (WIDTH + MARGIN)
                    row = pos[1] // (HEIGHT + MARGIN)
                    if grid[row][column] == 0 or grid[row][column] >= 10:      # If tile is already clicked & clear, do nothing
                        if grid[row][column] == 10:
                            # TODO flagging then unflagging removes bomb!
                            grid[row][column] = 0   # If tile is already flagged, unflag it
                        else:
                            grid[row][column] = 10   # If tile is unclicked, flag it

        # Set the screen background
        screen.fill(BLACK)

        # Draws the grid on top of the background
        for row in range(10):
            for column in range(10):
                # Unclicked cells are gray (default)
                color = GRAY
                # Clicked but empty cells are white
                if 1 <= grid[row][column] <= 9:
                    color = WHITE
                # Cells actually created here (screen, color, [uppermost point, leftmost point, width, height])
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])

                # Add numbers & x's over basic cells
                if 1 <= grid[row][column] <= 8:
                    draw_number(row, column, grid[row][column])

                elif grid[row][column] == 10:
                    draw_number(row, column, "x")

        # Limit refresh rate to 60 frames per second
        clock.tick(60)

        # Update the screen
        pygame.display.flip()

    # Once we have closed the window, this stops the process
    pygame.quit()


main()
