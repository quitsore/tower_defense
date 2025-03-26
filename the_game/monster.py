import pygame

class Monster:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = pygame.Color(255, 0, 0, 255)


    def draw(self, screen):
        self.x += 1.28
        self.y += 0.72
        pygame.draw.rect(screen, self.color,
                         pygame.Rect(self.x, self.y, 40, 40))