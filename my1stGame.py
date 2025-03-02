import pygame
import random
import time
import os

# Инициализация Pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxy Shooter")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Игровые переменные
clock = pygame.time.Clock()
FPS = 60
score = 0
lives = 3

# Состояния игры
START_SCREEN = 0
GAME_ACTIVE = 1
GAME_OVER = 2
game_state = START_SCREEN

# Загрузка рекорда
highscore_file = "highscore.txt"
if os.path.exists(highscore_file):
    with open(highscore_file, "r") as file:
        highscore = int(file.read())
else:
    highscore = 0

# Шрифт
font = pygame.font.Font(None, 36)

# Загрузка изображений
player_img = pygame.image.load("player.png")
enemy_img = pygame.image.load("enemy.png")
bullet_img = pygame.image.load("bullet.png")
enemy_bullet_img = pygame.image.load("enemy_bullet.png")

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_img, (50, 40))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Класс пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(bullet_img, (10, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -7

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Класс вражеской пули
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(enemy_bullet_img, (10, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(enemy_img, (40, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(2, 5)
        self.shoot_timer = random.randint(30, 120)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(2, 5)

        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot()
            self.shoot_timer = random.randint(60, 180)

    def shoot(self):
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)

# Группы спрайтов
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

enemies = pygame.sprite.Group()
for _ in range(5):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

# Функция для отрисовки текста
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Функция для создания кнопок
def draw_button(surface, color, x, y, width, height, text):
    pygame.draw.rect(surface, color, (x, y, width, height))
    draw_text(text, font, WHITE, surface, x + 10, y + 10)

# Основной игровой цикл
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == START_SCREEN:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    game_state = GAME_ACTIVE

        elif game_state == GAME_OVER:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    # Сброс игры
                    game_state = GAME_ACTIVE
                    score = 0
                    lives = 3
                    all_sprites.empty()
                    enemies.empty()
                    bullets.empty()
                    enemy_bullets.empty()
                    player = Player()
                    all_sprites.add(player)
                    for _ in range(5):
                        enemy = Enemy()
                        all_sprites.add(enemy)
                        enemies.add(enemy)
                elif exit_button.collidepoint(mouse_pos):
                    running = False

        if game_state == GAME_ACTIVE:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

    if game_state == START_SCREEN:
        screen.fill(BLACK)
        draw_text("Galaxy Shooter", font, WHITE, screen, WIDTH // 2 - 100, HEIGHT // 2 - 50)
        start_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2, 100, 40)
        draw_button(screen, GREEN, WIDTH // 2 - 50, HEIGHT // 2, 100, 40, "Start")
        pygame.display.flip()

    elif game_state == GAME_ACTIVE:
        # Обновление
        all_sprites.update()

        # Проверка столкновения пуль с врагами
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 10
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Проверка столкновения вражеских пуль с игроком
        if pygame.sprite.spritecollide(player, enemy_bullets, True):
            lives -= 1
            if lives <= 0:
                game_state = GAME_OVER

        # Отрисовка
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Отображение очков и жизней
        draw_text(f"Score: {score}", font, WHITE, screen, 10, 10)
        draw_text(f"Lives: {lives}", font, WHITE, screen, 10, 40)
        draw_text(f"Highscore: {highscore}", font, WHITE, screen, 10, 70)

        pygame.display.flip()

    elif game_state == GAME_OVER:
        screen.fill(BLACK)
        draw_text("GAME OVER", font, RED, screen, WIDTH // 2 - 80, HEIGHT // 2 - 40)
        draw_text(f"Score: {score}", font, WHITE, screen, WIDTH // 2 - 50, HEIGHT // 2)
        draw_text(f"Highscore: {highscore}", font, WHITE, screen, WIDTH // 2 - 70, HEIGHT // 2 + 40)

        restart_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 80, 120, 40)
        draw_button(screen, GREEN, WIDTH // 2 - 60, HEIGHT // 2 + 80, 120, 40, "Restart")
        exit_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 130, 120, 40)
        draw_button(screen, RED, WIDTH // 2 - 60, HEIGHT // 2 + 130, 120, 40, "Exit")

        pygame.display.flip()

pygame.quit()