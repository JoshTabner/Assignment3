## Assessment 3 Games Programming

# Initialise pygame
import random

import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 1270
SCREEN_HEIGHT = 720

# Draw window
screen = pygame.display.set_mode([1270, 720])


class Pillars:
    # Represents every 'pillar' created in game
    def __init__(self, startX):
        # Initialisation
        self.image = pygame.image.load("Assets/pillar.png").convert_alpha()
        self.x = startX
        self.y = SCREEN_HEIGHT - random.randint(250, 450)

    def move(self):
        self.x -= 1

    def draw(self):
        # Draw the sprite
        screen.blit(self.image, (self.x, self.y))


class Platforms:
    # Represents every 'platform' created in game
    def __init__(self, startX):
        # Initialisation
        self.image = pygame.image.load("Assets/platform.png").convert_alpha()
        self.x = startX
        self.y = SCREEN_HEIGHT - 112

    def move(self):
        self.x -= 1

    def draw(self):
        # Draw the sprite
        screen.blit(self.image, (self.x, self.y))


# Define the level
platforms = []
pillars = []

# Level Generation
for i in range(0, 11):
    platform = Platforms(SCREEN_WIDTH * i)
    platforms.append(platform)

    # Pillars created at random x coordinates on each platform
    pillar1 = Pillars(random.randint(300 * i, SCREEN_WIDTH * i))
    if i > 0:
        if pillar1.x - pillars[i - 1].x < 224 or pillars[i - 1].x - pillar1.x < -224:
            pillar1.x += 448

    pillars.append(pillar1)

    if random.randint(1, 100) > 40:
        pillar2 = Pillars(random.randint(300 * i, SCREEN_WIDTH * i))
        if i > 0:
            if pillar2.x - pillars[i - 1].x < 224 or pillars[i - 1].x - pillar2.x < -224:
                pillar2.x += 448

        pillars.append(pillar2)

# Run until quit
currentIndex = 11
running = True
while running:

    # Has the close button been pressed?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((100, 20, 255))

    # Draw a solid blue circle in the center
    # pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    for i in range(0, len(platforms)):
        platforms[i].draw()
        platforms[i].draw()
        platforms[i].move()

        if platforms[i].x < -SCREEN_WIDTH:
            platforms.remove(platforms[i])

            platform = Platforms(SCREEN_WIDTH * i)
            platforms.append(platform)

    for i in range(0, len(pillars)):
        pillars[i].draw()
        pillars[i].move()

        ### NEEDS WORK - TRYING TO INCREASE STABILITY AND PREVENT OVERLAPPING PILLARS
        if pillars[i].x < -SCREEN_WIDTH:
            pillars.remove(pillars[i])

            pillar = Pillars(random.randint(300 * (i + 3), SCREEN_WIDTH * (i + 3)))
            if i > 0:
                if pillar.x - pillars[i - 1].x < 224 or pillars[i - 1].x - pillar.x < -224:
                    pillar.x += 336

            pillars.append(pillar)

    currentIndex += 12

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
