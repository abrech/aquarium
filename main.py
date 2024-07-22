import pygame
import random
import math

from pygame import Rect

# Initialize Pygame
pygame.init()

DEBUG = False

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)

# fish behavior
IDLE, EAT = "IDLE", "EAT"
BOUNCE_OFFSET = 12

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
        self.direction_x = self.speed_x
        self.speed_y = 0
        self.animation_speed = 0.1  # Adjust animation speed as needed
        self.rotation_speed = random.randint(1, 5)
        self.rotation = 180 if self.speed_x < 0 else 0
        self.state = IDLE

        self.detection_area = 96
        self.food_rect = Rect(self.rect.x - (self.rect.width / 2), self.rect.y - (self.rect.height / 2),
                              self.detection_area,
                              self.detection_area)
        self.target = None

    def _bounce_edges(self):
        if self.rect.left < BOUNCE_OFFSET or self.rect.right > SCREEN_WIDTH - BOUNCE_OFFSET:
            self.speed_x = -self.speed_x
            # flip the image
            # TODO handle this with dynamic rotation
            self.rotation = 180 if self.rotation == 0 else 0

        if self.rect.top < BOUNCE_OFFSET or self.rect.bottom > SCREEN_HEIGHT - ground_rect.height - BOUNCE_OFFSET:
            self.speed_y = -self.speed_y

    def _update_animation(self):
        print(self.rotation)
        self.image_index += self.animation_speed
        if self.image_index >= len(self.images):
            self.image_index = 0
        new_image = pygame.transform.rotate(self.images[int(self.image_index)], self.rotation)
        # TODO check if this still makes sense after syncing
        if abs(self.rotation - 180) < 90:
            #pass
            new_image = pygame.transform.flip(new_image, False, True)
        self.image = new_image

    def _check_for_food(self):
        for f in food_group:
            if self.food_rect.colliderect(f.rect):
                self.state = EAT
                self.target = f

    def _move(self):
        if self.state == IDLE:
            if abs(180 - self.rotation) < 90:
                self.rotation += (1 if 180 - self.rotation > 0 else -1) * min(self.rotation_speed,
                                                                              abs(180 - self.rotation))
            else:
                self.rotation += (1 if 0 - self.rotation > 0 else -1) * min(self.rotation_speed,
                                                                            abs(0 - self.rotation))
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            self.food_rect.x += self.speed_x
            self.food_rect.y += self.speed_y

        elif self.state == EAT:
            dist = pygame.Vector2(self.target.rect.center) - pygame.Vector2(self.rect.center)
            if dist.length() != 0:
                dist = dist.normalize()
            if DEBUG:
                print(f"food vector: {dist}")
            self.rect.x += dist.x
            self.rect.y += dist.y

            self.food_rect.x += dist.x
            self.food_rect.y += dist.y

            angle = -pygame.Vector2(1, 0).angle_to(dist)
            is_negative = angle - self.rotation < 0
            self.rotation += min(abs(angle - self.rotation), self.rotation_speed) * (-1 if is_negative else 1)
            if DEBUG:
                print(f"food angle: {angle}")

    def _eat(self):
        if self.rect.colliderect(self.target.rect):
            food_group.remove(self.target)
            self.state = IDLE

    def update(self):
        # Update position
        self._move()

        # Bounce the fish off the edges
        self._bounce_edges()

        # Update animation frame
        self._update_animation()

        # collision detection
        if self.state == IDLE:
            self._check_for_food()
        if self.state == EAT:
            self._eat()


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
        self.rect.y += random.randint(1, 5) / 10 * self.speed_multiplication

        self._ground_collision()

        self._update_animation()


# Sprite group
fish_group = pygame.sprite.Group()
food_group = pygame.sprite.Group()

# Main loop
running = True
clock = pygame.time.Clock()

for _ in range(1):
    fish = Fish()
    fish_group.add(fish)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            food = Food()
            food_group.add(food)
        elif event.type == pygame.KEYDOWN:
            fish = Fish()
            fish_group.add(fish)
        elif DEBUG and event.type == pygame.KEYUP:
            for fish in fish_group:
                fish.image = pygame.transform.rotate(fish.image, 30)
                fish.rotation += 30

    # Update
    fish_group.update()
    food_group.update()

    # Draw
    screen.blit(background, (0, 0))
    fish_group.draw(screen)
    food_group.draw(screen)
    if DEBUG:
        for fish in fish_group:
            pygame.draw.rect(screen, WHITE, fish.food_rect)
    screen.blit(ground_image, ground_rect)

    # Refresh screen
    pygame.display.flip()

    # Frame rate
    clock.tick(FPS)

pygame.quit()
