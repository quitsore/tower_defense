import pygame
import math

# Init
pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 50, 50)

# Arc settings
rect = pygame.Rect(100, 100, 200, 200)
start_angle = math.radians(90)  # Top of the circle
end_angle = start_angle + math.radians(360)  # Full circle
speed = math.radians(1)

# Main loop
running = True
while running:
    screen.fill(WHITE)

    if end_angle > start_angle:
        pygame.draw.arc(screen, RED, rect, start_angle, end_angle, 8)
        start_angle += speed  # Shrinking counterclockwise

    pygame.display.flip()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
