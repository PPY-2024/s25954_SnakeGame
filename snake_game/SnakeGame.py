import pygame as pg
from random import randrange

user_name = input("Your name: ")
snake_speed = int(input("Set snake speed: "))

MIN_SIZE = 5
MAX_SIZE = 25

field_size = 0
while field_size < MIN_SIZE or field_size > MAX_SIZE:
    field_size = int(input(f"Set field size (between {MIN_SIZE}x{MIN_SIZE} and {MAX_SIZE}x{MAX_SIZE}): "))

WINDOW = 500
TILE_SIZE = WINDOW // field_size
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE//2, TILE_SIZE)
get_random_position = lambda : [randrange(*RANGE), randrange(*RANGE)]
snake = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
snake.center = get_random_position()
length = 1
segments = [snake.copy()]
snake_dir = (0, 0)
food = snake.copy()
food.center = get_random_position()
screen = pg.display.set_mode([WINDOW] * 2)
clock = pg.time.Clock()
dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
score = 0

def show_score(choice, color, font, size):
    score_font = pg.font.SysFont(font, size)
    score_surface = score_font.render(user_name +"'s Score : " + str(score), True, color)
    score_rect = score_surface.get_rect()
    screen.blit(score_surface, score_rect)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w and dirs[pg.K_w]:
                snake_dir = (0, -TILE_SIZE)
                dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}
            if event.key == pg.K_s and dirs[pg.K_s]:
                snake_dir = (0, TILE_SIZE)
                dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
            if event.key == pg.K_a and dirs[pg.K_a]:
                snake_dir = (-TILE_SIZE, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
            if event.key == pg.K_d and dirs[pg.K_d]:
                snake_dir = (TILE_SIZE, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}
    screen.fill('black')
    if snake.center == food.center:
        food.center = get_random_position()
        length += 1
        score += 1
    self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1
    if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW or self_eating:
        print("You lost. Here is your score:", score)
        snake.center, food.center = get_random_position(), get_random_position()
        length, snake_dir = 1, (0, 0)
        segments = [snake.copy()]

    pg.draw.rect(screen, 'red', food)
    [pg.draw.rect(screen, 'green', segment) for segment in segments]

    snake.move_ip(snake_dir)
    segments.append(snake.copy())
    segments = segments[-length:]
    pg.display.flip()
    clock.tick(snake_speed)