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

# Игровые переменные
clock = pygame.time.Clock()
FPS = 60
score = 0
lives = 3

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

# Игровой цикл
running = True
game_over = False

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player.shoot()

    if not game_over:
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
                game_over = True
                pygame.display.flip()
                time.sleep(5)

                # Проверка и запись рекорда
                new_highscore = False
                if score > highscore:
                    highscore = score
                    with open(highscore_file, "w") as file:
                        file.write(str(highscore))
                    new_highscore = True

                # Отображение Game Over
                screen.fill(BLACK)
                game_over_text = font.render("GAME OVER", True, WHITE)
                score_text = font.render(f"Score: {score}", True, WHITE)
                highscore_text = font.render(f"Highscore: {highscore}", True, WHITE)

                screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 40))
                screen.blit(score_text, (WIDTH // 2 - 50, HEIGHT // 2))
                screen.blit(highscore_text, (WIDTH // 2 - 70, HEIGHT // 2 + 40))

                if new_highscore:
                    new_highscore_text = font.render("NEW HIGHSCORE!", True, RED)
                    screen.blit(new_highscore_text, (WIDTH // 2 - 100, HEIGHT // 2 + 80))

                pygame.display.flip()
                time.sleep(5)
                running = False

    # Отрисовка
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Отображение очков и жизней
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    highscore_text = font.render(f"Highscore: {highscore}", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))
    screen.blit(highscore_text, (10, 70))

    pygame.display.flip()

pygame.quit()
