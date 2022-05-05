## Assessment 3 Games Programming

# Initialise pygame
import random
import sys

import pygame
from pygame.locals import *

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

SCREEN_WIDTH = 1270
SCREEN_HEIGHT = 720

SCROLL_SPEED = 1
GRAVITY = 0.77

# Draw window
screen = pygame.display.set_mode([1270, 720])

# Define pressed_keys
pressed_key = pygame.key.get_pressed()


class Pillars:
    # Represents every 'pillar' created in game
    def __init__(self, start_x, low=112, high=300):
        # Initialisation
        # pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets/pillar.png").convert_alpha()
        self.x = start_x
        self.high = high
        self.low = low
        self.y = SCREEN_HEIGHT - random.randint(low, high)
        self.rect = self.image.get_rect()
        self.rect.center = (28, 56)

    def move(self):
        self.x -= SCROLL_SPEED

    def draw(self):
        # Draw the sprite
        screen.blit(self.image, (self.x, self.y))

    def random_y(self):
        self.y = SCREEN_HEIGHT - random.randint(self.low, self.high)

    def higher(self, new_high):
        self.high = new_high


class Platforms:
    # Represents every 'platform' created in game
    def __init__(self, start_x):
        # Initialisation
        self.image = pygame.image.load("Assets/platform.png").convert_alpha()
        self.x = start_x
        self.y = SCREEN_HEIGHT - 112
        self.rect = self.image.get_rect()

    def move(self):
        self.x -= SCROLL_SPEED

    def draw(self):
        # Draw the sprite
        screen.blit(self.image, (self.x, self.y))


class Player:
    # Represents the player object
    def __init__(self):
        # pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets/player.png").convert_alpha()
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2

        self.rect = self.image.get_rect()
        self.rect.center = (28, 28)

    def draw(self):
        # Draw the sprite
        screen.blit(self.image, (self.x, self.y))

    def hit_by(self, hit):
        return ((self.x + 28) - hit.x) ** 2 + ((self.y + 56) - hit.y) ** 2 < 1960


# Define the level
platforms = (Platforms(0), Platforms(SCREEN_WIDTH))
pillars = (
    Pillars(SCREEN_WIDTH * 0.25), Pillars(SCREEN_WIDTH * 0.5), Pillars(SCREEN_WIDTH * 0.75), Pillars(SCREEN_WIDTH),
    Pillars(SCREEN_WIDTH * 1.25), Pillars(SCREEN_WIDTH * 1.5), Pillars(SCREEN_WIDTH * 1.75), Pillars(SCREEN_WIDTH * 2))



player = Player()

# Run until quit
currentIndex = 1
running = True
while running:

    # Has the close button been pressed?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()

    # Fill the background with purple
    screen.fill((190, 170, 240))

    # Collision


    for platform in platforms:
        platform.draw()
        platform.move()

        if platform.x < -SCREEN_WIDTH:
            platform.x += SCREEN_WIDTH * 2
            currentIndex += 1

    for pillar in pillars:
        pillar.draw()
        pillar.move()

        if player.hit_by(pillar):
            print("Will show text")
             # Show text here

        if currentIndex % 5 == 0:
            pillar.higher(pillar.high * 1.2)
        if currentIndex >= 25:
            SCROLL_SPEED = 1.25
        elif currentIndex >= 50:
            SCROLL_SPEED = 1.5
        elif currentIndex >= 75:
            SCROLL_SPEED = 2

        if pillar.high > SCREEN_HEIGHT / 2:
            pillar.higher(SCREEN_HEIGHT / 2)

        if pillar.x < -SCREEN_WIDTH:
            pillar.x += SCREEN_WIDTH * 2
            pillar.random_y()

    if pressed_keys[K_SPACE]:
        player.y -= 1

    if player.y < SCREEN_HEIGHT - 168:
        player.y += GRAVITY
    else:
        player.y = SCREEN_HEIGHT - 168

    player.draw()

    #print(currentIndex)
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
