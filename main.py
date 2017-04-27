import pygame

# Define some colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set width and height of each cell, in pixels
WIDTH = 20
HEIGHT = 20

# Set margin, in pixels, between each cell
MARGIN = 2

# Create a 2 dimensional array to hold information on each cell
# Fill in with zeroes to start with blank grid. Default grid size is 10x10 cells
grid = []
for row in range(10):
    grid.append([])
    for column in range(10):
        grid[row].append(0)

# Example to change cell information
grid[2][6] = 1  # 3 blocks down, 7 blocks over
grid[6][2] = 2  # 7 blocks down, 3 blocks over
grid[0][0] = 3  # Upper left corner

# Initialize pygame
pygame.init()

# Set screen height and width- 10 rows of cells * 20 pixels each + 2 pixels between each cell = 222 pixels square
WINDOW_SIZE = [222, 222]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Minesweeper")

# Used to loop until the user clicks the close button
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Main loop
while not done:
    # An event means the user did something
    for event in pygame.event.get():
        # If the user clicked the close button, use flag to exit loop
        if event.type == pygame.QUIT:
            done = True
        # If the user clicked somewhere, we need to translate the mouse position to the corresponding cell
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse position
            pos = pygame.mouse.get_pos()
            # Convert x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            # Set that location to one (changes color to green, for testing)
            grid[row][column] = 1

    # Set the screen background
    screen.fill(BLACK)

    # Draws the grid on top of the background
    for row in range(10):
        for column in range(10):
            # "empty" cells are colored white (value 0)
            color = WHITE
            # Set some initial colors for testing
            if grid[row][column] == 1:
                color = GREEN
            elif grid[row][column] == 2:
                color = RED
            elif grid[row][column] == 3:
                color = BLUE
            # Cells actually created here
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    # Limit refresh rate to 60 frames per second
    clock.tick(60)

    # Update the screen
    pygame.display.flip()

# Once we have closed the window, this stops the process
pygame.quit()
