## Assessment 3 Games Programming

# Initialise pygame
import random
import sys

import pygame
from pygame import mixer
from pygame.locals import *

pygame.init()
pygame.font.init()

# Sounds
mixer.init()
mixer.music.load("Assets/background.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(-1)

jump_sound = pygame.mixer.Sound("Assets/jump.wav")
pygame.mixer.Sound.set_volume(jump_sound, 0.05)
death_sound = pygame.mixer.Sound("Assets/death.wav")
pygame.mixer.Sound.set_volume(death_sound, 0.15)

# Score
text_display = pygame.font.SysFont('Arial', 30)
score = 0

# Colours & Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

SCREEN_WIDTH = 1270
SCREEN_HEIGHT = 720

SCROLL_SPEED = 0.5
GRAVITY = 0.25

# Draw window
screen = pygame.display.set_mode([1270, 720])


# Define pressed_keys
# key_pressed = pygame.key.get_pressed()


class Pillars:
    # Represents every 'pillar' created in game
    def __init__(self, start_x, low=168, high=200):
        # Initialisation
        # pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets/pillar.png").convert_alpha()
        self.x = start_x
        self.high = high
        self.low = low
        self.y = SCREEN_HEIGHT - random.randint(low, high)
        self.rect = self.image.get_rect()
        self.rect.center = (56, 200)
        self.reverse = False

    def move(self):
        self.x -= SCROLL_SPEED

    def draw(self):
        # Draw the sprite
        screen.blit(self.image, (self.x, self.y))

    def random_y(self):
        self.y = SCREEN_HEIGHT - random.randint(self.low, self.high)

    def higher(self, new_high):
        self.high = new_high


class ReversePillars(Pillars):
    # For every pillar on the ceiling
    def __init__(self, start_x, low=-344, high=-140):
        super().__init__(start_x, low, high)
        self.image = pygame.image.load("Assets/pillar.png").convert_alpha()
        self.x = start_x
        self.high = high
        self.low = low
        self.y = random.randint(low, high)
        self.reverse = True

    def random_y(self):
        self.y = random.randint(self.low, self.high)

    def higher(self, new_high):
        self.high = 0


class Platforms:
    # Represents every 'platform' created in game
    def __init__(self, start_x):
        # Initialisation
        self.image = pygame.image.load("Assets/platform.png").convert_alpha()
        self.x = start_x
        self.y = SCREEN_HEIGHT - 112
        self.rect = self.image.get_rect()
        self.rect.center = (635, 56)

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
        self.dy = 0  # Acceleration

        self.rect = self.image.get_rect()
        self.rect.center = (28, 28)

    def draw(self):
        # Draw the sprite
        screen.blit(self.image, (self.x, self.y))

    # def hit_by(self, hit, type):
    #     if type == "platform":
    #
    #     elif type == "pillar":
    #         return ((self.x + 28) - hit.x) ** 2 + ((self.y + 100) - hit.y) ** 2 < 21568
    #     else:
    #         return False


# Define the level
platforms = (Platforms(0), Platforms(SCREEN_WIDTH))
# pillars = (
#     Pillars(SCREEN_WIDTH * 0.25), Pillars(SCREEN_WIDTH * 0.5), Pillars(SCREEN_WIDTH * 0.75), Pillars(SCREEN_WIDTH),
#     Pillars(SCREEN_WIDTH * 1.25), Pillars(SCREEN_WIDTH * 1.5), Pillars(SCREEN_WIDTH * 1.75),
#     Pillars(SCREEN_WIDTH * 2))

pillars = (
    Pillars(SCREEN_WIDTH * 0.34), Pillars(SCREEN_WIDTH * 0.67), Pillars(SCREEN_WIDTH),
    Pillars(SCREEN_WIDTH * 1.34), Pillars(SCREEN_WIDTH * 1.67), Pillars(SCREEN_WIDTH * 2),

    ReversePillars(SCREEN_WIDTH * 0.34), ReversePillars(SCREEN_WIDTH * 0.67), ReversePillars(SCREEN_WIDTH),
    ReversePillars(SCREEN_WIDTH * 1.34), ReversePillars(SCREEN_WIDTH * 1.67), ReversePillars(SCREEN_WIDTH * 2))

player = Player()

# Run until quit
currentIndex = 1
running = True
dead = False
while running:
    # Has the close button been pressed?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with purple
    screen.fill((100, 100, 240))

    for platform in platforms:
        platform.draw()
        platform.move()

        if pygame.Rect(platform.x, platform.y, 1270, 112).collidepoint(player.x, player.y + 56) and not dead:
            pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            SCROLL_SPEED = 0
            GRAVITY = 0

            text_surface = text_display.render("YOU HAVE FAILED", False, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH/2 - 30, SCREEN_HEIGHT/2-30))
            dead = True

        if platform.x < -SCREEN_WIDTH:
            platform.x += SCREEN_WIDTH * 2
            currentIndex += 1

    for pillar in pillars:
        pillar.draw()
        pillar.move()

        if not dead:
            if pillar.reverse and pygame.Rect(pillar.x, pillar.y, 112, 400).collidepoint(player.x, player.y):
                pygame.mixer.Sound.play(death_sound)
                pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
                SCROLL_SPEED = 0
                GRAVITY = 0

                text_surface = text_display.render("YOU HAVE FAILED", False, WHITE)
                screen.blit(text_surface, (SCREEN_WIDTH/2 - 30, SCREEN_HEIGHT/2-30))
                dead = True

            elif not pillar.reverse and pygame.Rect(pillar.x, pillar.y, 112, 400).collidepoint(player.x, player.y + 56):
                pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
                pygame.mixer.Sound.play(death_sound)
                SCROLL_SPEED = 0
                GRAVITY = 0

                text_surface = text_display.render("YOU HAVE FAILED", False, WHITE)
                screen.blit(text_surface, (SCREEN_WIDTH / 2 - 30, SCREEN_HEIGHT / 2 - 30))
                dead = True

        #  Gradually increase random range
        if currentIndex % 5 == 0:
            pillar.higher(pillar.high + 5)

        # Increment game speed
        if currentIndex >= 15:
            SCROLL_SPEED = 0.75
        elif currentIndex >= 30:
            SCROLL_SPEED = 1
        elif currentIndex >= 45:
            SCROLL_SPEED = 1.5
        elif currentIndex >= 60:
            SCROLL_SPEED = 2

        if pillar.reverse and pillar.high > -160:
            pillar.higher(-240)
        elif not pillar.reverse and pillar.high > 240:
            pillar.higher(240)

        if pillar.x < -SCREEN_WIDTH:
            score += 10
            pillar.x += SCREEN_WIDTH * 2
            pillar.random_y()

    key_pressed = pygame.key.get_pressed()
    if key_pressed[K_SPACE] and not dead:
        pygame.mixer.Sound.play(jump_sound)
        player.y -= 0.6

    player.y += GRAVITY
    player.draw()

    if dead:
        pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        SCROLL_SPEED = 0
        GRAVITY = 0

        text_surface = text_display.render("YOU HAVE FAILED", False, WHITE)
        screen.blit(text_surface, (SCREEN_WIDTH / 2 - 30, SCREEN_HEIGHT / 2 - 30))

    # print(player.dy)

    # Score Display
    text_surface = text_display.render(str(score), False, WHITE)
    screen.blit(text_surface, (25, 25))
    # Flip the display
    pygame.display.flip()

# JUMPS

# target height = 160 pixels
# 160 = time squared / 2
# time = 17.88854382

# Done! Time to quit.
pygame.quit()
