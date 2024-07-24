import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
FPS = 60

FISH_SPAWN_OFFSET_X = 128
FISH_SPAWN_OFFSET_Y = 32

# Colors
WHITE = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Interactive Fish Tank")

# Load images
background = pygame.image.load('assets/background.png')

# Fish animation frames
pink_fish_images = [
    pygame.image.load('assets/pink_fish/pink_fish_1.png'),
    pygame.image.load('assets/pink_fish/pink_fish_2.png'),
    pygame.image.load('assets/pink_fish/pink_fish_3.png'),
]

orange_fish_images = [
    pygame.image.load('assets/orange_fish/orange_fish_1.png'),
    pygame.image.load('assets/orange_fish/orange_fish_2.png'),
    pygame.image.load('assets/orange_fish/orange_fish_3.png'),
    pygame.image.load('assets/orange_fish/orange_fish_4.png'),
]

# bubble animation frames
bubble_images = [
    pygame.image.load('assets/bubbles/bubble_x4_1.png'),
    pygame.image.load('assets/bubbles/bubble_x4_2.png'),
]

fish_images = [pink_fish_images, orange_fish_images]
# Resize fish frames if necessary
fish_images = [[pygame.transform.scale(img, (64, 64)) for img in fishes] for fishes in fish_images]


# Fish class
class Fish(pygame.sprite.Sprite):
    def __init__(self, x=None):
        super().__init__()
        self.from_right = bool(random.getrandbits(1))
        self.images = random.choice(fish_images)
        self.image_index = 0
        self.animation_speed = 0.1  # Adjust animation speed as needed
        self.image = self._get_image()
        self.rect = self.image.get_rect()
        self.rect.x = x if x else (0 - self.rect.width if not self.from_right else SCREEN_WIDTH + self.rect.width)
        self.rect.y = random.randint(0,
                                     SCREEN_HEIGHT - self.rect.height - FISH_SPAWN_OFFSET_Y)  # Ensure fish doesn't start in the ground
        self.speed_x = -1 if self.from_right else 1
        self.speed_y = 0

    def _get_image(self):
        self.image_index += self.animation_speed
        if self.image_index >= len(self.images):
            self.image_index = 0
        image = self.images[int(self.image_index)]
        if self.from_right:
            image = pygame.transform.flip(image, True, False)
        return image

    def _update_animation(self):
        self.image = self._get_image()

    def update(self):
        # Update position
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

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
    fish = Fish(x=random.randint(FISH_SPAWN_OFFSET_X, SCREEN_WIDTH - FISH_SPAWN_OFFSET_X))
    fish_group.add(fish)

while running:
    # remove sprites outside of screen
    bubbles_group.remove([b for b in bubbles_group if b.rect.y < 0])
    fish_group.remove(
        [b for b in fish_group if b.rect.x < 0 - 10 - b.rect.width or b.rect.x > SCREEN_WIDTH + 10 + b.rect.width])

    # randomly add bubbles
    if random.random() < 0.02:
        x = random.randint(0, SCREEN_WIDTH)
        for i in range(random.randint(1, 5)):
            bubble = Bubble(x=x, y=SCREEN_HEIGHT - (i * 10))
            bubbles_group.add(bubble)

    # randomly add fish

    if random.random() < 1 - (len(fish_group) / 10):
        fish = Fish()
        fish_group.add(fish)

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
