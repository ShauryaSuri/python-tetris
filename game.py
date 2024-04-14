import pygame
import random

# Initialize pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
cyan = (0, 255, 255)
yellow = (255, 255, 0)
magenta = (255, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
orange = (255, 165, 0)
blue = (0, 0, 255)

# Tetris shapes
shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 1], [1, 0, 0]]
]

# Game variables
grid_size = 30
grid_width = screen_width // grid_size
grid_height = screen_height // grid_size
grid = [[black] * grid_width for _ in range(grid_height)]

def draw_grid():
    for x in range(grid_width):
        for y in range(grid_height):
            pygame.draw.rect(screen, grid[y][x], (x * grid_size, y * grid_size, grid_size, grid_size))

def draw_shape(shape, x, y, color):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] == 1:
                pygame.draw.rect(screen, color, ((x + col) * grid_size, (y + row) * grid_size, grid_size, grid_size))

def check_collision(shape, x, y):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] == 1:
                if x + col < 0 or x + col >= grid_width or y + row >= grid_height or grid[y + row][x + col] != black:
                    return True
    return False

def rotate_shape(shape):
    return list(zip(*reversed(shape)))

def clear_rows():
    full_rows = [row for row in range(grid_height) if all(cell != black for cell in grid[row])]
    for row in full_rows:
        del grid[row]
        grid.insert(0, [black] * grid_width)

def main():
    clock = pygame.time.Clock()
    game_over = False

    current_shape = random.choice(shapes)
    current_color = random.choice([cyan, yellow, magenta, green, red, orange, blue])
    current_x = grid_width // 2 - len(current_shape[0]) // 2
    current_y = 0
    score = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(current_shape, current_x - 1, current_y):
                        current_x -= 1
                elif event.key == pygame.K_RIGHT:
                    if not check_collision(current_shape, current_x + 1, current_y):
                        current_x += 1
                elif event.key == pygame.K_DOWN:
                    if not check_collision(current_shape, current_x, current_y + 1):
                        current_y += 1
                elif event.key == pygame.K_UP:
                    rotated = rotate_shape(current_shape)
                    if not check_collision(rotated, current_x, current_y):
                        current_shape = rotated

        if not check_collision(current_shape, current_x, current_y + 1):
            current_y += 1
        else:
            for row in range(len(current_shape)):
                for col in range(len(current_shape[row])):
                    if current_shape[row][col] == 1:
                        grid[current_y + row][current_x + col] = current_color

            clear_rows()

            current_shape = random.choice(shapes)
            current_color = random.choice([cyan, yellow, magenta, green, red, orange, blue])
            current_x = grid_width // 2 - len(current_shape[0]) // 2
            current_y = 0

            if check_collision(current_shape, current_x, current_y):
                game_over = True

        screen.fill(black)
        draw_grid()
        draw_shape(current_shape, current_x, current_y, current_color)
        pygame.display.update()
        clock.tick(2)

    pygame.quit()

if __name__ == '__main__':
    main()
