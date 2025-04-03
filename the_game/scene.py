import pygame

from map import Map


class Scene:
    def __init__(self):
        self.path = pygame.image.load("../resources/path-40x40.png").convert()
        self.grass = pygame.image.load("../resources/grass-40x40.png").convert()
        self.placement = pygame.image.load("../resources/brick-40x40.png").convert()
        self.tower_shop = pygame.image.load("../resources/tower-32x40.png").convert()
        self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.game_map = Map("terrain.txt")

    def draw_map(self):
        color = None
        for row_idx, row in enumerate(self.game_map.map):
            for col_idx, cell in enumerate(row):
                if cell == Map.FREE:
                    self.screen.blit(self.path, (col_idx * 40, row_idx * 40))
                elif cell == Map.TERRAIN:
                    self.screen.blit(self.grass, (col_idx * 40, row_idx * 40))
                elif cell == Map.TOWER:
                    self.screen.blit(self.placement, (col_idx * 40, row_idx * 40))
                elif cell == Map.CASTLE:
                    color = pygame.Color(255, 215, 0, 255)
                    pygame.draw.rect(self.screen, color,
                                     pygame.Rect(col_idx * 40, row_idx * 40, 40, 40))
                elif cell == 8:
                    self.screen.blit(self.tower_shop, (col_idx * 32, 160))
                if cell == Map.BOT:
                    color = pygame.Color(93, 93, 93, 255)
                    pygame.draw.rect(self.screen, color,
                                     pygame.Rect(col_idx * 40, row_idx * 40, 40, 40))
