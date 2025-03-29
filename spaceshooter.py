import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load assets
player_img = pygame.Surface((50, 40))
player_img.fill(BLUE)
enemy_img = pygame.Surface((50, 40))
enemy_img.fill(RED)
bullet_img = pygame.Surface((10, 20))
bullet_img.fill(GREEN)

# Initialize score
score = 0
font = pygame.font.SysFont(None, 36)  # Font for displaying the score

def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5

    def update(self):
        mouse_x, _ = pygame.mouse.get_pos()
        self.rect.centerx = mouse_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(2, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(2, 6)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create enemies
for _ in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Initialize firing timer
fire_delay = 100  # Delay in milliseconds (0.1 seconds)
last_fire_time = pygame.time.get_ticks()

# Game loop
running = True
while running:
    clock.tick(60)
    current_time = pygame.time.get_ticks()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check if left mouse button is held down
    if pygame.mouse.get_pressed()[0]:  # Left mouse button
        if current_time - last_fire_time >= fire_delay:
            player.shoot()
            last_fire_time = current_time

    # Update
    player.update()  # Update player position based on mouse
    enemies.update()  # No arguments for enemies
    bullets.update()  # No arguments for bullets

    # Check for collisions
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 10  # Increment score by 10
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    if pygame.sprite.spritecollideany(player, enemies):
        running = False

    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_score()  # Draw the score on the screen
    pygame.display.flip()

pygame.quit()
sys.exit()
