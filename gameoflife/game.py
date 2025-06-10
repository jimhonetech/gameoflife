import pygame
import numpy as np

# === Config ===
CELL_SIZE = 10
GRID_WIDTH, GRID_HEIGHT = 100, 100
PANEL_WIDTH = 220
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE + PANEL_WIDTH
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE
FPS = 10

ALIVE_COLOR = (0, 255, 0)
DEAD_COLOR = (0, 0, 0)
PANEL_COLOR = (50, 50, 50)
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)
TEXT_COLOR = (255, 255, 255)

# === Init ===
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Segoe UI Emoji", 24)

# === State ===
MIN_LIMIT = 0
MAX_LIMIT = 8
grid = np.random.choice([0, 1], size=(GRID_HEIGHT, GRID_WIDTH))

rules = [
    {"label": "DEATH if > neighbors", "value": 3, "y": 120, "key": "overpop"},
    {"label": "DEATH if < neighbors", "value": 2, "y": 200, "key": "underpop"},
    {"label": "LIFE if == neighbors", "value": 3, "y": 280, "key": "repro"},
]
rule_map = {r["key"]: r for r in rules}

reset_button_rect = pygame.Rect(WINDOW_WIDTH - PANEL_WIDTH + 30, 40, 100, 40)
button_size = (30, 30)
left_x = WINDOW_WIDTH - PANEL_WIDTH + 20
right_x = left_x + 110

# === Functions ===

def create_random_grid():
    return np.random.choice([0, 1], size=(GRID_HEIGHT, GRID_WIDTH))

def count_neighbors(grid, x, y):
    neighbors = grid[max(0, y-1):y+2, max(0, x-1):x+2]
    return np.sum(neighbors) - grid[y, x]

def update_grid(grid):
    new_grid = np.zeros_like(grid)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            n = count_neighbors(grid, x, y)
            if grid[y, x] == 1:
                if rule_map["underpop"]["value"] <= n <= rule_map["overpop"]["value"]:
                    new_grid[y, x] = 1
            else:
                if n == rule_map["repro"]["value"]:
                    new_grid[y, x] = 1
    return new_grid

def draw_button(rect, text, mouse_pos):
    color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect)
    txt = font.render(text, True, TEXT_COLOR)
    screen.blit(txt, txt.get_rect(center=rect.center))

def draw_rule_control(rule, mouse_pos):
    label = font.render(rule["label"], True, TEXT_COLOR)
    screen.blit(label, (left_x, rule["y"] - 30))

    rule["minus_rect"] = pygame.Rect(left_x, rule["y"], *button_size)
    rule["plus_rect"] = pygame.Rect(right_x, rule["y"], *button_size)

    draw_button(rule["minus_rect"], "<", mouse_pos)
    draw_button(rule["plus_rect"], ">", mouse_pos)

    val_text = font.render(str(rule["value"]), True, TEXT_COLOR)
    val_rect = val_text.get_rect(center=((left_x + right_x) // 2, rule["y"] + 15))
    screen.blit(val_text, val_rect)

def handle_rule_click(pos):
    for rule in rules:
        if rule["minus_rect"].collidepoint(pos):
            rule["value"] = max(MIN_LIMIT, rule["value"] - 1)
        elif rule["plus_rect"].collidepoint(pos):
            rule["value"] = min(MAX_LIMIT, rule["value"] + 1)

# === Main loop ===

running = True
while running:
    screen.fill(DEAD_COLOR)

    # Draw cells
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y, x]:
                pygame.draw.rect(screen, ALIVE_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Side panel
    pygame.draw.rect(screen, PANEL_COLOR, (WINDOW_WIDTH - PANEL_WIDTH, 0, PANEL_WIDTH, WINDOW_HEIGHT))
    mouse_pos = pygame.mouse.get_pos()

    draw_button(reset_button_rect, "Reset", mouse_pos)

    for rule in rules:
        draw_rule_control(rule, mouse_pos)

    pygame.display.flip()
    grid = update_grid(grid)
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if reset_button_rect.collidepoint(event.pos):
                grid = create_random_grid()
            else:
                handle_rule_click(event.pos)

pygame.quit()
