import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 1920, 1020
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PINE X GAME")

# Цвета
WHITE = (124, 138, 170)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # Цвет текста "Вы выиграли"

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
    pygame.Rect(300, 900, 100, 20),
    pygame.Rect(540, 715, 100, 20),
    pygame.Rect(540, 540, 100, 20),
    pygame.Rect(435, 350, 100, 20),
    pygame.Rect(750, 275, 100, 20),
    pygame.Rect(975, 400, 100, 20),
    pygame.Rect(1150, 275, 500, 20),
    
    pygame.Rect(1850, 100, 400, 20),
    pygame.Rect(1800, 275, 400, 20),  # Платформа для победы
    pygame.Rect(1750, 400, 400, 20),
]

# Загрузка изображения ананаса
pineapple_img = pygame.image.load(r'c:\Users\sasha\OneDrive\Desktop\ANANAS.png')  # Замените 'pineapple.png' на имя вашего файла
pineapple_img = pygame.transform.scale(pineapple_img, (player_size, player_size))  # Масштабируем изображение

# Инициализация шрифта
font = pygame.font.Font(None, 72)

# Функция для отрисовки игрока
def draw_player(x, y):
    screen.blit(pineapple_img, (x, y))  # Отображаем изображение ананаса на экране

# Функция для обработки столкновений игрока с платформами
def check_collision(player_rect, platforms):
    global player_velocity_y, on_ground
    on_ground = False

    for platform in platforms:
        # Проверка вертикального столкновения только сверху платформы
        if player_rect.colliderect(platform):
            if player_velocity_y > 0:  # Падение игрока
                if player_rect.bottom > platform.top and player_rect.bottom - player_velocity_y <= platform.top:
                    player_rect.bottom = platform.top
                    player_velocity_y = 0
                    on_ground = True
            elif player_velocity_y < 0:  # Подпрыгивание игрока
                if player_rect.top < platform.bottom and player_rect.top - player_velocity_y >= platform.bottom:
                    player_rect.top = platform.bottom
                    player_velocity_y = 0

    return player_rect

# Основной игровой цикл
clock = pygame.time.Clock()
show_win_message = False  # Флаг для показа сообщения "Вы выиграли"

while True:
    screen.fill(WHITE)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_d]:
        player_x += player_speed
    if keys[pygame.K_SPACE] and on_ground:
        player_velocity_y = -jump_strength
        on_ground = False

    # Применение гравитации
    player_velocity_y += gravity
    player_y += player_velocity_y

    # Создание прямоугольника игрока
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

    # Проверка столкновений игрока с платформами
    player_rect = check_collision(player_rect, platforms)

    # Проверка столкновения с платформой победы
    win_platform = pygame.Rect(1850, 275, 400, 20)  # Платформа для победы
    if player_rect.colliderect(win_platform):
        show_win_message = True  # Показываем сообщение "Вы выиграли!"
    else:
        show_win_message = False  # Скрываем сообщение, если не на платформе

    # Обновление позиции игрока
    player_x, player_y = player_rect.x, player_rect.y

    # Остановка падения при достижении земли
    if player_y + player_size >= HEIGHT:
        player_y = HEIGHT - player_size
        player_velocity_y = 0
        on_ground = True

    # Отрисовка игрока и платформ
    draw_player(player_x, player_y)  # Отрисовка изображения ананаса
    for platform in platforms:
        pygame.draw.rect(screen, BLACK, platform)

    # Отображение сообщения "Вы выиграли!" если игрок на специальной платформе
    if show_win_message:
        text_surface = font.render("Вы выиграли!", True, GREEN)  # Создаём текстовую поверхность
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Определяем положение текста
        screen.blit(text_surface, text_rect)  # Отображение текста на экране

    # Обновление экрана
    pygame.display.flip()

    # Ограничение FPS
    clock.tick(60)
