import pygame
import random
import sys
import os  # For file operations

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

# File to store the high score
HIGH_SCORE_FILE = "high_score.txt"

def load_high_score():
    """Load the high score from a file."""
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            try:
                return int(file.read().strip())
            except ValueError:
                return 0  # Default to 0 if the file is corrupted
    return 0  # Default to 0 if the file doesn't exist

def save_high_score(score):
    """Save the high score to a file."""
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))

# Initialize high score
high_score = load_high_score()

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
fire_delay = 200  # Delay in milliseconds (0.2 seconds)
last_fire_time = pygame.time.get_ticks()

def show_welcome_screen():
    """Display the welcome screen with a 'Start' button."""
    button_font = pygame.font.SysFont(None, 48)
    title_font = pygame.font.SysFont(None, 64)

    title_text = title_font.render("Hello Welcome to Alex's Space Shooter game.", True, WHITE)
    button_text = button_font.render("Start", True, BLACK)
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 60)

    while True:
        screen.fill(BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        pygame.draw.rect(screen, GREEN, button_rect)
        screen.blit(button_text, (button_rect.x + button_rect.width // 2 - button_text.get_width() // 2,
                                  button_rect.y + button_rect.height // 2 - button_text.get_height() // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and button_rect.collidepoint(event.pos):  # Left click on the button
                    return  # Exit the welcome screen and start the game

def show_game_over_screen(final_score):
    """Display the game over screen with the final score and high score."""
    global high_score
    if final_score > high_score:
        high_score = final_score  # Update high score if the current score is higher
        save_high_score(high_score)  # Save the new high score to the file

    title_font = pygame.font.SysFont(None, 64)
    score_font = pygame.font.SysFont(None, 48)
    button_font = pygame.font.SysFont(None, 48)

    title_text = title_font.render("Game Over", True, WHITE)
    score_text = score_font.render(f"Your Score: {final_score}", True, WHITE)
    high_score_text = score_font.render(f"High Score: {high_score}", True, WHITE)
    button_text = button_font.render("Play Again", True, BLACK)
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 60)

    while True:
        screen.fill(BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 - 50))
        pygame.draw.rect(screen, GREEN, button_rect)
        screen.blit(button_text, (button_rect.x + button_rect.width // 2 - button_text.get_width() // 2,
                                  button_rect.y + button_rect.height // 2 - button_text.get_height() // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and button_rect.collidepoint(event.pos):  # Left click on the button
                    return  # Exit the game over screen and restart the game

# Main execution
while True:  # Allow restarting the game after "Game Over"
    show_welcome_screen()  # Show the welcome screen before starting the game

    # Reset game state
    score = 0
    all_sprites.empty()
    enemies.empty()
    bullets.empty()
    player = Player()
    all_sprites.add(player)
    for _ in range(8):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

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

    show_game_over_screen(score)  # Show the game over screen after the game ends
