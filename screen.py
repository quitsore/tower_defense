import pygame

def display():
    pygame.init()
    screen_width = 800
    screen_height = 600

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("my game")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            screen.fill((0, 0, 0))
            pygame.display.flip()
    pygame.quit()

display()
