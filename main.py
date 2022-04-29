## Assessment 3 Games Programming

# Initialise pygame
import pygame
pygame.init()

# Draw window
screen = pygame.display.set_mode([1270, 720])

# Run until quit
running = True
while running:

    # Has the close button been pressed?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
