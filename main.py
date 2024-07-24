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

# Fish animation frames
fish_images = [
    pygame.image.load('assets/pink_fish/pink_fish_1.png'),
    pygame.image.load('assets/pink_fish/pink_fish_2.png'),
    pygame.image.load('assets/pink_fish/pink_fish_3.png'),
]

# bubble animation frames
bubble_images = [
    pygame.image.load('assets/bubbles/bubble_x4_1.png'),
    pygame.image.load('assets/bubbles/bubble_x4_2.png'),
]
# Resize fish frames if necessary
fish_images = [pygame.transform.scale(img, (64, 64)) for img in fish_images]


# Fish class
class Fish(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = fish_images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)  # Ensure fish doesn't start in the ground
        self.speed_x = random.choice([-1, 1])
        self.speed_y = 0
        self.animation_speed = 0.1  # Adjust animation speed as needed

    def _bounce_edges(self):
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x = -self.speed_x
            # flip the image
            self.image = pygame.transform.flip(self.image, True, False)

        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
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


# TODO create base entity
class Bubble(pygame.sprite.Sprite):
    def __init__(self, x=None, y=None):
        super().__init__()
        self.images = bubble_images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = x if x else random.randint(self.rect.width, SCREEN_WIDTH - self.rect.width)
        self.rect.y = y if y else random.randint(SCREEN_HEIGHT - 32, SCREEN_HEIGHT)
        self.speed = random.randint(10, 30) / 10
        self.animation_speed = random.randint(5, 20) / 1000
        self.is_flipped = False

    def update(self):
        self._move()
        self._update_animation()

    def _move(self):
        multiplier = (((SCREEN_HEIGHT - self.rect.y) / SCREEN_HEIGHT) + .2)
        self.rect.y -= max(self.speed * multiplier, 1)  # must be 1, otherwise it doesnt change pos

    def _update_animation(self):
        self.image_index += self.animation_speed
        if self.image_index >= len(self.images):
            self.image_index = 0
        next_image = self.images[int(self.image_index)]
        if random.random() < 0.01:
            self.is_flipped = not self.is_flipped
        if self.is_flipped:
            next_image = pygame.transform.flip(next_image, True, True)
        self.image = next_image


# Sprite group
fish_group = pygame.sprite.Group()
bubbles_group = pygame.sprite.Group()

# Main loop
running = True
clock = pygame.time.Clock()

for _ in range(10):
    fish = Fish()
    fish_group.add(fish)

while running:
    # remove sprites outside of screen
    bubbles_group.remove([b for b in bubbles_group if b.rect.y < 0])

    # randomly add bubbles
    if random.random() < 0.02:
        x = random.randint(0, SCREEN_WIDTH)
        for i in range(random.randint(1, 5)):
            bubble = Bubble(x=x, y=SCREEN_HEIGHT - (i * 10))
            bubbles_group.add(bubble)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            bubbles_group.add(Bubble())

    # Update
    fish_group.update()
    bubbles_group.update()
    # Draw
    screen.blit(background, (0, 0))
    fish_group.draw(screen)
    bubbles_group.draw(screen)

    # Refresh screen
    pygame.display.flip()

    # Frame rate
    clock.tick(FPS)

pygame.quit()
