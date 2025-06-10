import pygame
import numpy as np

CELL_SIZE = 10
GRID_WIDTH, GRID_HEIGHT = 120, 80
PANEL_WIDTH = 150  # Width of side panel
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE + PANEL_WIDTH
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE
FPS = 10

ALIVE_COLOR = (0, 255, 0)
DEAD_COLOR = (0, 0, 0)
PANEL_COLOR = (50, 50, 50)
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)
TEXT_COLOR = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# randomly setup 1s and 0s
def create_random_grid():
    return np.random.choice([0, 1], size=(GRID_HEIGHT, GRID_WIDTH))

grid = create_random_grid()

def count_neighbors(grid, x, y):
    neighbors = grid[max(0,y-1):y+2, max(0,x-1):x+2]
    total = np.sum(neighbors) - grid[y, x]
    return total

def update_grid(grid):
    new_grid = np.zeros_like(grid)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            neighbors = count_neighbors(grid, x, y)
            if grid[y, x] == 1 and neighbors in [2, 3]:
                new_grid[y, x] = 1
            elif grid[y, x] == 0 and neighbors == 3:
                new_grid[y, x] = 1
    return new_grid

# Define reset button rect
reset_button_rect = pygame.Rect(WINDOW_WIDTH - PANEL_WIDTH + 25, 50, 100, 40)

running = True
while running:
    screen.fill(DEAD_COLOR)

    # grid cells
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y, x] == 1:
                rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, ALIVE_COLOR, rect)

    # side panel
    panel_rect = pygame.Rect(WINDOW_WIDTH - PANEL_WIDTH, 0, PANEL_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(screen, PANEL_COLOR, panel_rect)

    # reset button
    mouse_pos = pygame.mouse.get_pos()

    if reset_button_rect.collidepoint(mouse_pos):
        color = BUTTON_HOVER_COLOR
    else:
        color = BUTTON_COLOR
    pygame.draw.rect(screen, color, reset_button_rect)

    text_surface = font.render("Reset", True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=reset_button_rect.center)
    screen.blit(text_surface, text_rect)

    pygame.display.flip()
    grid = update_grid(grid)
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if reset_button_rect.collidepoint(event.pos):
                    grid = create_random_grid()

pygame.quit()
