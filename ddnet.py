import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 1920, 1020
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PINE X GAM")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Игровые переменные
gravity = 0.6
player_speed = 5
jump_strength = 15

# Игрок
player_size = 40
player_x = 100
player_y = HEIGHT - player_size - 50
player_velocity_y = 0
on_ground = False

# Платформы
platforms = [
    #ygame.Rect(типо длина x 100, 800 высота y, длина плотформа200, ширина плотформы 20),
    pygame.Rect(600, 800, 100, 20),
    pygame.Rect(100, 100, 100, 20),
    pygame.Rect(350, 350, 100, 20),

]

# Функция для отрисовки игрока
def draw_player(x, y):
    pygame.draw.rect(screen, GREEN, (x, y, player_size, player_size))

# Основной игровой цикл
clock = pygame.time.Clock()
while True:
    screen.fill(WHITE)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_SPACE] and on_ground:
        player_velocity_y = -jump_strength
        on_ground = False

    # Применение гравитации
    player_velocity_y += gravity
    player_y += player_velocity_y

    # Проверка на столкновение с платформами
    on_ground = False
    for platform in platforms:
        if player_y + player_size >= platform.top and player_y + player_size <= platform.bottom and \
           player_x + player_size > platform.left and player_x < platform.right:
            player_y = platform.top - player_size
            player_velocity_y = 0
            on_ground = True

    # Остановка падения при достижении земли
    if player_y + player_size >= HEIGHT:
        player_y = HEIGHT - player_size
        player_velocity_y = 0
        on_ground = True

    # Отрисовка игрока и платформ
    draw_player(player_x, player_y)
    for platform in platforms:
        pygame.draw.rect(screen, BLACK, platform)

    # Обновление экрана
    pygame.display.flip()

    # Ограничение FPS
    clock.tick(60)