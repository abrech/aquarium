import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)


# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Interactive Fish Tank")

# Load images
background = pygame.image.load('assets/background.png')
ground_image = pygame.image.load('assets/ground.png')
ground_image = pygame.transform.scale(ground_image, (SCREEN_WIDTH, 64))  # Resize ground if necessary

# Fish animation frames
fish_images = [
    pygame.image.load('assets/fish1.png'),
    pygame.image.load('assets/fish2.png'),
    pygame.image.load('assets/fish3.png')
]

food_images = [
    pygame.image.load('assets/food1.png'),
    pygame.image.load('assets/food2.png'),
    pygame.image.load('assets/food3.png'),
    pygame.image.load('assets/food4.png')
]
# Resize fish frames if necessary
fish_images = [pygame.transform.scale(img, (32, 16)) for img in fish_images]

# Ground position
ground_rect = ground_image.get_rect()
ground_rect.x = 0
ground_rect.y = SCREEN_HEIGHT - ground_rect.height


# Fish class
class Fish(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = fish_images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0,
                                     SCREEN_HEIGHT - self.rect.height - ground_rect.height)  # Ensure fish doesn't start in the ground
        self.speed_x = random.choice([-1, 1])
        self.speed_y = random.choice([-1, 1])
        self.animation_speed = 0.1  # Adjust animation speed as needed

    def _bounce_edges(self):
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x = -self.speed_x
            # flip the image
            self.image = pygame.transform.flip(self.image, True, False)

        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT - ground_rect.height:
            self.speed_y = -self.speed_y

    def _update_animation(self):
        self.image_index += self.animation_speed
        if self.image_index >= len(self.images):
            self.image_index = 0
        self.image = self.images[int(self.image_index)]

    def update(self):
        # Update position
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce the fish off the edges
        self._bounce_edges()

        # Update animation frame
        self._update_animation()


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = food_images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = 0
        self.speed_multiplication = random.randint(1, 5)
        self.animation_speed = 0.1

    def _ground_collision(self):
        # Check for collision with the ground
        if self.rect.colliderect(ground_rect):
            self.rect.bottom = ground_rect.top
            self.speed_multiplication = 0

    def _update_animation(self):
        self.image_index += self.animation_speed
        if self.image_index >= len(self.images):
            self.image_index = 0
        self.image = self.images[int(self.image_index)]

    def update(self):
        if self.speed_multiplication == 0:
            return
        self.rect.y += random.randint(1, 5)/10 * self.speed_multiplication

        self._ground_collision()

        self._update_animation()


# Sprite group
fish_group = pygame.sprite.Group()
food_group = pygame.sprite.Group()

# Main loop
running = True
clock = pygame.time.Clock()

for _ in range(10):
    fish = Fish()
    fish_group.add(fish)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            food = Food()
            food_group.add(food)

    # Update
    fish_group.update()
    food_group.update()

    # Draw
    screen.blit(background, (0, 0))
    fish_group.draw(screen)
    food_group.draw(screen)
    screen.blit(ground_image, ground_rect)

    # Refresh screen
    pygame.display.flip()

    # Frame rate
    clock.tick(FPS)

pygame.quit()
